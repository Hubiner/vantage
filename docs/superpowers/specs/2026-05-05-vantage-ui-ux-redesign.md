# Vantage — UI/UX Premium Refinement + Content Additions

**Data:** 2026-05-05  
**Escopo:** Melhorias visuais (sem alterar layout) + adição de conteúdo relevante + README  
**Abordagem aprovada:** Incrementalista — alterações em `static/index.html` e `main.py`

---

## 1. Tipografia

- Importar **Inter** (400/500/600/700) via Google Fonts no `<head>`
- Aplicar como `font-family` primária em `:root`, com `system-ui` como fallback
- Elementos numéricos (`.quote-price`, `.watch-price-val`, `.mi-price`, `.stat-value`) ganham:
  - `font-variant-numeric: tabular-nums`
  - `letter-spacing: -0.02em`
- `.quote-price` sobe de `font-weight: 700` → `800`

## 2. Glassmorphism (sutil)

Aplicar em `.quote-card` e `.chart-panel`:
- `background: rgba(22,27,34,0.85)`
- `backdrop-filter: blur(12px)`
- `border` superior com `rgba(255,255,255,0.06)` (highlight de vidro — `border-top: 1px solid rgba(255,255,255,0.06)`)
- `border` lateral/inferior mantém `var(--border-subtle)`
- `border-radius` permanece 12px

## 3. Micro-glow em valores positivos/negativos

- `.pos`: adiciona `text-shadow: 0 0 20px rgba(63,185,80,0.35)`
- `.neg`: adiciona `text-shadow: 0 0 20px rgba(248,81,73,0.35)`
- Ambos com `transition: text-shadow 0.3s ease`
- Aplicar também em `.watch-chg` e `.quote-change`

## 4. Skeleton shimmer

Substituir `@keyframes sk-pulse` (opacity fade) por shimmer com gradiente deslizante:

```css
@keyframes sk-shimmer {
  0%   { background-position: -400px 0 }
  100% { background-position: 400px 0 }
}
.sk {
  background: linear-gradient(90deg,
    var(--border-subtle) 25%,
    rgba(48,54,61,0.9) 50%,
    var(--border-subtle) 75%
  );
  background-size: 800px 100%;
  animation: sk-shimmer 1.4s linear infinite;
}
```

## 5. Momentum Score (frontend)

**Posição:** Novo bloco entre `.stats-grid` e o primeiro `.chart-panel` (price chart).

**Lógica de cálculo** (usa dados de `indicators` já carregados):

| Sinal | Condição Bullish (+1) | Condição Bearish (-1) | Neutro (0) |
|-------|----------------------|----------------------|-----------|
| RSI | < 35 | > 65 | 35–65 |
| MACD | hist > 0 e crescendo | hist < 0 e caindo | outros |
| Bollinger | preço ≤ BB inferior + 5% | preço ≥ BB superior - 5% | outros |

Score final: soma dos 3 sinais → mapeado para label:
- +3 → `Forte Alta` (verde)
- +1/+2 → `Alta` (verde claro)
- 0 → `Neutro` (muted)
- -1/-2 → `Baixa` (vermelho claro)
- -3 → `Forte Baixa` (vermelho)

**Visual:** barra horizontal (`height: 6px`) com gradiente `red → gray → green`, ponteiro circular posicionado com `left: calc(50% + score * 16.67%)`. Label acima da barra à direita.

**Container:**
```html
<div class="momentum-block">
  <div class="momentum-label">Momentum <span id="momentum-text">Neutro</span></div>
  <div class="momentum-bar"><div class="momentum-pointer" id="momentumPointer"></div></div>
  <div class="momentum-signals">RSI · MACD · Bollinger</div>
</div>
```

## 6. Recomendação de Analistas

**Backend — `main.py`:**

Adicionar 2 campos ao response de `/api/quote/{ticker}` via `get_meta()`:
- `analyst_recommendation`: `info.get("recommendationKey")` → string (`"buy"`, `"hold"`, `"sell"`, `"strong_buy"`, `"strong_sell"`) ou `None`
- `num_analyst_opinions`: `info.get("numberOfAnalystOpinions")` → int ou `None`

Mapeamento para exibição:
```python
REC_LABEL = {
    "strong_buy": ("Compra Forte", "green"),
    "buy": ("Compra", "green"),
    "hold": ("Neutro", "yellow"),
    "sell": ("Venda", "red"),
    "strong_sell": ("Venda Forte", "red"),
}
```
Os campos `rec_label` e `rec_color` entram no response (evita lógica de mapeamento no frontend).

**Frontend — quote card:**

Abaixo do `.quote-ts` (linha do horário de atualização), adicionar:
```html
<div class="analyst-rec" id="analystRec">
  <!-- renderizado se analyst_recommendation != null -->
  <span class="pill green">● Compra</span>
  <span class="rec-count">38 analistas</span>
</div>
```

## 7. Market Bar — DXY e Treasury 10Y

**Backend — `main.py`:**

Adicionar ao dict `symbols` em `get_market()`:
```python
"DX-Y.NYB": "DXY",
"^TNX":     "T10Y",
```

Nenhuma mudança no frontend necessária — o market bar já renderiza via loop.

**Nota:** `^TNX` retorna o yield em pontos (ex: `45.2` = 4.52%). Adicionar divisão por 10 no label: `f"{price/10:.2f}%"` para o campo `price` exibido.

## 8. README.md

**Adições:**
- Badges no topo: Python 3.11+, FastAPI 0.115, Vercel, yfinance
- Seção **Demo** com placeholder `[Link do deploy]` e instrução de screenshot
- Atualizar **Funcionalidades** com: Momentum Score, Recomendação de analistas, DXY e T10Y
- Nova seção **Indicadores Técnicos** — 3 linhas por indicador (RSI, MACD, Bollinger, SMA, EMA)
- Nova seção **Momentum Score** — explicação da lógica dos 3 sinais
- Atualizar **Estrutura** incluindo `vercel.json`
- Corrigir `cd stockboard-api` → `cd vantage`

---

## Arquivos modificados

| Arquivo | Tipo de mudança |
|---------|----------------|
| `static/index.html` | CSS (tipografia, glassmorphism, glow, shimmer) + JS (momentum score, analyst rec render) + HTML (novos blocos) |
| `main.py` | `get_meta()` + 2 campos em `/api/quote` + 2 símbolos em `/api/market` |
| `README.md` | Conteúdo expandido |

## Restrições

- Zero mudança no layout (grid, posições, sidebar, tamanho dos painéis)
- Zero dependências novas (Inter via CDN Google Fonts, sem npm)
- Breaking change: nenhuma — apenas campos adicionais nos responses
- Compatibilidade Vercel: mantida (`static/index.html` continua sendo o único arquivo frontend)
