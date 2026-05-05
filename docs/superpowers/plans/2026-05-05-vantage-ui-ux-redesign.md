# Vantage UI/UX Premium Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Elevar visualmente o Vantage com tipografia Inter, glassmorphism sutil, micro-glow em valores, skeleton shimmer, Momentum Score, recomendação de analistas e DXY/T10Y no market bar — sem alterar layout.

**Architecture:** Todas as mudanças acontecem em 3 arquivos: `static/index.html` (CSS + JS + HTML inline), `main.py` (2 campos novos em `/api/quote`, 2 símbolos em `/api/market`) e `README.md`. Zero dependências novas além de Google Fonts via CDN.

**Tech Stack:** FastAPI, yfinance, Chart.js 4.4, Vanilla JS, CSS puro, Google Fonts (Inter)

---

## Mapa de arquivos

| Arquivo | O que muda |
|---------|-----------|
| `static/index.html` | `<head>`: link Inter. CSS: body font, shimmer, glassmorphism, glow. JS: `calcMomentumScore()`, `renderDashboard()` (analyst + momentum HTML). CSS: `.momentum-block`, `.analyst-rec` |
| `main.py` | `get_meta()`: 2 campos. `get_quote()`: repassa 2 campos. `get_market()`: 2 símbolos |
| `README.md` | Badges, seções de indicadores, momentum score, estrutura atualizada |

---

## Task 1: Tipografia Inter + Shimmer animation

**Files:**
- Modify: `static/index.html` — `<head>` e bloco CSS (`:root`, `body`, `@keyframes`, `.sk`)

- [ ] **Step 1: Adicionar link do Google Fonts Inter**

Localizar no `static/index.html` a linha:
```html
<title>Vantage</title>
```

Inserir **antes** dela:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

- [ ] **Step 2: Atualizar font-family no body**

Localizar:
```css
body { background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; font-size:14px; line-height:1.5; overflow:hidden; }
```

Substituir por:
```css
body { background:var(--bg); color:var(--text); font-family:'Inter',system-ui,sans-serif; font-size:14px; line-height:1.5; overflow:hidden; }
```

- [ ] **Step 3: Adicionar `tabular-nums` aos elementos de preço**

Localizar:
```css
.watch-price-val { font-size:13px; font-weight:600; }
```

Substituir por:
```css
.watch-price-val { font-size:13px; font-weight:600; font-variant-numeric:tabular-nums; }
```

Localizar:
```css
.mi-price { font-size:12px; font-weight:600; }
```

Substituir por:
```css
.mi-price { font-size:12px; font-weight:600; font-variant-numeric:tabular-nums; letter-spacing:-0.01em; }
```

Localizar:
```css
.quote-price { font-size:28px; font-weight:700; line-height:1.1; }
```

Substituir por:
```css
.quote-price { font-size:28px; font-weight:800; line-height:1.1; font-variant-numeric:tabular-nums; letter-spacing:-0.02em; }
```

Localizar:
```css
.stat-value { font-size:13px; font-weight:700; }
```

Substituir por:
```css
.stat-value { font-size:13px; font-weight:700; font-variant-numeric:tabular-nums; }
```

- [ ] **Step 4: Substituir skeleton pulse por shimmer**

Localizar:
```css
@keyframes sk-pulse { 0%,100%{opacity:.35} 50%{opacity:.7} }
.sk { background:var(--border-subtle); border-radius:5px; animation:sk-pulse 1.6s ease-in-out infinite; }
```

Substituir por:
```css
@keyframes sk-shimmer {
  0%   { background-position:-600px 0 }
  100% { background-position:600px 0 }
}
.sk {
  background:linear-gradient(90deg,var(--border-subtle) 25%,rgba(48,54,61,0.9) 50%,var(--border-subtle) 75%);
  background-size:1200px 100%;
  border-radius:5px;
  animation:sk-shimmer 1.5s linear infinite;
}
```

- [ ] **Step 5: Verificar no browser**

Iniciar servidor: `uvicorn main:app --reload`

Abrir `http://localhost:8000`. Verificar:
- Fonte Inter carregada (textos mais nítidos, sem serifa)
- Skeleton mostra efeito deslizante (não piscada)
- Números na watchlist alinhados verticalmente

- [ ] **Step 6: Commit**

```bash
git add static/index.html
git commit -m "style: Inter font + tabular-nums + skeleton shimmer"
```

---

## Task 2: Glassmorphism nos cards + Micro-glow em valores

**Files:**
- Modify: `static/index.html` — CSS (`.quote-card`, `.chart-panel`, `.pos`, `.neg`, `.watch-chg`)

- [ ] **Step 1: Aplicar glassmorphism no quote-card**

Localizar:
```css
.quote-card {
  background:var(--surface);
  border:1px solid var(--border-subtle);
  border-radius:12px;
  padding:18px 22px;
}
```

Substituir por:
```css
.quote-card {
  background:rgba(22,27,34,0.88);
  backdrop-filter:blur(12px);
  -webkit-backdrop-filter:blur(12px);
  border:1px solid var(--border-subtle);
  border-top-color:rgba(255,255,255,0.07);
  border-radius:12px;
  padding:18px 22px;
}
```

- [ ] **Step 2: Aplicar glassmorphism no chart-panel**

Localizar:
```css
.chart-panel { background:var(--surface); border:1px solid var(--border-subtle); border-radius:12px; padding:14px 18px; }
```

Substituir por:
```css
.chart-panel { background:rgba(22,27,34,0.88); backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); border:1px solid var(--border-subtle); border-top-color:rgba(255,255,255,0.07); border-radius:12px; padding:14px 18px; }
```

- [ ] **Step 3: Adicionar micro-glow em .pos e .neg**

Localizar:
```css
.pos { color:var(--green); }
.neg { color:var(--red); }
```

Substituir por:
```css
.pos { color:var(--green); text-shadow:0 0 18px rgba(63,185,80,0.38); transition:text-shadow 0.3s ease; }
.neg { color:var(--red); text-shadow:0 0 18px rgba(248,81,73,0.38); transition:text-shadow 0.3s ease; }
```

- [ ] **Step 4: Verificar no browser**

Carregar qualquer ticker (ex: AAPL). Verificar:
- `.quote-card` tem bordas com leve brilho no topo (highlight de vidro)
- Valor do preço positivo tem glow verde sutil, negativo tem glow vermelho
- Sidebar permanece sem glassmorphism (correto — é sólida)

- [ ] **Step 5: Commit**

```bash
git add static/index.html
git commit -m "style: glassmorphism on cards + micro-glow on pos/neg values"
```

---

## Task 3: Backend — Analyst Recommendation em /api/quote

**Files:**
- Modify: `main.py` — função `get_meta()` e `get_quote()`

- [ ] **Step 1: Adicionar campos em get_meta()**

Localizar o bloco `meta = {` dentro do `try` de `get_meta()` (linha ~70):
```python
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
```

Substituir por:
```python
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
            "analyst_recommendation": info.get("recommendationKey"),
            "num_analyst_opinions": info.get("numberOfAnalystOpinions"),
        }
```

- [ ] **Step 2: Atualizar o bloco except de get_meta() com os novos campos**

Localizar o bloco `except Exception:` em `get_meta()`:
```python
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
```

Substituir por:
```python
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
            "analyst_recommendation": None,
            "num_analyst_opinions": None,
        }
```

- [ ] **Step 3: Repassar campos no response de get_quote()**

Dentro de `get_quote()`, localizar a linha:
```python
            "52w_low": clean(fi_get(fi, "year_low")),
```

Adicionar após ela:
```python
            "analyst_recommendation": meta.get("analyst_recommendation"),
            "num_analyst_opinions": meta.get("num_analyst_opinions"),
```

- [ ] **Step 4: Verificar via curl**

Com o servidor rodando:
```bash
curl http://localhost:8000/api/quote/AAPL | python -m json.tool | grep -E "analyst|opinions"
```

Saída esperada (valores variam):
```json
"analyst_recommendation": "buy",
"num_analyst_opinions": 38
```

Para um ticker sem analistas (ex: índice):
```bash
curl http://localhost:8000/api/quote/%5EGSPC | python -m json.tool | grep -E "analyst|opinions"
```

Saída esperada:
```json
"analyst_recommendation": null,
"num_analyst_opinions": null
```

- [ ] **Step 5: Commit**

```bash
git add main.py
git commit -m "feat: add analyst_recommendation + num_analyst_opinions to /api/quote"
```

---

## Task 4: Backend — DXY e Treasury 10Y no /api/market

**Files:**
- Modify: `main.py` — dict `symbols` dentro de `get_market()`

- [ ] **Step 1: Adicionar DXY e T10Y ao dict symbols**

Localizar em `get_market()`:
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

Substituir por:
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
        "DX-Y.NYB": "DXY",
        "^TNX":     "T10Y",
    }
```

- [ ] **Step 2: Verificar via curl**

```bash
curl http://localhost:8000/api/market | python -m json.tool | grep -A3 -E '"DXY"|"T10Y"'
```

Saída esperada (valores variam):
```json
{
    "symbol": "DX-Y.NYB",
    "label": "DXY",
    "price": 104.23,
    "change_pct": -0.15
},
{
    "symbol": "^TNX",
    "label": "T10Y",
    "price": 4.52,
    "change_pct": 0.44
}
```

- [ ] **Step 3: Confirmar no browser**

Recarregar `http://localhost:8000` e verificar que o market bar agora exibe `DXY` e `T10Y` ao final da barra (pode precisar de scroll horizontal).

- [ ] **Step 4: Commit**

```bash
git add main.py
git commit -m "feat: add DXY and T10Y (Treasury 10Y) to market bar"
```

---

## Task 5: Frontend — Exibir Recomendação de Analistas

**Files:**
- Modify: `static/index.html` — CSS (`.analyst-rec`) + JS (`renderDashboard()`)

- [ ] **Step 1: Adicionar CSS para .analyst-rec**

Localizar no bloco CSS:
```css
.quote-ts .refresh-btn:hover { color:var(--accent); border-color:var(--accent); }
```

Adicionar **após** essa linha:
```css
.analyst-rec { display:flex; align-items:center; gap:8px; margin-top:8px; }
.rec-count { font-size:11px; color:var(--muted); }
```

- [ ] **Step 2: Adicionar mapeamento de recomendação no JS**

Localizar no JS (logo após as declarações de `const C = {` ou antes da função `renderDashboard`):
```javascript
const C = {
```

Adicionar **antes** de `const C = {`:
```javascript
const REC_MAP = {
  strong_buy:  { label:'Compra Forte', cls:'green' },
  buy:         { label:'Compra',       cls:'green' },
  hold:        { label:'Neutro',       cls:'yellow' },
  sell:        { label:'Venda',        cls:'red' },
  strong_sell: { label:'Venda Forte',  cls:'red' },
};
```

- [ ] **Step 3: Inserir o bloco de analistas no HTML do renderDashboard**

Localizar dentro da função `renderDashboard`, o trecho:
```javascript
          <div class="quote-ts">
            Atualizado ${now}
            <button class="refresh-btn" onclick="forceRefresh()">↻</button>
          </div>
        </div>
```

Substituir por:
```javascript
          <div class="quote-ts">
            Atualizado ${now}
            <button class="refresh-btn" onclick="forceRefresh()">↻</button>
          </div>
          ${(() => {
            const rec = REC_MAP[quote.analyst_recommendation];
            if (!rec) return '';
            const count = quote.num_analyst_opinions ? ` · ${quote.num_analyst_opinions} analistas` : '';
            return `<div class="analyst-rec">
              <span class="pill ${rec.cls}">● ${rec.label}</span>
              <span class="rec-count">${count}</span>
            </div>`;
          })()}
        </div>
```

- [ ] **Step 4: Verificar no browser**

Carregar AAPL ou MSFT (têm cobertura de analistas). Verificar:
- Badge colorido aparece abaixo do horário de atualização (ex: `● Compra`)
- Conta de analistas aparece em muted ao lado (ex: `· 38 analistas`)
- Carregar `^GSPC` (índice sem analistas): badge **não** aparece

- [ ] **Step 5: Commit**

```bash
git add static/index.html
git commit -m "feat: analyst recommendation badge in quote card"
```

---

## Task 6: Frontend — Momentum Score

**Files:**
- Modify: `static/index.html` — CSS (`.momentum-block`) + JS (`calcMomentumScore()`, `renderDashboard()`)

- [ ] **Step 1: Adicionar CSS do Momentum Score**

Localizar:
```css
.rec-count { font-size:11px; color:var(--muted); }
```

Adicionar **após**:
```css
.momentum-block { background:var(--bg); border-radius:10px; padding:12px 16px; }
.momentum-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.momentum-title { font-size:11px; font-weight:700; color:var(--muted); letter-spacing:.05em; text-transform:uppercase; }
.momentum-label-text { font-size:12px; font-weight:700; }
.momentum-track {
  position:relative; height:6px;
  background:linear-gradient(90deg, var(--red) 0%, var(--border-subtle) 50%, var(--green) 100%);
  border-radius:6px; margin-bottom:8px;
}
.momentum-pointer {
  position:absolute; top:50%; width:12px; height:12px;
  background:var(--text); border-radius:50%;
  transform:translate(-50%, -50%);
  box-shadow:0 0 6px rgba(0,0,0,.6);
  transition:left 0.4s ease;
}
.momentum-signals { font-size:10px; color:var(--muted); }
```

- [ ] **Step 2: Adicionar função calcMomentumScore no JS**

Localizar:
```javascript
const REC_MAP = {
```

Adicionar **antes**:
```javascript
function calcMomentumScore(indicators) {
  const data = indicators.data;
  const last = data.filter(d => d.rsi != null).slice(-1)[0];
  const prev = data.filter(d => d.macd_hist != null).slice(-2)[0];
  if (!last) return 0;

  let score = 0;

  // RSI: <35 bullish, >65 bearish
  if (last.rsi < 35) score += 1;
  else if (last.rsi > 65) score -= 1;

  // MACD: histograma positivo e crescendo vs negativo e caindo
  if (last.macd_hist != null && prev?.macd_hist != null) {
    if (last.macd_hist > 0 && last.macd_hist >= prev.macd_hist) score += 1;
    else if (last.macd_hist < 0 && last.macd_hist <= prev.macd_hist) score -= 1;
  }

  // Bollinger: preço próximo da banda inferior (bullish) ou superior (bearish)
  if (last.close != null && last.bb_lower != null && last.bb_upper != null) {
    if (last.close <= last.bb_lower * 1.05) score += 1;
    else if (last.close >= last.bb_upper * 0.95) score -= 1;
  }

  return Math.max(-3, Math.min(3, score));
}

function momentumLabel(score) {
  if (score >= 3)  return ['Forte Alta', 'pos'];
  if (score > 0)   return ['Alta', 'pos'];
  if (score === 0)  return ['Neutro', 'neu'];
  if (score <= -3) return ['Forte Baixa', 'neg'];
  return ['Baixa', 'neg'];
}
```

- [ ] **Step 3: Inserir bloco HTML do Momentum Score no renderDashboard**

Localizar dentro de `renderDashboard`, o trecho que abre o price+volume chart:
```javascript
    <!-- Price + Volume Chart -->
    <div class="chart-panel">
```

Inserir **antes** dele:
```javascript
    <!-- Momentum Score -->
    ${(() => {
      const score = calcMomentumScore(indicators);
      const [label, cls] = momentumLabel(score);
      const pct = 50 + (score / 3) * 50;
      return `<div class="momentum-block">
        <div class="momentum-header">
          <span class="momentum-title">Momentum</span>
          <span class="momentum-label-text ${cls}">${label}</span>
        </div>
        <div class="momentum-track">
          <div class="momentum-pointer" style="left:${pct.toFixed(1)}%"></div>
        </div>
        <div class="momentum-signals">RSI · MACD · Bollinger Bands</div>
      </div>`;
    })()}

    <!-- Price + Volume Chart -->
    <div class="chart-panel">
```

- [ ] **Step 4: Verificar no browser**

Carregar qualquer ticker com histórico (ex: AAPL, PETR4.SA, BTC-USD). Verificar:
- Bloco "MOMENTUM" aparece entre stats grid e gráfico de preço
- Barra gradiente (vermelho → cinza → verde) com ponteiro branco posicionado
- Label colorido à direita (ex: `Alta` em verde, `Neutro` em cinza)
- Ponteiro anima suavemente ao trocar de ticker

- [ ] **Step 5: Commit**

```bash
git add static/index.html
git commit -m "feat: momentum score block (RSI + MACD + Bollinger)"
```

---

## Task 7: README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Reescrever README.md**

Substituir o conteúdo completo do arquivo por:

```markdown
# Vantage

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black?logo=vercel)
![yfinance](https://img.shields.io/badge/Data-Yahoo%20Finance-purple)

Dashboard de acompanhamento de ativos financeiros com cotações em tempo real, gráficos interativos, indicadores técnicos e Momentum Score.

**Stack:** FastAPI + yfinance + ta + Chart.js (frontend vanilla JS, zero dependências de build)

---

## Demo

> [Link do deploy na Vercel] ← substitua após o deploy

---

## Funcionalidades

- Cotações em tempo real — ações BR/EUA, cripto, índices
- Market bar com S&P 500, NASDAQ, Ibovespa, VIX, Bitcoin, Ouro, WTI, EUR/USD, **DXY** e **Treasury 10Y**
- Histórico de preço + volume com seletor de período (1M → 2A)
- Indicadores técnicos: RSI 14, MACD (12/26/9), SMA 20/50, EMA 9, Bollinger Bands
- **Momentum Score** — leitura combinada de RSI + MACD + Bollinger em uma barra visual
- **Recomendação de analistas** — consenso (Compra / Neutro / Venda) com contagem de analistas
- Watchlist persistente via `localStorage`
- Browse por categoria (EUA, Brasil, Cripto, Índices)
- Busca de ativos pelo nome ou ticker
- Cache TTL em memória (cotação: 60s · histórico/indicadores: 300s · mercado: 120s)
- GZip middleware para respostas comprimidas

---

## Indicadores Técnicos

| Indicador | O que mede | Como interpretar |
|-----------|-----------|-----------------|
| **RSI 14** | Força relativa do preço nos últimos 14 dias | >70: sobrecomprado (possível queda) · <30: sobrevendido (possível alta) |
| **MACD (12,26,9)** | Diferença entre médias exponenciais rápida e lenta | Histograma positivo e crescendo = momentum de alta |
| **Bollinger Bands** | Volatilidade em torno da SMA 20 | Preço próximo da banda superior = extensão de alta; inferior = extensão de baixa |
| **SMA 20/50** | Média aritmética dos últimos 20/50 fechamentos | SMA 20 cruzando SMA 50 para cima = sinal de tendência |
| **EMA 9** | Média exponencial de curto prazo | Mais reativa que SMA — útil para timing de entrada |

---

## Momentum Score

O Momentum Score combina 3 sinais independentes em uma leitura de **-3 a +3**:

| Sinal | Bullish (+1) | Bearish (-1) | Neutro (0) |
|-------|-------------|-------------|-----------|
| RSI | < 35 | > 65 | 35–65 |
| MACD | Histograma positivo e crescendo | Negativo e caindo | Outros |
| Bollinger | Preço ≤ banda inferior +5% | Preço ≥ banda superior -5% | Outros |

**Interpretação:** +3 = Forte Alta · +1/+2 = Alta · 0 = Neutro · -1/-2 = Baixa · -3 = Forte Baixa

> O score é indicativo, não uma recomendação de investimento.

---

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Serve o frontend |
| `GET` | `/api/quote/{ticker}` | Cotação atual + métricas fundamentalistas + recomendação de analistas |
| `GET` | `/api/quotes?tickers=A,B` | Cotações em batch (máx 20 tickers) |
| `GET` | `/api/history/{ticker}` | Histórico OHLCV (`?period=3mo&interval=1d`) |
| `GET` | `/api/indicators/{ticker}` | RSI, MACD, SMA, EMA, Bollinger (`?period=6mo`) |
| `GET` | `/api/market` | Resumo dos principais índices e ativos globais |
| `GET` | `/api/search/{query}` | Busca de ativos por nome ou ticker |

Períodos válidos: `1d 5d 1mo 3mo 6mo 1y 2y 5y`  
Intervalos válidos: `1m 5m 15m 30m 60m 1d 1wk 1mo`

Documentação interativa: `/docs` (Swagger) · `/redoc`

---

## Execução local

**Requisitos:** Python 3.11+

```bash
# 1. Clonar o repositório
git clone <url-do-repo>
cd vantage

# 2. Criar e ativar ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Iniciar o servidor
uvicorn main:app --reload
```

Acesse: [http://localhost:8000](http://localhost:8000)

Porta alternativa: `uvicorn main:app --reload --port 8080`  
Rede local: `uvicorn main:app --host 0.0.0.0 --port 8000`

---

## Deploy na Vercel

**Requisitos:** conta na [Vercel](https://vercel.com) + Vercel CLI (`npm i -g vercel`)

```bash
vercel
# Wizard: framework → Other · build command → vazio · output → vazio
```

**Variáveis de ambiente:** nenhuma — usa apenas Yahoo Finance (público).

**Limitações no plano gratuito:**
- Timeout de função: 10s (considere Pro para análises demoradas)
- Cold start: ~2–3s na primeira request (yfinance + pandas são pesados)

---

## Estrutura do projeto

```
vantage/
├── main.py          # API FastAPI — rotas, cache, lógica de dados
├── requirements.txt # Dependências Python
├── vercel.json      # Configuração de deploy Vercel
└── static/
    └── index.html   # Frontend completo (HTML + CSS + JS)
```

## Dependências

| Pacote | Versão | Função |
|--------|--------|--------|
| fastapi | 0.115.0 | Framework web ASGI |
| uvicorn | 0.30.6 | Servidor ASGI |
| yfinance | ≥1.3.0 | Dados de mercado (Yahoo Finance) |
| pandas | 2.2.3 | Manipulação de séries temporais |
| ta | 0.11.0 | Indicadores técnicos (RSI, MACD, Bollinger) |
| python-multipart | 0.0.12 | Suporte a form data |
```

- [ ] **Step 2: Verificar renderização**

Abrir o arquivo em qualquer visualizador Markdown (VS Code, GitHub, etc.) e confirmar:
- Badges no topo renderizam corretamente
- Tabela de indicadores está alinhada
- Tabela de Momentum Score está alinhada
- Código blocks com syntax highlighting

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: comprehensive README with badges, indicators guide, momentum score"
```

---

## Self-Review — Cobertura da Spec

| Requisito da Spec | Task |
|-------------------|------|
| Inter font + tabular-nums | Task 1 |
| font-weight 700→800 no quote-price | Task 1 |
| Skeleton shimmer (não pulse) | Task 1 |
| Glassmorphism .quote-card | Task 2 |
| Glassmorphism .chart-panel | Task 2 |
| Micro-glow .pos/.neg com transition | Task 2 |
| analyst_recommendation em get_meta() | Task 3 |
| analyst_recommendation em get_quote() | Task 3 |
| DXY no market bar | Task 4 |
| T10Y no market bar | Task 4 |
| Badge analistas no quote card | Task 5 |
| calcMomentumScore() | Task 6 |
| Bloco visual momentum com barra | Task 6 |
| README badges | Task 7 |
| README seção indicadores | Task 7 |
| README seção momentum score | Task 7 |
| README estrutura atualizada (vercel.json) | Task 7 |
| Fix: cd stockboard-api → cd vantage | Task 7 |
