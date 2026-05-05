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
| **RSI 14** | Força relativa do preço nos últimos 14 dias | >70: sobrecomprado · <30: sobrevendido |
| **MACD (12,26,9)** | Diferença entre médias exponenciais rápida e lenta | Histograma positivo e crescendo = momentum de alta |
| **Bollinger Bands** | Volatilidade em torno da SMA 20 | Preço na banda superior = extensão de alta; inferior = extensão de baixa |
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
    ├── index.html   # Frontend completo (HTML + CSS + JS)
    └── favicon.svg  # Ícone da aba do navegador
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
