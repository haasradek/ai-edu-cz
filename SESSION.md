# Session State — AI-EDU-CZ

> Tento soubor se aktualizuje na konci každého sessionu. Při zahájení nového sessionu ho Claude přečte jako první.

---

## Poslední update
**Datum:** 2026-04-26  
**Session číslo:** 1  
**Claude model:** claude-sonnet-4-6

---

## Co bylo uděláno v tomto sessionu

- Zahájen projekt AI-EDU-CZ — vzdělávací platforma o AI pro CZ/SK
- Vytvořen CLAUDE.md s celkovou strategií a rolemi AI modelů
- Vytvořena složka `strategie/` s dokumenty: vize, agent-architektura, obsahový plán, monetizace
- Vytvořena první lekce: `obsah/modul-1-zaklady/01-co-je-ai.md`
- Vytvořena prompt knihovna: emailové šablony
- Vytvořena Twitter thread šablona
- Vytvořen dashboard systém (SESSION.md, PROGRESS.md, dashboard.py)
- Inicializován git repozitář (master branch)
- Vytvořen GitHub repozitář: https://github.com/haasradek/ai-edu-cz
- Proveden první push (HTTPS, uživatel haasradek)

---

## Aktuální fáze projektu

**Fáze:** 1 — Lokální platforma a obsah  
**Sprint:** Sprint 1 (Duben–Květen 2026) — Základy AI

**Co je hotovo:**
- [x] Základní struktura projektu
- [x] Strategické dokumenty (vize, architektura, plán)
- [x] První lekce (Modul 1, Lekce 1)
- [x] Prompt knihovna — start
- [x] Dashboard + GitHub integrace

**Co je in progress:**
- [ ] Modul 1 dokončit (lekcí 2-6)
- [ ] Modul 2 — Přehled nástrojů

---

## Příští kroky — pro nový session

1. Napsat Lekci 2: "Jak AI myslí — co je velký jazykový model?"
2. Napsat Lekci 3: "Přehled AI nástrojů 2026 — který si vybrat?"
3. Vytvořit ChatGPT průvodce pro začátečníky (Modul 2)
4. Rozšířit prompt knihovnu (kreativita + automatizace)
5. Zvážit Obsidian vault setup pro lepší lokální čtení

---

## Otevřené otázky / Rozhodnutí k řešení

- Jaká doména pro web? (ai-edu.cz / aieducz.cz / nauc-se-ai.cz)
- Kdy spustit Twitter účet?
- Obsidian vs. VS Code jako čtečka lokální platformy?

---

## Klíčová rozhodnutí z tohoto sessionu

- Claude Code = orchestrátor, mozek projektu
- Grok = novinky + Twitter, Perplexity = research, Gemini = dokumenty, GPT = obrázky
- Web stack: Astro + GitHub Pages (zdarma)
- Monetizace: rok 1 zdarma, pak kurzy + konzultace
- n8n místo Make/Zapier (open-source, vlastní hosting)

---

## Soubory projektu (aktuální stav)

```
ai-edu-cz/
├── CLAUDE.md                              ✅ Hotovo
├── SESSION.md                             ✅ Tento soubor
├── PROGRESS.md                            ✅ Hotovo
├── dashboard.py                           ✅ Hotovo
├── scripts/
│   ├── save-session.ps1                   ✅ Hotovo
│   └── push-github.ps1                    ✅ Hotovo
├── strategie/
│   ├── vize.md                            ✅ Hotovo
│   ├── agent-architektura.md              ✅ Hotovo
│   ├── obsahovy-plan.md                   ✅ Hotovo
│   └── monetizace.md                      ✅ Hotovo
├── obsah/
│   └── modul-1-zaklady/
│       └── 01-co-je-ai.md                 ✅ Hotovo
├── prompt-knihovna/
│   └── prace/
│       └── email-sablony.md               ✅ Hotovo
└── sablony/
    └── twitter/
        └── thread-sablona.md              ✅ Hotovo
```
