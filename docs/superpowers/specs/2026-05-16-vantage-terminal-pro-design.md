# Vantage — Terminal Pro (UI/UX Transformation)

**Data:** 2026-05-16
**Escopo:** Redesenho visual marcante + reorganização de informação + 4 features novas + responsividade
**Arquivos:** `static/index.html` (CSS/render/interações), `main.py` (1 endpoint aditivo)
**Restrição-chave:** nenhuma informação existente é removida — apenas reorganizada.

---

## 1. Sistema visual

### Tipografia
- `Inter` (400/500/600/700/800) — texto de UI.
- `JetBrains Mono` (400/500/600/700) — **todo dado numérico e ticker**: preços, variações,
  stats, eixos de gráfico, range, sparkline labels. Assinatura "terminal".
- Variável CSS `--mono` aplicada via classe utilitária `.num` e nos seletores numéricos.

### Paleta (camadas mais profundas)
| Token | Antes | Depois |
|---|---|---|
| `--bg` | `#0d1117` | `#080a0d` |
| `--surface` | `#161b22` | `#0f1318` |
| `--surface2` | `#1c2128` | `#161b22` |
| `--border` | `#30363d` | `#272d36` |
| `--border-subtle` | `#21262d` | `#1b212a` |

Verde `#3fb950` / vermelho `#f85149` mantidos. Gradiente azul→roxo (`#58a6ff`→`#bc8cff`)
permanece como marca. Espaçamento numa escala de 8px (4/8/12/16/24).

### Microinterações
- **Flash de preço**: ao atualizar preço ao vivo (refresh 60s + force refresh), a célula
  pisca verde/vermelho (`@keyframes flash`, ~600ms) conforme a direção da mudança.
- Sparkline desenha com animação de stroke.
- Hover nos cards: elevação sutil (`box-shadow` + `translateY(-1px)`).
- Transições suaves em todos os estados interativos.

## 2. Reorganização da informação

### Cabeçalho do ativo (quote card)
Mantém: ticker · exchange · currency, nome, setor, preço, variação, timestamp, refresh.
**Adiciona embutido:**

- **Barra de range 52 semanas** — trilho horizontal mín→máx; marcador na posição
  `(price - low) / (high - low)`. Pontas rotuladas com `52w_low` e `52w_high`
  (esses números saem do grid de stats e viram rótulos da barra — informação preservada).
- **Bloco de analistas** — pill de recomendação (REC_MAP existente) + `target_price`
  com **% upside/downside** = `(target - price) / price * 100`, e mini-barra
  posicionando preço atual vs alvo. Contagem de analistas mantida.
  Se `target_price` ausente → bloco omitido (como hoje).

### Stats agrupados (substitui grid plano de 16 células)
Três seções, cada uma com subtítulo + grid próprio:

- **Negociação**: Abertura, Máxima, Mínima, Volume, Vol Méd 10d
- **Valuation**: Market Cap, P/L, P/VP, EPS TTM, Receita TTM
- **Risco & Retorno**: Beta, RSI 14 (+ pill sobrecomprado/sobrevendido)

`52w_high` / `52w_low` migram para a barra de range. `target_price` e
`dividend_yield` migram para o bloco de analistas (Div. Yield exibido junto).
Nenhum campo é descartado — todos os 16 indicadores continuam visíveis.

### Mantidos sem mudança estrutural
Momentum block, 4 gráficos (Preço+Volume, RSI, MACD, Bollinger), watchlist,
browse, search, market bar, estados de loading/erro/vazio.

## 3. Feature: Sparkline na watchlist

### Backend — `GET /api/sparklines`
```
GET /api/sparklines?tickers=AAPL,MSFT,...
→ { "sparklines": [ { "ticker": "AAPL", "closes": [f, ...], "change_pct": f }, ... ] }
```
- Aceita até 20 tickers (mesmo limite de `/quotes`).
- Período `1mo`, intervalo `1d` (~22 pontos). Reusa `yf.Ticker().history`.
- Cache TTL 300s por ticker (chave `spark:{ticker}`), padrão dos endpoints existentes.
- Erro por ticker → entrada omitida (não derruba o batch). ThreadPoolExecutor como `/quotes`.
- Read-only, sem auth, sem dado de usuário — consistente com a superfície atual.

### Frontend
- Cada `.watch-item` ganha um `<canvas>` de sparkline (~64×22px) entre nome e preço.
- Cor pela tendência (`closes[last] >= closes[0]` → verde, senão vermelho).
- Carregado após `renderWatchlist`, em batch único; falha → sparkline simplesmente ausente.

## 4. Responsividade

- Remover `overflow:hidden` global do `body` em telas pequenas.
- **≥1025px**: grid atual (sidebar 272px fixa).
- **≤1024px**: sidebar vira **drawer** deslizante da esquerda; botão hambúrguer no header;
  overlay escurece o conteúdo; fecha ao selecionar ativo ou clicar fora.
- **≤640px**: `indicators-grid` colapsa para 1 coluna; `quote-top` empilha; grids de stats
  com `minmax` menor; market bar continua com scroll horizontal.

## 5. Não-objetivos (YAGNI)

- Sem framework JS — segue vanilla, single-file.
- Sem novas dependências de backend.
- Sem persistência server-side, sem auth, sem login.
- Sem mudança nos endpoints existentes (`/quote`, `/quotes`, `/history`, `/indicators`,
  `/market`, `/search`).

## 6. Verificação

- App sobe (`uvicorn main:app`), `/` serve o HTML.
- `/api/sparklines?tickers=AAPL,MSFT` retorna closes válidos.
- Selecionar ativo: cabeçalho com barra 52s, bloco de analistas, 3 grupos de stats,
  momentum, 4 gráficos — todos os 16 indicadores presentes.
- Watchlist com sparklines coloridos.
- Flash de preço visível no refresh.
- Layout íntegro em 1440px, 1024px, 768px e 375px.
