# Vantage — Rebrand & Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the app to "Vantage", adicionar métricas reais de mercado, polir visualmente sem mudar o layout, e preparar o deploy na Vercel.

**Architecture:** Single-file frontend (`static/index.html`) servido por FastAPI via `FileResponse`. Todos os dados vêm de yfinance via API REST com cache TTL em memória. Vercel deploy usa Python serverless com `vercel.json` roteando tudo para `main.py`.

**Tech Stack:** Python 3.11+ · FastAPI · yfinance · ta · Chart.js 4 (CDN) · Vercel Python runtime

---

## File Map

| Arquivo | O que muda |
|---------|-----------|
| `static/index.html` | Rename + novo logo + mais stats + market bar expandido + market status |
| `main.py` | Rename + novos campos em get_meta/get_quote + mais symbols no market bar + market status + GZip + batch endpoint + remove StaticFiles |
| `vercel.json` | Arquivo novo — configuração de deploy |
| `README.md` | Rename + instrução de deploy na Vercel |

---

## Task 1: Rename — Pulse/StockBoard → Vantage

**Files:**
- Modify: `static/index.html:6` (title), `static/index.html:276` (logo span), `static/index.html:317-319` (empty state)
- Modify: `main.py:15` (FastAPI title)
- Modify: `README.md:1,79` (título e estrutura de pasta)

- [ ] **Step 1: Atualizar `<title>` e logo em `index.html`**

Em `static/index.html`, linha 6:
```html
<!-- ANTES -->
<title>Pulse</title>

<!-- DEPOIS -->
<title>Vantage</title>
```

Linha 276 (logo span):
```html
<!-- ANTES -->
<span class="logo">📈 Pulse</span>

<!-- DEPOIS -->
<span class="logo">
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style="flex-shrink:0">
    <path d="M2 12L6 7L9 10L14 4" stroke="url(#lg)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <defs><linearGradient id="lg" x1="2" y1="12" x2="14" y2="4" gradientUnits="userSpaceOnUse">
      <stop stop-color="#58a6ff"/><stop offset="1" stop-color="#bc8cff"/>
    </linearGradient></defs>
  </svg>
  Vantage
</span>
```

- [ ] **Step 2: Atualizar empty state em `index.html`**

Linhas 316-319 (dentro de `<main id="main">`):
```html
<!-- ANTES -->
<div class="state-box">
  <div class="state-icon">📊</div>
  <div class="state-title">StockBoard</div>
  <div class="state-sub">Selecione um ativo na watchlist ou explore em Browse para começar.</div>
</div>

<!-- DEPOIS -->
<div class="state-box">
  <div class="state-icon">📈</div>
  <div class="state-title">Vantage</div>
  <div class="state-sub">Selecione um ativo na watchlist ou explore em <strong>Browse</strong> para começar.</div>
</div>
```

- [ ] **Step 3: Atualizar `main.py`**

Linha 15:
```python
# ANTES
app = FastAPI(title="Pulse", version="2.0.0")

# DEPOIS
app = FastAPI(title="Vantage", version="2.0.0")
```

- [ ] **Step 4: Atualizar `README.md`**

Linha 1:
```markdown
# Vantage
```

Linha 79 (estrutura de pasta):
```
vantage/
├── main.py
├── vercel.json
├── requirements.txt
└── static/
    └── index.html
```

- [ ] **Step 5: Commit**

```bash
git add static/index.html main.py README.md
git commit -m "rebrand: rename Pulse/StockBoard to Vantage"
```

---

## Task 2: Novo logo CSS — gradiente e tipografia

**Files:**
- Modify: `static/index.html` (bloco `/* ── Variables */` e `.logo`)

- [ ] **Step 1: Atualizar estilos do logo**

No bloco CSS, substitua a regra `.logo` existente (linha 55):
```css
/* ANTES */
.logo { font-size:16px; font-weight:700; color:var(--accent); white-space:nowrap; letter-spacing:-.3px; }

/* DEPOIS */
.logo {
  font-size:16px; font-weight:800; white-space:nowrap; letter-spacing:-.4px;
  background:linear-gradient(135deg, #58a6ff 0%, #bc8cff 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text;
  display:flex; align-items:center; gap:7px;
  text-decoration:none;
}
```

- [ ] **Step 2: Commit**

```bash
git add static/index.html
git commit -m "style: gradient logo for Vantage branding"
```

---

## Task 3: Expandir métricas do quote card (dados reais de mercado)

**Files:**
- Modify: `main.py` — `get_meta()` e `get_quote()`
- Modify: `static/index.html` — `renderDashboard()`

Métricas adicionadas: **Beta**, **EPS TTM**, **Target Price** (consenso analistas), **Avg Volume 10d**, **P/B Ratio**, **Receita TTM**.

- [ ] **Step 1: Estender `get_meta()` em `main.py`**

Substitua a função `get_meta` completa:
```python
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
            "beta": clean(info.get("beta")),
            "eps": clean(info.get("trailingEps")),
            "target_price": clean(info.get("targetMeanPrice")),
            "pb_ratio": clean(info.get("priceToBook")),
            "revenue": clean(info.get("totalRevenue")),
            "avg_volume_10d": clean(info.get("averageVolume10days") or info.get("averageVolume")),
        }
    except Exception:
        meta = {
            "name": DISPLAY_NAMES.get(ticker, ticker),
            "sector": "",
            "pe_ratio": None,
            "dividend_yield": None,
            "beta": None,
            "eps": None,
            "target_price": None,
            "pb_ratio": None,
            "revenue": None,
            "avg_volume_10d": None,
        }
    cache_set(f"meta:{ticker}", meta)
    return meta
```

- [ ] **Step 2: Propagar novos campos em `get_quote()` em `main.py`**

No bloco `result = { ... }` de `get_quote`, adicione após `"dividend_yield"`:
```python
"beta": meta["beta"],
"eps": meta["eps"],
"target_price": meta["target_price"],
"pb_ratio": meta["pb_ratio"],
"revenue": meta["revenue"],
"avg_volume_10d": meta["avg_volume_10d"],
```

- [ ] **Step 3: Renderizar novos stats em `renderDashboard()` em `index.html`**

No template `renderDashboard`, substitua o bloco `.stats-grid`:
```html
<div class="stats-grid">
  <div class="stat"><div class="stat-label">Abertura</div><div class="stat-value">${fmt.price(quote.open)}</div></div>
  <div class="stat"><div class="stat-label">Máxima</div><div class="stat-value pos">${fmt.price(quote.high)}</div></div>
  <div class="stat"><div class="stat-label">Mínima</div><div class="stat-value neg">${fmt.price(quote.low)}</div></div>
  <div class="stat"><div class="stat-label">Volume</div><div id="live-vol" class="stat-value">${fmt.large(quote.volume)}</div></div>
  <div class="stat"><div class="stat-label">Vol Méd 10d</div><div class="stat-value">${fmt.large(quote.avg_volume_10d)}</div></div>
  <div class="stat"><div class="stat-label">Market Cap</div><div class="stat-value">${fmt.large(quote.market_cap)}</div></div>
  <div class="stat"><div class="stat-label">P/L</div><div class="stat-value">${quote.pe_ratio ? Number(quote.pe_ratio).toFixed(2) : '—'}</div></div>
  <div class="stat"><div class="stat-label">P/VP</div><div class="stat-value">${quote.pb_ratio ? Number(quote.pb_ratio).toFixed(2) : '—'}</div></div>
  <div class="stat"><div class="stat-label">EPS TTM</div><div class="stat-value">${quote.eps ? fmt.price(quote.eps) : '—'}</div></div>
  <div class="stat"><div class="stat-label">Beta</div><div class="stat-value">${quote.beta ? Number(quote.beta).toFixed(2) : '—'}</div></div>
  <div class="stat"><div class="stat-label">Div. Yield</div><div class="stat-value">${quote.dividend_yield ? (quote.dividend_yield*100).toFixed(2)+'%' : '—'}</div></div>
  <div class="stat"><div class="stat-label">Alvo Analistas</div><div class="stat-value">${quote.target_price ? fmt.price(quote.target_price) : '—'}</div></div>
  <div class="stat"><div class="stat-label">Receita TTM</div><div class="stat-value">${fmt.large(quote.revenue)}</div></div>
  <div class="stat"><div class="stat-label">Máx 52s</div><div class="stat-value">${fmt.price(quote['52w_high'])}</div></div>
  <div class="stat"><div class="stat-label">Mín 52s</div><div class="stat-value">${fmt.price(quote['52w_low'])}</div></div>
  <div class="stat"><div class="stat-label">RSI 14</div><div class="stat-value">${lastRSI ? lastRSI.toFixed(1) : '—'} ${rsiPill}</div></div>
</div>
```

- [ ] **Step 4: Ajustar grid para acomodar mais stats**

No CSS, linha 232:
```css
/* ANTES */
.stats-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(110px,1fr)); gap:10px; }

/* DEPOIS */
.stats-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(120px,1fr)); gap:10px; }
```

- [ ] **Step 5: Commit**

```bash
git add main.py static/index.html
git commit -m "feat: add beta, eps, target price, P/B, revenue, avg volume to quote card"
```

---

## Task 4: Expandir market bar + indicador de status de mercado

**Files:**
- Modify: `main.py` — `get_market()`, adicionar helper `is_us_market_open()`
- Modify: `static/index.html` — `loadMarketBar()`, adicionar status dot no header

Novos símbolos: **VIX** (índice de medo), **Gold** (GC=F), **Oil WTI** (CL=F), **EUR/USD** (EURUSD=X).

- [ ] **Step 1: Adicionar helper `is_us_market_open()` em `main.py`**

Adicione antes de `@app.get("/api/market")`:
```python
def is_us_market_open() -> bool:
    from zoneinfo import ZoneInfo
    from datetime import datetime, time as dtime
    now = datetime.now(ZoneInfo("America/New_York"))
    if now.weekday() >= 5:
        return False
    return dtime(9, 30) <= now.time() <= dtime(16, 0)
```

- [ ] **Step 2: Expandir symbols em `get_market()` em `main.py`**

Substitua o dict `symbols` dentro de `get_market`:
```python
symbols = {
    "^GSPC":    "S&P 500",
    "^IXIC":    "NASDAQ",
    "^DJI":     "DOW",
    "^BVSP":    "IBOV",
    "^VIX":     "VIX",
    "BTC-USD":  "BTC",
    "GC=F":     "Ouro",
    "CL=F":     "WTI",
    "EURUSD=X": "EUR/USD",
}
```

- [ ] **Step 3: Adicionar `market_open` na resposta de `get_market()`**

No final de `get_market`, antes de `return result`:
```python
result = {"indices": list(indices), "market_open": is_us_market_open()}
```

- [ ] **Step 4: Adicionar elemento de status no header em `index.html`**

Após `<span class="header-time" id="headerTime"></span>`, adicione:
```html
<span id="marketStatus" class="market-status"></span>
```

- [ ] **Step 5: Adicionar CSS do market status**

No bloco CSS, após `.header-time`:
```css
.market-status {
  font-size:10px; font-weight:700; letter-spacing:.06em; text-transform:uppercase;
  padding:3px 8px; border-radius:20px; white-space:nowrap; flex-shrink:0;
}
.market-status.open  { background:var(--green-dim); color:var(--green); }
.market-status.closed { background:rgba(125,133,144,.15); color:var(--muted); }
```

- [ ] **Step 6: Atualizar `loadMarketBar()` em `index.html` para usar `market_open`**

Substitua a função `loadMarketBar`:
```js
async function loadMarketBar() {
  try {
    const data = await api('/market');
    const bar = document.getElementById('marketBar');
    bar.innerHTML = data.indices.map(i => {
      const cls = cc(i.change_pct);
      const chgStr = i.change_pct != null ? (i.change_pct > 0?'+':'') + i.change_pct.toFixed(2)+'%' : '—';
      const priceStr = i.price != null ? Number(i.price).toLocaleString('pt-BR',{maximumFractionDigits:2}) : '—';
      return `<div class="mi">
        <span class="mi-label">${i.label}</span>
        <span class="mi-price">${priceStr}</span>
        <span class="mi-chg ${cls}">${chgStr}</span>
      </div>`;
    }).join('');
    const statusEl = document.getElementById('marketStatus');
    if (statusEl) {
      statusEl.textContent = data.market_open ? '● Mercado Aberto' : '● Mercado Fechado';
      statusEl.className = 'market-status ' + (data.market_open ? 'open' : 'closed');
    }
  } catch(e) {
    document.getElementById('marketBar').innerHTML = '<span class="mi-loading" style="color:var(--red)">⚠ mercado indisponível</span>';
  }
}
```

- [ ] **Step 7: Commit**

```bash
git add main.py static/index.html
git commit -m "feat: expand market bar (VIX, Gold, WTI, EURUSD) + market open/closed status"
```

---

## Task 5: Performance — GZip middleware + batch quotes endpoint

**Files:**
- Modify: `main.py` — adicionar GZipMiddleware e novo endpoint `/api/quotes`
- Modify: `static/index.html` — `renderWatchlist()` usa batch endpoint

O batch endpoint elimina N requests paralelas na watchlist (1 request em vez de N).

- [ ] **Step 1: Adicionar GZip middleware em `main.py`**

Após a linha `app = FastAPI(...)`, adicione:
```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=500)
```

- [ ] **Step 2: Adicionar endpoint `/api/quotes` em `main.py`**

Adicione antes de `@app.get("/api/history")`:
```python
@app.get("/api/quotes")
def get_quotes(tickers: str):
    """Batch quote — tickers separados por vírgula. Ex: ?tickers=AAPL,MSFT,PETR4.SA"""
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()][:20]

    import concurrent.futures
    def fetch(t: str):
        try:
            return get_quote(t)
        except Exception:
            return {"ticker": t, "error": True}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(fetch, ticker_list))

    return {"quotes": results}
```

- [ ] **Step 3: Atualizar `renderWatchlist()` em `index.html` para usar batch**

Substitua o trecho de fetch individual dentro de `renderWatchlist` (o bloco `state.watchlist.forEach(async t => { ... })`):
```js
// Batch fetch — uma request para todos os tickers da watchlist
try {
  const batch = await api('/quotes?tickers=' + state.watchlist.join(','));
  batch.quotes.forEach(q => {
    if (q.error) return;
    const id = q.ticker.replace(/[^a-z0-9]/gi,'_');
    const pEl = document.getElementById('wp-' + id);
    const cEl = document.getElementById('wc-' + id);
    const nEl = document.getElementById('wn-' + id);
    if (pEl) pEl.textContent = fmt.price(q.price);
    if (cEl) { cEl.className = 'watch-chg ' + cc(q.change_pct); cEl.textContent = fmt.pct(q.change_pct); }
    if (nEl) nEl.textContent = q.name;
  });
} catch {
  state.watchlist.forEach(t => {
    const pEl = document.getElementById('wp-' + t.replace(/[^a-z0-9]/gi,'_'));
    if (pEl) { pEl.textContent = '—'; pEl.style.color = 'var(--muted)'; }
  });
}
```

- [ ] **Step 4: Verificar que o endpoint funciona**

Com o servidor rodando (`uvicorn main:app --reload`), teste:
```
GET http://localhost:8000/api/quotes?tickers=AAPL,MSFT,PETR4.SA
```
Esperado: JSON `{"quotes": [{...}, {...}, {...}]}` com os 3 tickers.

- [ ] **Step 5: Commit**

```bash
git add main.py static/index.html
git commit -m "perf: GZip middleware + batch quotes endpoint for watchlist"
```

---

## Task 6: Visual polish — period labels + market bar overflow

**Files:**
- Modify: `static/index.html`

- [ ] **Step 1: Atualizar labels dos period buttons**

Em `renderDashboard`, substitua o map dos period buttons:
```js
// ANTES
${['1mo','3mo','6mo','1y','2y'].map(p=>`<button class="period-btn ${p===state.activePeriod?'active':''}" onclick="changePeriod('${p}')">${p}</button>`).join('')}

// DEPOIS
${[
  {key:'1mo',label:'1M'}, {key:'3mo',label:'3M'},
  {key:'6mo',label:'6M'}, {key:'1y',label:'1A'},
  {key:'2y',label:'2A'}
].map(({key,label})=>`<button class="period-btn ${key===state.activePeriod?'active':''}" onclick="changePeriod('${key}')">${label}</button>`).join('')}
```

No `changePeriod`, o `b.textContent===period` precisa ser atualizado para comparar por data-key. Adicione `data-period` aos botões:
```js
.map(({key,label})=>`<button class="period-btn ${key===state.activePeriod?'active':''}" data-period="${key}" onclick="changePeriod('${key}')">${label}</button>`)
```

Em `changePeriod`, substitua o querySelector:
```js
// ANTES
document.querySelectorAll('.period-btn').forEach(b => b.classList.toggle('active', b.textContent===period));

// DEPOIS
document.querySelectorAll('.period-btn').forEach(b => b.classList.toggle('active', b.dataset.period===period));
```

- [ ] **Step 2: Fazer market bar scrollável quando overflow**

No CSS, substitua `.market-bar`:
```css
.market-bar {
  grid-column:1/-1;
  background:#0a0d12;
  border-bottom:1px solid var(--border-subtle);
  display:flex;
  align-items:center;
  padding:0 18px;
  gap:0;
  overflow-x:auto;
  scrollbar-width:none;
}
.market-bar::-webkit-scrollbar { display:none; }
```

- [ ] **Step 3: Commit**

```bash
git add static/index.html
git commit -m "style: cleaner period labels (1M/3M) + scrollable market bar"
```

---

## Task 7: Configurar deploy na Vercel

**Files:**
- Modify: `main.py` — remover `StaticFiles` mount (desnecessário; único static é `index.html` já servido por `FileResponse`)
- Create: `vercel.json`
- Modify: `README.md` — adicionar seção de deploy

- [ ] **Step 1: Remover mount desnecessário de `main.py`**

Remova a linha:
```python
# REMOVER esta linha
app.mount("/static", StaticFiles(directory="static"), name="static")
```

E remova o import não mais usado:
```python
# REMOVER do import
from fastapi.staticfiles import StaticFiles
```

Confirme que a linha `from fastapi.responses import FileResponse, Response` permanece — ela é necessária para o `FileResponse("static/index.html")`.

- [ ] **Step 2: Criar `vercel.json`**

Crie `vercel.json` na raiz:
```json
{
  "builds": [
    { "src": "main.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "main.py" }
  ]
}
```

> **Nota:** O Vercel bundeia os arquivos do projeto com a função serverless. `FileResponse("static/index.html")` funciona porque o arquivo é incluído no bundle em tempo de build.

- [ ] **Step 3: Adicionar seção Vercel ao `README.md`**

Após a seção `## Execução local`, adicione:
```markdown
## Deploy na Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

**Requisitos:** conta na [Vercel](https://vercel.com) + Vercel CLI (`npm i -g vercel`)

```bash
# Na raiz do projeto
vercel

# Seguir o wizard — framework: Other, build command: vazio, output: vazio
```

**Variáveis de ambiente:** nenhuma necessária — o app usa apenas yfinance (Yahoo Finance público).

**Limitações no plano gratuito:**
- Timeout de função: 10s (padrão) → upgrade para Pro para 60s se necessário
- Cold start: primeira request pode demorar ~2-3s enquanto carrega yfinance + pandas
```

- [ ] **Step 4: Testar build local simulando Vercel**

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Acesse `http://localhost:8000` — deve servir o `index.html` normalmente sem o `StaticFiles` mount.

Verifique que `http://localhost:8000/api/market` retorna os 9 índices expandidos.

- [ ] **Step 5: Commit final**

```bash
git add vercel.json main.py README.md
git commit -m "feat: add Vercel deployment config + remove unused StaticFiles mount"
```

---

## Self-Review

### Spec coverage
| Requisito | Task |
|-----------|------|
| Renomear tudo para Vantage | Task 1 |
| Logo visualmente agradável | Task 1 (SVG) + Task 2 (CSS gradiente) |
| Não mudar onde cada item está | ✅ Layout preservado — apenas stats-grid expandido |
| Informações reais de mercado | Task 3 (beta, EPS, target, P/B, receita) + Task 4 (VIX, ouro, petróleo, EUR/USD) |
| Melhor performance | Task 5 (GZip + batch endpoint) |
| Deploy na Vercel | Task 7 |

### Gaps identificados
- Nenhum — todas as mudanças são aditivas e não quebram funcionalidade existente.

### Notas de consistência
- `changePeriod()` usa `b.textContent===period` → corrigido na Task 6 para `b.dataset.period`
- `get_quote()` retorna cache antes de ir ao yfinance → os novos campos (`beta`, `eps`, etc.) estarão presentes porque `get_meta()` (que os busca) também é cacheada por 600s
- O batch endpoint `/api/quotes` chama `get_quote()` internamente, então usa o mesmo cache TTL de 60s — consistente
