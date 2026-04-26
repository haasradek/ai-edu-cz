# Session State — AI-EDU-CZ

> Tento soubor se aktualizuje na konci každého sessionu. Při zahájení nového sessionu ho Claude přečte jako první.

---

## Poslední update
**Datum:** 2026-04-26
**Session číslo:** 2
**Claude model:** claude-sonnet-4-6

---

## Co bylo uděláno v tomto sessionu

### Infrastruktura (Fáze A — dokončena)
- **FastAPI migrace** — `server/main.py` + `server/static/index.html` (nahradil starý `dashboard.py`)
- **SQLite databáze** — `database.py` (tabulky: `items`, `generated`, `published`)
- **RSS agent** — `agenti/rss_agent.py` (10 feedů, AI keyword filtr, tag detekce)
- **`start.py`** — auto-kill portu 8765, jednoduchý restart jedním příkazem

### Dashboard — nové funkce
- **Tabová navigace** — Přehled / Feed / GitHub / Session
- **System Status** — animovaný indikátor uprostřed headeru (zelený/oranžový/červený)
- **Feed sekce** — 112 článků, řazení od nejnovějšího, filtr dle zdroje + stavu
- **Tagy** — Claude, ChatGPT, Gemini, Grok, Llama, Copilot, Mistral, Perplexity, Agenti, LLM
- **Tag filtr** — klikatelné pilulky, okamžité filtrování feedu
- **Polling** — "Stáhnout novinky" čeká na dokončení agenta místo pevného timeoutu

### RSS feedy (funkční)
| Zdroj | Stav |
|-------|------|
| OpenAI Blog | ✅ (filter_ai=True) |
| TechCrunch AI | ✅ |
| VentureBeat AI | ✅ |
| The Verge AI | ✅ |
| Google News CZ | ✅ (AI klíčová slova v dotazu) |
| Google News SK | ✅ (AI klíčová slova v dotazu) |
| Lupa.cz | ✅ (filter_ai=True) |
| Root.cz | ✅ (filter_ai=True) |
| Anthropic Blog | ❌ (RSS neexistuje) |
| HackerNews AI | ❌ (nestabilní) |

---

## Schválená architektura platformy (nezměněno)

### Databáze
- **SQLite** — `data/aieducz.db`
- Tabulky: `items`, `generated`, `published`

### Pipeline (co je hotové → co zbývá)
```
RSS feeds → SQLite DB ✅
                ↓
        Feed v dashboardu ✅
                ↓
        Tlačítko "Zpracovat" ⏳ (pipeline zatím placeholder)
                ↓
        Claude API → generování obsahu ⏳
                ↓
        Fact-check agent ⏳
                ↓
        Výstupy: článek CZ, Twitter, Instagram, YouTube, Podcast ⏳
```

### Jazyk obsahu
- **DB**: articles v originálním jazyce (EN/CZ)
- **Výstupy po "Zpracovat"**: vždy česky (Claude API přeloží/přepíše)

---

## Aktuální fáze projektu

**Fáze:** 2 — Generovací pipeline (napojení Claude API)
**Priorita:** Zprovoznit tlačítko "Zpracovat" — end-to-end od článku k českému obsahu

---

## Příští kroky — pro nový session (Fáze B)

1. **Generovací pipeline** — `agenti/content_agent.py` (Claude API)
   - Vstup: `item_id` z DB
   - Výstup: článek CZ, Twitter thread, Instagram post, YouTube scénář
   - Uložení do tabulky `generated`
2. **Fact-check agent** — `agenti/factcheck_agent.py`
   - DuckDuckGo search + Claude → % skóre + zdroje
3. **Napojit tlačítko "Zpracovat"** v dashboardu
   - POST `/api/process/{item_id}` → spustí content_agent
   - Zobrazit výsledky (generated content) pod článkem
4. **Výsledky v dashboardu** — zobrazení vygenerovaného obsahu, možnost kopírovat
5. **Commit + push** všech změn z tohoto sessionu na GitHub

---

## Otevřené otázky pro budoucí session

- Kdy přejít na publikaci přes API (až bude obsah pravidelný a ověřený)?
- Kdy přidat Supabase (až bude potřeba cloud přístup)?
- Doménové jméno pro web (ai-edu.cz nebo jiné)?
- Přidat Windows Task Scheduler pro automatické spouštění RSS agenta?

---

## Soubory projektu (aktuální stav)

```
ai-edu-cz/
├── CLAUDE.md                          ✅
├── SESSION.md                         ✅ (tento soubor)
├── PROGRESS.md                        ✅
├── start.py                           ✅ (auto-kill port, jednoduchý start)
├── database.py                        ✅ (SQLite — items, generated, published)
├── dashboard.py                       ⚠ (starý, nahrazen FastAPI — lze smazat)
├── .env                               ✅ (Anthropic API key)
├── .env.example                       ✅
├── .gitignore                         ✅
├── data/
│   └── aieducz.db                     ✅ (112 článků)
├── server/
│   ├── main.py                        ✅ (FastAPI backend)
│   └── static/index.html              ✅ (dashboard — Feed, tagy, filtry, status)
├── agenti/
│   └── rss_agent.py                   ✅ (10 feedů, AI filtr, tagy)
│   └── content_agent.py               ⏳ (Fáze B)
│   └── factcheck_agent.py             ⏳ (Fáze B)
├── strategie/                         ✅ (5 dokumentů)
├── obsah/modul-1-zaklady/            ✅ (1 lekce)
├── obsah/modul-2 až modul-6/        ⏳ (prázdné, připravené)
├── prompt-knihovna/                   ✅ (emailové šablony)
└── sablony/                           ✅ (Twitter šablona)
```
