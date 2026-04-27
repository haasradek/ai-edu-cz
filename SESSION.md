# Session State — AI-EDU-CZ / HugoAI.cz

> Čti tento soubor na začátku každého sessionu. Pak přečti také `C:\Users\haasr\Desktop\hugoai\CLAUDE.md`.

---

## Poslední update
**Datum:** 2026-04-27
**Session číslo:** 3
**Claude model:** claude-sonnet-4-6

---

## Stav obou projektů

### Mission Control (ai-edu-cz) — localhost:8765
- `python start.py` → spustí server na portu 8765
- Dashboard má 5 tabů: Přehled / Feed / ✨Výstupy / GitHub / Session
- DB má 112+ článků z RSS feedů

### Veřejný web (hugoai.cz)
- **URL:** https://hugoai.cz
- **Deploy:** Vercel — automaticky při `git push` do `haasradek/hugoai`
- **Lokální složka:** `C:\Users\haasr\Desktop\hugoai\`
- **Slovník:** 100+ pojmů v `wiki/pojmy/` → `hugoai.cz/slovnik/`
- **Blog:** `wiki/clanky/` → `hugoai.cz/clanky/` (publikujeme z dashboardu)

---

## Co bylo uděláno v Session 3

### Generovací pipeline (Fáze B — dokončena)
- **`agenti/content_agent.py`** — Claude API generátor (4 platformy)
  - `article` — blog článek 600–1000 slov v češtině
  - `twitter` — thread 5–7 tweetů
  - `instagram` — caption + hashtags
  - `youtube` — scénář videa 4–6 minut
- **`POST /api/process/{item_id}`** — spustí content agenta, vrátí výsledky

### Dashboard — nové funkce
- **Modal "Zpracovat"** — kliknutím na článek ve Feedu otevře modal s checklistem platforem
  - Článek (blog) zaškrtnutý defaultně
  - Twitter, Instagram, YouTube volitelné
  - Spinner během generování
  - Výsledky v tabech po vygenerování
- **Editovatelná textarea** — obsah lze upravit před publikováním
- **Tlačítko "💾 Uložit úpravy"** — uloží upravenou verzi zpátky do DB
- **Tlačítko "🌐 Publikovat na hugoai.cz"** — pro typ `article`
- **Tab "✨ Výstupy"** — všechny vygenerované texty, filtr dle typu, kopírovat

### Publikační pipeline (hotovo)
- **`POST /api/publish/{gen_id}`** — zapíše `.md` do `hugoai/wiki/clanky/`, git commit + push
- Frontmatter: `title`, `date`, `source`, `tags`, `summary`
- Po pushu Vercel automaticky přestaví web

### Opraveno
- **Worktree bug** — všechny předchozí sessiony editovaly worktree místo hlavního adresáře.
  Soubory synchronizovány. Od teď vždy editovat v `C:\Users\haasr\Desktop\claude\ai-edu-cz\`
- **Modal viditelnost** — gradient pozadí + cyan border
- **`_modalState` bug** — explicitní `'block'/'flex'/'none'` místo prázdného stringu

---

## Aktuální pipeline (celkový stav)

```
RSS feeds → SQLite DB                        ✅
SQLite DB → Feed dashboard                   ✅
Feed → "Zpracovat" modal → Claude API        ✅
Claude API → generated tabulka               ✅
Editace v modalu + uložit úpravy             ✅
"Publikovat" → hugoai/wiki/clanky/           ✅
git push → Vercel → hugoai.cz               ✅
Tab "Výstupy" — přehled všech výstupů        ✅
Fact-check agent                             ⏳ TODO
Automatické plánování (Windows Scheduler)    ⏳ TODO
Twitter/Instagram přímá publikace            ⏳ budoucí
```

---

## Příští kroky — pro nový session

1. **Fact-check agent** — `agenti/factcheck_agent.py`
   - DuckDuckGo/Tavily search + Claude → skóre věrohodnosti + zdroje
   - Zobrazit v modalu před publikováním
2. **Automatické spouštění RSS** — Windows Task Scheduler nebo cron
   - `agenti/rss_agent.py` spouštět každých 6 hodin automaticky
3. **hugoai.cz — stránka článků** — zkontrolovat jestli `clanky` route v Astru existuje
   - Pokud ne, vytvořit `site/src/pages/clanky/[slug].astro`
4. **Vzdělávací obsah** — začít psát lekce do `obsah/modul-1-zaklady/`
   - Modul 1: Co je AI, jak myslí, mýty, bezpečnost
5. **Commit + push** ai-edu-cz na GitHub

---

## Otevřené otázky

- Existuje Astro stránka pro `hugoai.cz/clanky/`? Zkontrolovat `site/src/pages/`.
- Přidat Windows Task Scheduler pro automatický RSS fetch?
- Twitter/Instagram API pro přímou publikaci (zatím jen clipboard)?
- Newsletter integrace (Beehiiv)?

---

## Soubory — kompletní stav

```
C:\Users\haasr\Desktop\claude\ai-edu-cz\    ← EDITOVAT ZDE
├── CLAUDE.md                    ✅ přečíst na začátku sessionu
├── SESSION.md                   ✅ tento soubor
├── PROGRESS.md                  ✅
├── start.py                     ✅ python start.py → localhost:8765
├── database.py                  ✅ get_all_generated(), update_generated_content()
├── .env                         ✅ ANTHROPIC_API_KEY, HUGOAI_PATH
├── server/
│   ├── main.py                  ✅ všechny API endpointy vč. /api/publish/
│   └── static/index.html        ✅ dashboard — modal, výstupy, publikování
├── agenti/
│   ├── rss_agent.py             ✅
│   ├── content_agent.py         ✅ Claude API, 4 platformy
│   └── factcheck_agent.py       ⏳ TODO

C:\Users\haasr\Desktop\hugoai\              ← VEŘEJNÝ WEB
├── CLAUDE.md                    ✅ přečíst na začátku sessionu
├── wiki/pojmy/                  ✅ 100+ pojmů
├── wiki/clanky/                 ✅ blog (publikováno z dashboardu)
└── site/                        ✅ Astro projekt (npm run build → Vercel)
```
