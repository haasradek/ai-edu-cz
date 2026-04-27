# Nápady a tipy pro AI-EDU-CZ / HugoAI.cz

> Sloučeno z `ideas.docx` + `tips.docx` — zdroj nápadů pro budoucí rozvoj projektu.  
> Při plánování další session zde hledej inspiraci.

---

## Stav implementace

| Symbol | Význam |
|--------|--------|
| ✅ | Hotovo |
| 🔄 | V pipeline / částečně |
| ⏳ | Plánováno |
| 💡 | Nápad k zvážení |

---

## PRIORITA 1 — Připraveno k implementaci

### ✅ AI Slovník / Wikipedie CZ
Základ webu. SEO magnet. URL: `hugoai.cz/slovnik/{pojem}`.  
**Přínos: 95% | Náročnost: 2/10**

### ✅ Učebnice AI
Strukturované lekce po modulech. URL: `hugoai.cz/ucebnice/{slug}`.  
**Přínos: 90% | Náročnost: 3/10**

### ✅ Nejnovější AI články
RSS → Claude → publikace na web. URL: `hugoai.cz/clanky/{slug}`.  
**Přínos: 85% | Náročnost: 4/10**

### ⏳ Automatizovaný Newsletter (Beehiiv)
Beehiiv free plan až do 2 500 odběratelů.  
Mechanika: nový článek → API Beehiiv → draft newsletteru automaticky.  
`POST https://api.beehiiv.com/v2/publications/{id}/subscriptions`  
Potřeba: `BEEHIIV_API_KEY` + `BEEHIIV_PUBLICATION_ID` v `.env`.  
**Přínos: 85% | Náročnost: 3/10**

### ⏳ Převod článku → 5 formátů
Jeden Markdown článek → automaticky:
- LinkedIn post
- Instagram carousel text
- X/Twitter thread
- YouTube scénář
- Newsletter draft

Extrémní leverage. Jeden obsah = 5 výstupů.  
**Přínos: 100% | Náročnost: 5/10**

---

## PRIORITA 2 — Střední náročnost, vysoký dopad

### ⏳ Zapojení dalších AI modelů do dashboardu
Výběr modelu přímo v modalu "Zpracovat":
- **Gemini Flash** (zdarma přes Google AI Studio) → RSS filtrování, tagy, sumarizace
- **Perplexity** (free tier) → fact-checking, ověřování zdrojů
- **Claude** → kvalitní blog článek (zůstává pro nejdůležitější výstupy)
- **GPT-4o mini** → Twitter/Instagram/YouTube (levnější alternativa)

Vše ovládané z dashboardu — výběr modelu jedním kliknutím.  
**Přínos: 92% | Náročnost: 5/10**

### ⏳ AI Trend Radar CZ/SK
Automatický sběr AI novinek pro český/slovenský trh.  
n8n každý den projede: Reddit (r/ChatGPT, r/artificial), Hacker News, X trendy, Product Hunt AI.  
Claude/Gemini vytáhne: co je hype, co je reálně užitečné, co stojí za článek.  
Výstup: "AI novinky týdne" newsletter + Shorts/Reels podklady.  
**Přínos: 90% | Náročnost: 8/10**

### ⏳ Hromadné publikování (Batch publish)
Checkboxy u zpracovaných výstupů v tab Výstupy.  
Tlačítko "Publikovat vybrané" → sekvenčně spustí `/api/publish/{id}`.  
**Přínos: 88% | Náročnost: 4/10**

### 💡 AI Diagnostika firmy (Lead magnet)
Formulář na webu: "Jak moc jste připraveni na AI?" — 10–20 otázek.  
AI vyhodnotí: skóre, doporučení, roadmapa.  
Využití: sběr emailů + budoucí B2B klienti.  
**Přínos: 88% | Náročnost: 6/10**

### 💡 AI Prompt Builder
Interaktivní generátor promptů.  
Formulář: Co chceš udělat? Jaký styl? Jaký formát? → hotový prompt.  
Virální feature na web.  
**Přínos: 88% | Náročnost: 4/10**

---

## PRIORITA 3 — Dobré nápady, prozatím odloženo

### 💡 Hlubší slovníkové pojmy ("Pod pokličkou")
Rozšíření struktury hesla o:
- **Pod pokličkou** — techničtější vysvětlení (jak to funguje uvnitř)
- **Hugův tip pro experty** — konkrétní trik na úsporu času
- **Na co si dát pozor** — časté chyby

SEO benefit: Google miluje delší, expertní texty.  
Začít s 10 nejdůležitějšími pojmy (AI, LLM, Prompt, RAG...).  
**Přínos: 85% | Náročnost: 5/10**

### 💡 Gemini jako "Multimodální Skener" (zdarma)
Google AI Studio — Gemini 1.5 Pro/Flash s štědrým free limitem.  
Nahraješ PDF knihu, YouTube záznam nebo 100 fotek z konference.  
Gemini udělá výtah lekcí přímo do Markdown souborů.  
**Přínos: 92% | Náročnost: 4/10**

### 💡 AI Audio-Lekce (NotebookLM)
Nahrát Markdown soubory z `obsah/` do NotebookLM.  
Automaticky vygeneruje "Deep Dive" audio podcast jako bonus ke stažení.  
Cena: 0 Kč.  
**Přínos: 90% | Náročnost: 1/10**

### 💡 Automatický generátor PDF e-booků
n8n vezme články z Markdownu a složí do PDF.  
Příklad: "10 nejlepších AI nástrojů 2026".  
Lead magnet: email za PDF.  
**Přínos: 80% | Náročnost: 4/10**

### 💡 AI Compare Tool
Uživatel zadá prompt → backend pošle do GPT, Claude, Gemini, Grok → ukáže rozdíly.  
Unikátní feature: "Který AI model je nejlepší?"  
**Přínos: 80% | Náročnost: 7/10**

### 💡 AI Challenge — 30 dní s AI
Každý den email/Telegram: "Dnešní úkol: použij AI na…"  
Gamifikace, retence uživatelů, budování návyku.  
**Přínos: 78% | Náročnost: 5/10**

### 💡 Komunita — Prompt-O-Mat (Google Sheets)
Google Tabulky jako databáze promptů (zdarma).  
Uživatelé posílají oblíbené prompty → Claude je týdně zkontroluje → n8n přidá do `obsah/modul-3-prompting/`.  
**Přínos: 82% | Náročnost: 4/10**

### 💡 AI Workflow Marketplace
Sekce na webu: "Stáhni n8n workflow zdarma".  
Příklady: AI newsletter automatizace, AI shrnutí emailů, AI generátor postů.  
Budování autority — lidé budou sdílet.  
**Přínos: 86% | Náročnost: 5/10**

---

## PRIORITA 4 — Budoucnost / monetizace

### 💡 AI Akademie pro firmy (B2B)
Landing page: "Naučíme váš tým používat AI."  
Workshop + audit + implementace.  
Spustit až při dostatečném trafficu.  
**Přínos: 95% | Náročnost: 7/10**

### 💡 Lokální "Video-to-Shorts" střihač
FFmpeg (open-source) + Whisper (lokálně).  
16:9 video → automaticky ořízne na 9:16, přidá titulky → Reels/Shorts.  
**Přínos: 82% | Náročnost: 9/10**

### 💡 Prompt Playground (Hugging Face Spaces)
Hostovat demo na Hugging Face (zdarma pro open-source projekty).  
Lidé si vyzkouší prompty z `prompt-knihovna/` přímo v prohlížeči.  
**Přínos: 75% | Náročnost: 8/10**

---

## Technické SEO — checklist (z tips.docx)

- [ ] `title` tag na homepage ✅
- [ ] `meta description` ✅
- [ ] `sitemap.xml` — zkontrolovat/přidat
- [ ] `robots.txt` — zkontrolovat
- [ ] Open Graph obrázek (1200×630px) ✅ (základní)
- [ ] `canonical URL` ✅
- [ ] Google Analytics — nasadit
- [ ] Google Search Console — propojit + indexace
- [ ] Po každém novém článku: "Požádat o indexaci" v Search Console

---

## Sociální sítě — checklist

- [ ] LinkedIn — profil HugoAI.cz
- [ ] Instagram — @hugoai.cz
- [ ] X/Twitter — @hugoaicz
- [ ] YouTube — kanál HugoAI

---

*Soubor aktualizován: Duben 2026 | Sloučeno z ideas.docx + tips.docx*
