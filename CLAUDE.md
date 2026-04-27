# AI-EDU-CZ — Mission Control Dashboard

## ⚠️ KRITICKÁ PRAVIDLA PRO CLAUDE (čti VŽDY jako první)

### 1. Kde editovat soubory
**VŽDY edituj v hlavním adresáři:**
```
C:\Users\haasr\Desktop\claude\ai-edu-cz\
```
**NIKDY ne ve worktree:**
```
C:\Users\haasr\Desktop\claude\ai-edu-cz\.claude\worktrees\*  ← IGNORUJ
```
Server běží z hlavního adresáře. Změny ve worktree uživatel nikdy neuvidí.

### 2. Dva projekty = jeden systém
Toto je JEDEN projekt rozdělený do dvou složek:

| Složka | Role | URL |
|--------|------|-----|
| `C:\Users\haasr\Desktop\claude\ai-edu-cz\` | **Mission Control** — backend pipeline, dashboard | localhost:8765 |
| `C:\Users\haasr\Desktop\hugoai\` | **Veřejný web** — slovník + blog | hugoai.cz |

**Tok dat:**
```
RSS feeds → ai-edu-cz DB → Claude API generuje → editace → PUBLIKOVAT → hugoai/wiki/clanky/ → git push → Vercel → hugoai.cz
```

### 3. Na začátku každého sessionu přečti:
1. `C:\Users\haasr\Desktop\claude\ai-edu-cz\SESSION.md` ← stav projektu
2. `C:\Users\haasr\Desktop\hugoai\CLAUDE.md` ← schema webu

---

## Projekt — přehled

**Název:** AI-EDU-CZ / HugoAI.cz  
**Zakladatel:** Radek Haas — technolog, GZ Media  
**Zahájení:** 2026-04-26  
**Cíl:** Nejlepší česky psaný vzdělávací zdroj o AI — každý Čech a Slovák může pochopit AI a využít ji.

---

## Architektura systému

### Mission Control (ai-edu-cz)
- **Dashboard:** `http://localhost:8765` — spustit přes `python start.py`
- **Backend:** FastAPI (`server/main.py`)
- **DB:** SQLite `data/aieducz.db` — tabulky: `items`, `generated`, `published`
- **Git repo:** součást většího projektu na ploše

### Veřejný web (hugoai.cz)
- **Framework:** Astro (static site)
- **Hosting:** Vercel — automatický deploy při git push
- **Git repo:** `https://github.com/haasradek/hugoai.git`
- **Lokální složka:** `C:\Users\haasr\Desktop\hugoai\`
- **Obsah:**
  - `wiki/pojmy/` → `hugoai.cz/slovnik/{slug}` — AI slovník (hotovo, 100+ pojmů)
  - `wiki/clanky/` → `hugoai.cz/clanky/{slug}` — Blog články (sem publikujeme z dashboardu)
  - `wiki/kategorie/` — přehledy kategorií
  - `wiki/synteza/` — analýzy a syntézy

### Frontmatter pro blog článek (`wiki/clanky/slug.md`)
```yaml
---
title: "Název článku"
date: "YYYY-MM-DD"
source: "Zdroj (např. TechCrunch AI)"
tags: ["ai", "novinky", "claude"]
summary: "Krátké shrnutí článku (max 180 znaků)"
---
```

---

## Pipeline — aktuální stav

```
RSS feeds (10 zdrojů)  →  SQLite DB          ✅ hotovo
SQLite DB              →  Feed dashboard     ✅ hotovo
Feed dashboard         →  "Zpracovat" modal  ✅ hotovo
"Zpracovat" modal      →  Claude API         ✅ hotovo
Claude API             →  generated tabulka  ✅ hotovo
generated tabulka      →  Editace v modalu   ✅ hotovo
Editace                →  "Publikovat"       ✅ hotovo
"Publikovat"           →  hugoai/wiki/clanky ✅ hotovo
git push hugoai        →  Vercel deploy      ✅ automaticky
```

---

## Dashboard — struktura a endpointy

### Taby
- **📊 Přehled** — statistiky, git stav, příští kroky
- **📰 Feed** — RSS články, filtr, tag filtr, "Zpracovat" modal
- **✨ Výstupy** — všechny vygenerované texty, kopírovat, otevřít detail
- **⚡ GitHub** — security scan, push
- **💾 Session** — uložit stav, poznámky

### API endpointy
| Metoda | Endpoint | Popis |
|--------|----------|-------|
| POST | `/api/status` | Stav projektu (git, feed, progress) |
| POST | `/api/security-scan` | Security audit |
| POST | `/api/push` | Commit + push ai-edu-cz |
| POST | `/api/save-session` | Uložit SESSION.md + push |
| GET | `/api/feed` | Seznam RSS článků z DB |
| POST | `/api/feed/fetch` | Spustit RSS agenta |
| GET | `/api/feed/{id}` | Detail článku + generated |
| POST | `/api/process/{id}` | Generovat obsah (Claude API) |
| GET | `/api/generated` | Všechny vygenerované výstupy |
| PATCH | `/api/generated/{id}` | Uložit úpravy do DB |
| POST | `/api/publish/{id}` | Publikovat článek na hugoai.cz |

---

## Agenti

| Soubor | Stav | Popis |
|--------|------|-------|
| `agenti/rss_agent.py` | ✅ | Stahuje RSS, ukládá do DB, detekuje tagy |
| `agenti/content_agent.py` | ✅ | Claude API → článek/twitter/instagram/youtube |
| `agenti/factcheck_agent.py` | ⏳ | Fact-check pomocí vyhledávání (budoucí) |

### Content agent — platformy
- `article` — blog článek 600–1000 slov (PRIORITA)
- `twitter` — thread 5–7 tweetů
- `instagram` — caption + hashtags
- `youtube` — scénář videa 4–6 minut

---

## Soubory projektu (aktuální stav)

```
C:\Users\haasr\Desktop\claude\ai-edu-cz\
├── CLAUDE.md                    ✅ tento soubor
├── SESSION.md                   ✅ stav projektu (čti na začátku sessionu)
├── PROGRESS.md                  ✅ checklist lekcí
├── start.py                     ✅ spustí server (python start.py)
├── database.py                  ✅ SQLite — items, generated, published
├── .env                         ✅ ANTHROPIC_API_KEY, HUGOAI_PATH
├── .env.example                 ✅
├── .gitignore                   ✅
├── data/
│   └── aieducz.db               ✅ SQLite databáze (112+ článků)
├── server/
│   ├── main.py                  ✅ FastAPI — všechny API endpointy
│   └── static/index.html        ✅ Dashboard UI (SPA, inline JS)
├── agenti/
│   ├── rss_agent.py             ✅ RSS pipeline
│   ├── content_agent.py         ✅ Claude API generátor
│   └── factcheck_agent.py       ⏳ TODO
├── strategie/                   ✅ strategické dokumenty
├── obsah/                       ⏳ vzdělávací moduly (prázdné)
├── prompt-knihovna/             ✅ šablony promptů
└── sablony/                     ✅ šablony pro sociální sítě

C:\Users\haasr\Desktop\hugoai\   ← VEŘEJNÝ WEB
├── CLAUDE.md                    ✅ schema webu (čti na začátku sessionu)
├── wiki/
│   ├── pojmy/                   ✅ 100+ AI pojmů → hugoai.cz/slovnik/
│   ├── clanky/                  ✅ blog články → hugoai.cz/clanky/
│   ├── kategorie/               ✅ přehledy kategorií
│   └── synteza/                 ⏳ analýzy
├── site/                        ✅ Astro projekt
│   ├── src/content.config.ts    ✅ Astro content schema
│   ├── src/pages/               ✅ stránky
│   └── src/layouts/             ✅ layouty
└── raw/                         ✅ zdrojové dokumenty (immutable)
```

---

## RSS feedy

| Zdroj | Stav | Poznámka |
|-------|------|----------|
| TechCrunch AI | ✅ | |
| VentureBeat AI | ✅ | |
| The Verge AI | ✅ | |
| OpenAI Blog | ✅ | filter_ai=True |
| Google News CZ | ✅ | AI klíčová slova |
| Google News SK | ✅ | AI klíčová slova |
| Lupa.cz | ✅ | filter_ai=True |
| Root.cz | ✅ | filter_ai=True |
| Anthropic Blog | ❌ | RSS neexistuje |
| HackerNews AI | ❌ | nestabilní |

---

## Bezpečnostní pravidla (neporušitelná)

- **Před každým `git push` musí proběhnout `scan_security()`** — bez výjimky
- `.env` soubory nikdy na GitHub — vždy v `.gitignore`
- API klíče pouze v `.env`, nikdy natvrdo v kódu

---

## Pracovní principy

1. **Czech-first:** Veškerý obsah primárně v češtině
2. **Jednoduše, prakticky:** Žádný zbytečný žargon, vždy příklad
3. **Zdarma nejdříve:** Vždy hledat free alternativu, cenu uvést u placených
4. **Editovat v hlavním adresáři:** NIKDY ve worktree
5. **Konzistence:** Stejný tone of voice napříč platformami
