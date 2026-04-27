# Session State — AI-EDU-CZ / HugoAI.cz

> Čti tento soubor na začátku každého sessionu. Pak přečti také `C:\Users\haasr\Desktop\hugoai\CLAUDE.md`.

---

## Poslední update
**Datum:** 2026-04-27
**Session číslo:** 4
**Claude model:** claude-sonnet-4-6

---

## Stav obou projektů

### Mission Control (ai-edu-cz) — localhost:8765
- Spustit: `python start.py` → port 8765
- Dashboard: 5 tabů — Přehled / Feed / ✨Výstupy / GitHub / Session
- DB: `data/aieducz.db` — items, generated, published

### Veřejný web (hugoai.cz)
- **URL:** https://hugoai.cz
- **Deploy:** Vercel — automaticky při `git push` do `haasradek/hugoai`
- **Složka:** `C:\Users\haasr\Desktop\hugoai\`
- **Slovník:** 100+ pojmů → `hugoai.cz/slovnik/`
- **Články:** `wiki/clanky/` → `hugoai.cz/clanky/` ✅ funguje, 3 články live

---

## Co bylo uděláno v Session 4

### Pipeline — dokončeno
- **Full-text fetch přesunut do content_agent** — RSS je rychlý, plný text se stáhne jen při "Zpracovat"
- **YAML escaping** — uvozovky v titulcích a summary se automaticky escapují (`_yaml_str()`)
- **DB reset** — čistý start po přepnutí architektury

### Dashboard UI opravy
- **"Článek (blog)" label** — neklikatelný badge místo tlačítka (1 platforma = label, více = taby)
- **Titulek modalu** — po generování se změní na "Vygenerovaný obsah"
- **Po publikování** — textarea readonly, "Uložit úpravy" skryto, jen URL odkaz
- **Badge výstupů** — načítá se při init stránky, ne až po kliknutí

### Web hugoai.cz — design a funkce
- **Logo** — větší (48px), nav "Články" → `/clanky` s aktivním stavem
- **Hero** — "AI pro lidi." / "Pochop ji. Využij ji."
- **Stránka pojmu** — skrytý duplicitní H1, odstraněny "Jdi hlouběji" a "Poznámky", "Hugovo vysvětlení" cyan barvou, "Související pojmy" (ne slovensky)
- **Homepage** — sekce "Nejnovější AI články" (poslední 3 + "Všechny články →")
- **`/clanky`** — přehled článků (seřazeno dle data)
- **`/clanky/[slug]`** — detail článku (breadcrumb, meta, markdown)

### Opravené bugy
- **YAML build failure** — uvozovky v summary rozbíjely Astro build → Vercel nenasazoval nové články
- **Lokální build ověřen** — `npm run build` → 206 stránek OK

---

## Aktuální pipeline — stav

```
RSS feeds → SQLite DB (rychle, ~30 sec)          ✅
Feed dashboard → výběr článku                    ✅
"Zpracovat" → fetch full text → Claude API       ✅
Editace v modalu                                 ✅
"Uložit úpravy" → DB                            ✅
"Publikovat" → hugoai/wiki/clanky/ → git push   ✅
Vercel deploy → hugoai.cz/clanky/{slug}         ✅
Tab "Výstupy" — přehled, kopírovat              ✅
Automatické RSS (Task Scheduler)                 ⏳ Priorita 1
Hromadné zpracování více článků                  ⏳ Priorita 1
SEO / Open Graph tagy                           ⏳ Priorita 2
Paginace a filtry na /clanky                    ⏳ Priorita 2
Vzdělávací moduly (obsah/)                      ⏳ Priorita 3
Newsletter (Beehiiv integrace)                  ⏳ Priorita 4
Fact-check agent                                ⏳ Budoucí
```

---

## Příští kroky — Session 5

### Priorita 1: Automatizace pipeline
1. **Windows Task Scheduler** — automatické spouštění `agenti/rss_agent.py` každých 6 hodin
   - Skript: `scheduler/rss_cron.py` nebo PowerShell task
   - Alternativa: přidat "Spustit automaticky" toggle do dashboardu
2. **Hromadné zpracování** — checkbox u každého článku ve Feed tabu + tlačítko "Zpracovat vybrané"
   - API: `POST /api/process-batch` s body `{"item_ids": [...], "platforms": [...]}`

### Priorita 2: Web — distribuce a SEO
3. **Open Graph meta tagy** — pro `/clanky/[slug].astro` přidat `og:title`, `og:description`, `og:image`
   - Generovat OG obrázek nebo použít statický fallback
4. **Filtrování `/clanky`** — filtr dle tagu (claude, chatgpt, agenti...) + search

### Priorita 3: Vzdělávací obsah
5. **Modul 1: Co je AI** — napsat první lekci (`obsah/modul-1-zaklady/01-co-je-ai.md`)
   - Formát: markdown, česky, bez žargonu, s příklady

### Priorita 4: Growth
6. **Beehiiv newsletter** — propojit formulář na homepage s Beehiiv API
7. **Google Analytics / Plausible** — přidat tracking na hugoai.cz

---

## Technické poznámky pro příští session

### Soubory k editaci — VŽDY v hlavním adresáři
```
C:\Users\haasr\Desktop\claude\ai-edu-cz\    ← ai-edu-cz dashboard
C:\Users\haasr\Desktop\hugoai\              ← veřejný web
```
**NIKDY** editovat ve worktree: `.claude\worktrees\*`

### YAML v článcích — pravidla
- Funkce `_yaml_str()` v `server/main.py` escapuje `"` → `\"`
- Před každým pushem do hugoai spustit lokálně: `cd site && npm run build`
- Pokud build selže → zkontrolovat `wiki/clanky/*.md` frontmatter

### Klíčové soubory
| Soubor | Účel |
|--------|------|
| `server/main.py` | FastAPI backend, všechny API endpointy, publish logika |
| `server/static/index.html` | Dashboard SPA (vše inline) |
| `agenti/content_agent.py` | Claude API generátor, full-text fetch |
| `agenti/rss_agent.py` | RSS pipeline, FETCH_FULLTEXT=False |
| `database.py` | SQLite funkce |
| `hugoai/site/src/pages/clanky/` | Astro stránky pro články |
| `hugoai/site/src/layouts/Layout.astro` | Header, nav, footer |
| `hugoai/site/src/pages/index.astro` | Homepage |
