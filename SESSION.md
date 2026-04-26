# Session State — AI-EDU-CZ

> Tento soubor se aktualizuje na konci každého sessionu. Při zahájení nového sessionu ho Claude přečte jako první.

---

## Poslední update
**Datum:** 2026-04-26
**Session číslo:** 1
**Claude model:** claude-sonnet-4-6

---

## Co bylo uděláno v tomto sessionu

### Infrastruktura
- Zahájen projekt AI-EDU-CZ
- Vytvořen CLAUDE.md, celá složková struktura projektu
- Vytvořen GitHub repozitář: https://github.com/haasradek/ai-edu-cz
- Nastaven git + HTTPS push workflow
- Vytvořen dashboard (dashboard.py) — FastAPI migrace plánována
- Implementován security agent (scan před každým pushem)
- Implementován session systém (SESSION.md + save-session flow)
- Nastaven .env systém s Anthropic API klíčem
- Rozšířen .gitignore (klíče, certifikáty, OS soubory)

### Strategické dokumenty
- strategie/vize.md
- strategie/agent-architektura.md
- strategie/obsahovy-plan.md
- strategie/monetizace.md
- strategie/platformy-a-nastroje.md (70+ AI nástrojů ve 13 kategoriích)

### První obsah
- obsah/modul-1-zaklady/01-co-je-ai.md
- prompt-knihovna/prace/email-sablony.md
- sablony/twitter/thread-sablona.md

---

## Schválená architektura platformy (klíčová rozhodnutí)

### Databáze
- **SQLite** — lokální, zdarma, vestavěná v Pythonu
- Supabase odloženo na budoucnost (cloud přístup)
- Tabulky: `items`, `generated`, `published`

### Zdroje dat (všechny zdarma)
- RSS feeds (blog.anthropic.com, openai.com/blog, techcrunch AI, venturebeat AI...)
- Google News RSS
- HackerNews API (bez klíče)
- Twitter/nitter RSS — bonus, nestabilní, ale zdarma
- **trafilatura** Python lib — stahuje plný text článků z URL (zdarma)
- **Tavily** free tier (1000/měs) — pro vlastní témata zadaná manuálně

### Sběr dat
- Automatický denně (Windows Task Scheduler nebo n8n)
- Deduplication přes URL hash
- Archiv v dashboardu — lze zpracovat i 10 dní staré téma
- Dva vstupní body: automatické novinky + vlastní téma od Radka

### Framework
- **FastAPI** (migrace z http.server) — Python backend
- Separátní HTML/CSS/JS soubory (ne embedded v Pythonu)

### Generování obsahu
- Claude API generuje: článek, Twitter thread, Instagram post, Stories, Reels scénář, YouTube scénář, Podcast scénář
- **Fact-check agent**: DuckDuckGo search + Claude → % skóre ověřitelnosti + zdroje

### Publikace
- Twitter/X: **manuálně** (API $100/měs — nevyplatí se ve fázi vývoje)
- Instagram, YouTube: API integrace v pozdější fázi
- Buffer free tier jako záložní možnost

### Pravidla projektu
- **Free-first:** Vždy nejdřív free varianta, placená jen s cenou jako alternativa
- **Security-first:** scan_security() před každým git push, bez výjimky

---

## Aktuální fáze projektu

**Fáze:** 1 — Development platformy (ne obsah)
**Priorita:** Zprovoznit celou pipeline — sběr → výběr → generování → publikace

---

## Příští kroky — pro nový session (Fáze A)

1. Migrace dashboardu na **FastAPI** (server/main.py + dashboard/index.html)
2. Vytvoření **SQLite databáze** (database.py — tabulky items, generated, published)
3. První **RSS agent** (agents/rss-agent.py — stahuje novinky, ukládá do DB)
4. Sekce **Feed** v dashboardu (zobrazení novinek z DB, filtrování, archiv)
5. Tlačítko **"Zpracovat"** u každé novinky → spustí pipeline

---

## Otevřené otázky pro budoucí session

- Kdy přejít na publikaci přes API (až bude obsah pravidelný a ověřený)?
- Kdy přidat Supabase (až bude potřeba cloud přístup)?
- Doménové jméno pro web (ai-edu.cz nebo jiné)?

---

## Soubory projektu (aktuální stav)

```
ai-edu-cz/
├── CLAUDE.md                          ✅
├── SESSION.md                         ✅ (tento soubor)
├── PROGRESS.md                        ✅
├── dashboard.py                       ✅ (bude migrován na FastAPI)
├── .env                               ✅ (Anthropic API key nastavený)
├── .env.example                       ✅
├── .gitignore                         ✅ (rozšířený)
├── scripts/                           ✅
├── strategie/                         ✅ (5 dokumentů)
├── obsah/modul-1-zaklady/            ✅ (1 lekce)
├── obsah/modul-2 až modul-6/        ⏳ (prázdné, připravené)
├── agenti/                            ⏳ (README, čeká na vývoj)
├── automatizace/                      ⏳ (README, čeká na vývoj)
├── web/                               ⏳ (Fáze 2)
├── assets/                            ⏳
├── prompt-knihovna/                   ✅ (emailové šablony)
└── sablony/                           ✅ (Twitter šablona)
```
