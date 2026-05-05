# Vantage

Dashboard de acompanhamento de ativos financeiros com cotações em tempo real, gráficos interativos e indicadores técnicos.

**Stack:** FastAPI + yfinance + ta-lib + Chart.js (frontend vanilla JS, zero dependências de build)

---

## Funcionalidades

- Cotações em tempo real (ações BR/EUA, cripto, índices)
- Histórico de preço + volume com seletor de período
- Indicadores técnicos: RSI, MACD, SMA 20/50, EMA 9, Bollinger Bands
- Watchlist persistente via `localStorage`
- Browse por categoria (EUA, Brasil, Cripto, Índices)
- Busca de ativos pelo nome ou ticker
- Cache TTL em memória (cotação: 60s | histórico/indicadores: 300s | mercado: 120s)

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Serve o frontend |
| `GET` | `/api/quote/{ticker}` | Cotação atual |
| `GET` | `/api/history/{ticker}` | Histórico OHLCV (`?period=3mo&interval=1d`) |
| `GET` | `/api/indicators/{ticker}` | Indicadores técnicos (`?period=6mo`) |
| `GET` | `/api/market` | Resumo dos principais índices |
| `GET` | `/api/search/{query}` | Busca de ativos |

Períodos válidos: `1d 5d 1mo 3mo 6mo 1y 2y 5y`  
Intervalos válidos: `1m 5m 15m 30m 60m 1d 1wk 1mo`

Documentação interativa disponível em `/docs` (Swagger) e `/redoc`.

---

## Execução local

**Requisitos:** Python 3.11+

```bash
# 1. Clonar o repositório
git clone <url-do-repo>
cd stockboard-api

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

Para rodar em porta diferente:
```bash
uvicorn main:app --reload --port 8080
```

Para expor na rede local:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Deploy na Vercel

**Requisitos:** conta na [Vercel](https://vercel.com) + Vercel CLI (`npm i -g vercel`)

```bash
# Na raiz do projeto
vercel

# Seguir o wizard: framework → Other, build command → vazio, output → vazio
```

**Variáveis de ambiente:** nenhuma necessária — o app usa apenas Yahoo Finance (público).

**Limitações no plano gratuito:**
- Timeout de função: 10s padrão (considere Pro se necessário)
- Cold start: ~2-3s na primeira request (yfinance + pandas são pesados)

---

## Estrutura do projeto

```
vantage/
├── main.py          # API FastAPI — rotas, cache, lógica de negócio
├── requirements.txt # Dependências Python
└── static/
    └── index.html   # Frontend completo (HTML + CSS + JS)
```

## Dependências

| Pacote | Versão | Função |
|--------|--------|--------|
| fastapi | 0.115.0 | Framework web |
| uvicorn | 0.30.6 | Servidor ASGI |
| yfinance | ≥1.3.0 | Dados de mercado (Yahoo Finance) |
| pandas | 2.2.3 | Manipulação de séries temporais |
| ta | 0.11.0 | Indicadores técnicos |
| python-multipart | 0.0.12 | Suporte a form data |
