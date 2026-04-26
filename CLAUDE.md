# AI-EDU-CZ — Vzdělávací platforma o AI pro Čechy a Slováky

## Vize projektu

Vytvořit nejlepší česky psaný vzdělávací zdroj o umělé inteligenci. Cíl je jednoduchý: aby každý Čech a Slovák mohl pochopit AI, nebát se jí a využít ji ve svém životě a práci.

**Zakladatel:** Radek Haas — technolog, IT vzdělání, GZ Media  
**Datum zahájení:** 2026-04-26  
**Jazyk:** Čeština (primárně), slovenština (sekundárně)

---

## Role Claude Code v projektu

Claude Code (Sonnet 4.6) je **mozkem celé platformy**. Orchestruje ostatní AI modely, navrhuje strategii, tvoří obsah, generuje výstupy pro různé kanály a průběžně zlepšuje platformu.

### Co Claude Code dělá:
- Navrhuje architekturu a strategii projektu
- Koordinuje zapojení ostatních AI modelů (GPT, Gemini, Grok, Perplexity)
- Generuje a reviduje vzdělávací obsah v češtině
- Vytváří šablony pro sociální sítě a YouTube
- Automatizuje opakující se úkoly
- Udržuje konzistenci obsahu napříč kanály

---

## Zapojené AI modely a jejich role

Projekt využívá celý ekosystém AI nástrojů a platforem — nejen jazykové modely, ale i nástroje pro design, video, audio, automatizaci, hosting a analýzu.

**Kompletní přehled všech platforem:** viz [`strategie/platformy-a-nastroje.md`](strategie/platformy-a-nastroje.md)

### Klíčové nástroje (stručně)

| Kategorie | Primární nástroj | Záložní |
|-----------|-----------------|---------|
| **LLM / Mozek** | Claude Code | ChatGPT, Gemini, Grok |
| **Research** | Perplexity | Tavily, Exa |
| **Design** | Canva | DALL-E, Leonardo.ai |
| **Video** | OBS + CapCut | Runway, HeyGen |
| **Audio** | ElevenLabs | NotebookLM Podcast |
| **Znalosti** | NotebookLM | Obsidian + AI |
| **Automatizace** | n8n (self-hosted) | Make.com |
| **AI Agenti** | Claude API + CrewAI | LangChain, Flowise |
| **Vektorová DB** | Pinecone | Chroma, Supabase |
| **Hosting** | Vercel | GitHub Pages |
| **Newsletter** | Beehiiv | Substack |

---

## Struktura obsahu platformy

### Modul 1: Základy AI (pro úplné začátečníky)
- Co je umělá inteligence? (bez žargonu)
- Jak AI "myslí" — jednoduché vysvětlení
- Historie AI v 5 minutách
- AI dnes: co existuje a co umí
- Mýty o AI (přijdu kvůli ní o práci?)
- Bezpečnost a soukromí při práci s AI

### Modul 2: Přehled AI nástrojů
- ChatGPT — jak začít (step-by-step)
- Gemini — jak začít
- Grok — jak začít
- Claude — jak začít
- Perplexity — jak začít
- Porovnání: kdy použít který nástroj?

### Modul 3: Umění promptování
- Co je prompt a proč na něm záleží
- Základní struktura dobrého promptu
- Techniky: Chain-of-Thought, Few-Shot, Role-Play
- Příklady promptů pro práci
- Příklady promptů pro osobní život
- Jak iterovat a vylepšovat prompty
- Prompt knihovna (šablony ke stažení)

### Modul 4: Praktické use cases
- AI pro psaní (emaily, reporty, prezentace)
- AI pro výzkum a učení
- AI pro kreativitu (texty, obrázky, video)
- AI pro programátory (GitHub Copilot, Claude Code)
- AI pro podnikání (marketing, zákaznický servis)
- AI pro studenty
- AI pro učitele

### Modul 5: AI agenti
- Co je AI agent?
- Jak vytvořit svého prvního agenta (Claude, GPT)
- Multi-agent systémy — jak spolupracují AI modely
- Praktický projekt: agent pro denní shrnutí zpráv
- Praktický projekt: agent pro správu emailů

### Modul 6: Automatizace byznysu a workflow
- Mapování workflow — kde ztrácím čas?
- Make.com (Integromat) — základy zdarma
- n8n — open-source alternativa
- Zapier — rychlý start
- Praktické automatizace:
  - Automatický newsletter
  - Social media plánování
  - Reporty z dat
  - CRM automatizace
- ROI automatizace — jak měřit úsporu času

---

## Výstupní kanály

### Fáze 1: Lokální platforma (teď)
- Markdown soubory organizované ve složkách
- Čtení přes Obsidian nebo VS Code
- Zdarma, žádná infrastruktura

### Fáze 2: Web (brzy)
- Statický web generátor: **Astro** nebo **Hugo** (zdarma)
- Hosting: **GitHub Pages** nebo **Vercel** (zdarma)
- Doména: ai-edu.cz nebo podobná (~250 Kč/rok)

### Fáze 3: Sociální sítě
- **Twitter/X:** AI novinky, tipy, zkrácené lekce
- **Instagram:** Vizuální infografiky, Reels (tipy za 60 sekund)
- **LinkedIn:** B2B obsah, use cases pro firmy

### Fáze 4: Video obsah
- **YouTube:** Detailní tutoriály, screencasty
- **YouTube Shorts:** Rychlé tipy (< 60 sekund)
- **Instagram Reels:** Stejný obsah jako Shorts

---

## Technický stack (vše zdarma nebo open-source)

```
Obsah:         Markdown + Git
Web:           Astro/Hugo + GitHub Pages
Automatizace:  n8n (self-hosted, open-source)
Obrázky:       DALL-E 3 free tier, Canva free
Video:         OBS Studio (zdarma), DaVinci Resolve (zdarma)
Hlasy:         ElevenLabs free tier
Analytics:     Plausible / Google Analytics (free)
Emaily:        Resend free tier (3000/měs)
```

---

## Pracovní principy

1. **Czech-first:** Veškerý obsah primárně v češtině
2. **Jednoduše, prakticky:** Žádný zbytečný žargon, vždy příklad
3. **Zdarma nejdříve:** Vždy hledat free alternativu
4. **Multi-channel:** Každý kus obsahu upravit pro více kanálů
5. **Konzistence:** Stejný tone of voice napříč platformami

## Bezpečnostní pravidla (neporušitelná)

- **Před každým `git push` musí proběhnout `scan_security()`** — bez výjimky
- Platí pro všechny cesty: tlačítko Push, Save Session, skripty, agenty, automatizace
- Pokud scan najde problém → push se zablokuje, dokud není opraveno
- `.env` soubory nikdy na GitHub — vždy v `.gitignore`
- API klíče pouze v `.env`, nikdy natvrdo v kódu nebo Markdown souborech

---

## Soubory projektu

```
ai-edu-cz/
├── CLAUDE.md              # Tento soubor — hlavní strategie
├── strategie/
│   ├── vize.md            # Dlouhodobá vize
│   ├── agent-architektura.md  # Jak spolupracují AI modely
│   ├── obsahovy-plan.md   # Editorial kalendář
│   └── monetizace.md      # Budoucí monetizace
├── obsah/
│   ├── modul-1-zaklady/
│   ├── modul-2-nastroje/
│   ├── modul-3-prompting/
│   ├── modul-4-use-cases/
│   ├── modul-5-agenti/
│   └── modul-6-automatizace/
├── sablony/
│   ├── twitter/
│   ├── instagram/
│   └── youtube/
└── prompt-knihovna/
    ├── prace/
    ├── kreativita/
    └── automatizace/
```
