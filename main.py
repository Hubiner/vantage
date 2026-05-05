import asyncio
import math
import time
from typing import Any

import yfinance as yf
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

app = FastAPI(title="Vantage", version="2.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── TTL Cache ──────────────────────────────────────────────────────────────
_cache: dict[str, tuple[Any, float]] = {}

def cache_get(key: str, ttl: int) -> Any:
    entry = _cache.get(key)
    if entry and (time.time() - entry[1]) < ttl:
        return entry[0]
    return None

def cache_set(key: str, value: Any) -> None:
    _cache[key] = (value, time.time())

# ── Helpers ────────────────────────────────────────────────────────────────
DISPLAY_NAMES: dict[str, str] = {
    "^GSPC": "S&P 500",
    "^IXIC": "NASDAQ",
    "^DJI": "Dow Jones",
    "^BVSP": "Ibovespa",
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    "SOL-USD": "Solana",
}

def clean(value: Any) -> Any:
    if value is None:
        return None
    try:
        f = float(value)
        if math.isnan(f) or math.isinf(f):
            return None
        return round(f, 4)
    except (TypeError, ValueError):
        return value

def fi_get(fi: Any, attr: str, default: Any = None) -> Any:
    try:
        val = getattr(fi, attr, default)
        if val is None:
            return default
        return val
    except Exception:
        return default

def get_meta(ticker: str, stock: Any) -> dict:
    cached = cache_get(f"meta:{ticker}", 600)
    if cached:
        return cached
    try:
        info = stock.info
        meta = {
            "name": info.get("longName") or info.get("shortName") or DISPLAY_NAMES.get(ticker, ticker),
            "sector": info.get("sector", ""),
            "pe_ratio": clean(info.get("trailingPE")),
            "dividend_yield": clean(info.get("dividendYield")),
        }
    except Exception:
        meta = {
            "name": DISPLAY_NAMES.get(ticker, ticker),
            "sector": "",
            "pe_ratio": None,
            "dividend_yield": None,
        }
    cache_set(f"meta:{ticker}", meta)
    return meta

# ── Routes ─────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


@app.get("/api/quote/{ticker}")
def get_quote(ticker: str):
    ticker = ticker.upper()
    cached = cache_get(f"quote:{ticker}", 60)
    if cached:
        return cached

    try:
        stock = yf.Ticker(ticker)
        fi = stock.fast_info

        price = fi_get(fi, "last_price")
        prev_close = fi_get(fi, "previous_close") or fi_get(fi, "regular_market_previous_close")

        if price is None:
            raise HTTPException(status_code=404, detail=f"Ativo '{ticker}' não encontrado ou sem dados de preço.")

        change = round(price - prev_close, 4) if prev_close else None
        change_pct = round((change / prev_close) * 100, 2) if change and prev_close else None

        meta = get_meta(ticker, stock)

        result = {
            "ticker": ticker,
            "name": meta["name"],
            "price": clean(price),
            "change": clean(change),
            "change_pct": clean(change_pct),
            "open": clean(fi_get(fi, "open")),
            "high": clean(fi_get(fi, "day_high")),
            "low": clean(fi_get(fi, "day_low")),
            "volume": fi_get(fi, "last_volume"),
            "market_cap": fi_get(fi, "market_cap"),
            "currency": fi_get(fi, "currency", "USD"),
            "exchange": fi_get(fi, "exchange", ""),
            "sector": meta["sector"],
            "pe_ratio": meta["pe_ratio"],
            "dividend_yield": meta["dividend_yield"],
            "52w_high": clean(fi_get(fi, "year_high")),
            "52w_low": clean(fi_get(fi, "year_low")),
        }
        cache_set(f"quote:{ticker}", result)
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ativo '{ticker}' não encontrado: {str(e)}")


@app.get("/api/history/{ticker}")
def get_history(ticker: str, period: str = "3mo", interval: str = "1d"):
    valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"]
    valid_intervals = ["1m", "5m", "15m", "30m", "60m", "1d", "1wk", "1mo"]

    if period not in valid_periods:
        raise HTTPException(status_code=400, detail=f"Período inválido. Use: {valid_periods}")
    if interval not in valid_intervals:
        raise HTTPException(status_code=400, detail=f"Intervalo inválido. Use: {valid_intervals}")

    cache_key = f"history:{ticker}:{period}:{interval}"
    cached = cache_get(cache_key, 300)
    if cached:
        return cached

    try:
        df = yf.Ticker(ticker.upper()).history(period=period, interval=interval)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"Sem dados históricos para '{ticker}'")

        df.index = df.index.strftime("%Y-%m-%dT%H:%M:%S")
        result = {
            "ticker": ticker.upper(),
            "period": period,
            "interval": interval,
            "data": [
                {
                    "date": idx,
                    "open": clean(row["Open"]),
                    "high": clean(row["High"]),
                    "low": clean(row["Low"]),
                    "close": clean(row["Close"]),
                    "volume": int(row["Volume"]) if not math.isnan(float(row["Volume"])) else None,
                }
                for idx, row in df.iterrows()
            ],
        }
        cache_set(cache_key, result)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/indicators/{ticker}")
def get_indicators(ticker: str, period: str = "6mo"):
    cache_key = f"indicators:{ticker}:{period}"
    cached = cache_get(cache_key, 300)
    if cached:
        return cached

    try:
        df = yf.Ticker(ticker.upper()).history(period=period, interval="1d")
        if df.empty:
            raise HTTPException(status_code=404, detail=f"Sem dados para '{ticker}'")

        close = df["Close"]
        df["SMA20"] = SMAIndicator(close=close, window=20).sma_indicator()
        df["SMA50"] = SMAIndicator(close=close, window=50).sma_indicator()
        df["EMA9"] = EMAIndicator(close=close, window=9).ema_indicator()
        df["RSI"] = RSIIndicator(close=close, window=14).rsi()

        macd_obj = MACD(close=close, window_slow=26, window_fast=12, window_sign=9)
        df["MACD"] = macd_obj.macd()
        df["MACD_signal"] = macd_obj.macd_signal()
        df["MACD_hist"] = macd_obj.macd_diff()

        bb_obj = BollingerBands(close=close, window=20, window_dev=2)
        df["BB_upper"] = bb_obj.bollinger_hband()
        df["BB_mid"] = bb_obj.bollinger_mavg()
        df["BB_lower"] = bb_obj.bollinger_lband()

        df.index = df.index.strftime("%Y-%m-%dT%H:%M:%S")
        result = {
            "ticker": ticker.upper(),
            "period": period,
            "data": [
                {
                    "date": idx,
                    "close": clean(row["Close"]),
                    "sma20": clean(row.get("SMA20")),
                    "sma50": clean(row.get("SMA50")),
                    "ema9": clean(row.get("EMA9")),
                    "rsi": clean(row.get("RSI")),
                    "macd": clean(row.get("MACD")),
                    "macd_signal": clean(row.get("MACD_signal")),
                    "macd_hist": clean(row.get("MACD_hist")),
                    "bb_upper": clean(row.get("BB_upper")),
                    "bb_mid": clean(row.get("BB_mid")),
                    "bb_lower": clean(row.get("BB_lower")),
                }
                for idx, row in df.iterrows()
            ],
        }
        cache_set(cache_key, result)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market")
async def get_market():
    cached = cache_get("market", 120)
    if cached:
        return cached

    symbols = {
        "^GSPC": "S&P 500",
        "^IXIC": "NASDAQ",
        "^DJI": "DOW",
        "BTC-USD": "Bitcoin",
        "^BVSP": "IBOV",
    }

    async def fetch_one(sym: str, label: str) -> dict:
        try:
            fi = await asyncio.to_thread(lambda: yf.Ticker(sym).fast_info)
            price = fi_get(fi, "last_price")
            prev = fi_get(fi, "previous_close") or fi_get(fi, "regular_market_previous_close")
            change_pct = round((price - prev) / prev * 100, 2) if price and prev else None
            return {"symbol": sym, "label": label, "price": clean(price), "change_pct": clean(change_pct)}
        except Exception:
            return {"symbol": sym, "label": label, "price": None, "change_pct": None}

    indices = await asyncio.gather(*[fetch_one(s, l) for s, l in symbols.items()])
    result = {"indices": list(indices)}
    cache_set("market", result)
    return result


@app.get("/api/search/{query}")
def search_ticker(query: str):
    try:
        results = yf.Search(query, max_results=8)
        quotes = results.quotes if hasattr(results, "quotes") else []
        return {
            "results": [
                {
                    "ticker": q.get("symbol", ""),
                    "name": q.get("longname") or q.get("shortname") or q.get("symbol", ""),
                    "exchange": q.get("exchange", ""),
                    "type": q.get("quoteType", ""),
                }
                for q in quotes
                if q.get("symbol")
            ]
        }
    except Exception:
        return {"results": []}
