# Session State — AI-EDU-CZ / HugoAI.cz

> Čti tento soubor na začátku každého sessionu. Pak přečti také `C:\Users\haasr\Desktop\hugoai\CLAUDE.md`.

---

## Poslední update
**Datum:** 2026-04-27
**Session číslo:** 5
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
- **Články:** `wiki/clanky/` → `hugoai.cz/clanky/` ✅ funguje, články live

---

## Co bylo uděláno v Session 5

### Pipeline — hromadné zpracování
- **Batch processing** — checkboxy u článků, floating toolbar dole na obrazovce, progress modal s progress barem
- **Backend:** `POST /api/process-batch` + `GET /api/process-batch/{job_id}` (background task + polling)
- **Dismiss tlačítko** — ✕ u každého nového článku, nastaví `processed=2`, zmizí z feedu
- **Filtr "Skryté"** — v dropdownu pro zpětné zobrazení skrytých článků

### RSS agent — čistý feed
- **MAX_AGE_DAYS = 3** — přeskakuje články starší 3 dny při fetchování
- **DB:** `get_items()` defaultně skrývá `processed=2`, `count_items()` je nepočítá

### Řazení článků
- **`date` v frontmatter** nyní obsahuje full datetime (`YYYY-MM-DDTHH:MM:SS`) místo jen data
- Správné sestupné řazení i pro více článků ze stejného dne

### Web hugoai.cz
- **Open Graph + Twitter Card meta tagy** — `og:title`, `og:description`, `og:type`, `og:url`, `og:image`, `og:locale`, canonical URL, `twitter:card`
- **Filtrování `/clanky`** — tag filtry nad seznamem článků, client-side JS, počítadlo se aktualizuje

---

## Aktuální pipeline — stav

```
RSS feeds → SQLite DB (rychle, ~30 sec)          ✅
Feed dashboard → výběr článku                    ✅
"Zpracovat" → fetch full text → Claude API       ✅
Hromadné zpracování (batch)                      ✅
Dismiss nepotřebných článků                      ✅
Editace v modalu                                 ✅
"Uložit úpravy" → DB                            ✅
"Publikovat" → hugoai/wiki/clanky/ → git push   ✅
Vercel deploy → hugoai.cz/clanky/{slug}         ✅
Tab "Výstupy" — přehled, kopírovat              ✅
Open Graph + Twitter Card meta tagy             ✅
Filtrování /clanky dle tagu                     ✅
Automatické RSS (Task Scheduler)                 ⏳ přeskočeno
Hromadné publikování více článků                 ⏳ Priorita 1
Newsletter (Beehiiv integrace)                  ⏳ Priorita 1
Vzdělávací modul 1: Co je AI                    ⏳ Priorita 2
SEO social image (1200×630px OG obrázek)        ⏳ Priorita 3
Paginace /clanky                                ⏳ Priorita 3
Fact-check agent                                ⏳ Budoucí
```

---

## Příští kroky — Session 6

### Priorita 1: Hromadné publikování
1. **Batch publish** — checkboxy u zpracovaných výstupů (typ: article) v tab Výstupy nebo Feed
   - Tlačítko "Publikovat vybrané" → sekvenčně spustí `POST /api/publish/{gen_id}` pro každý vybraný
   - Progress podobný batch processingu (modal nebo floating toolbar)

### Priorita 2: Newsletter — Beehiiv
2. **Beehiiv API integrace** — formulář na homepage (`hugoai/site/src/pages/index.astro`)
   - Beehiiv API endpoint: `POST https://api.beehiiv.com/v2/publications/{id}/subscriptions`
   - Potřeba: `BEEHIIV_API_KEY` a `BEEHIIV_PUBLICATION_ID` v `.env`
   - Frontend: nahradit placeholder `/#newsletter` sekcí s funkčním formulářem
   - Backend: nový endpoint `POST /api/newsletter/subscribe` (proxy, aby API klíč nezůstal v JS)

### Priorita 3: Vzdělávací obsah
3. **Modul 1: Co je AI** — první lekce (`obsah/modul-1-zaklady/01-co-je-ai.md`)
   - Formát: markdown, česky, bez žargonu, s příklady z reálného života
   - Délka: ~800–1200 slov
   - Cílová skupina: úplný laik, ne technický člověk

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
- `date` pole = `YYYY-MM-DDTHH:MM:SS` (celý datetime pro správné řazení)
- Před každým pushem do hugoai spustit lokálně: `cd site && npm run build`

### processed stavy v DB (items tabulka)
| Hodnota | Význam |
|---------|--------|
| `0` | Nový — čeká na zpracování |
| `1` | Zpracovaný — má generated obsah |
| `2` | Skrytý (dismissed) — nezobrazuje se ve feedu |

### Klíčové soubory
| Soubor | Účel |
|--------|------|
| `server/main.py` | FastAPI backend, všechny API endpointy, publish logika |
| `server/static/index.html` | Dashboard SPA (vše inline) |
| `agenti/content_agent.py` | Claude API generátor, full-text fetch |
| `agenti/rss_agent.py` | RSS pipeline, MAX_AGE_DAYS=3 |
| `database.py` | SQLite funkce |
| `hugoai/site/src/pages/clanky/` | Astro stránky pro články |
| `hugoai/site/src/layouts/Layout.astro` | Header, nav, footer, OG tagy |
| `hugoai/site/src/pages/index.astro` | Homepage |
