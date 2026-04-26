# Agent Architektura — Jak spolupracují AI modely v projektu

## Přehled architektury

```
                    ┌─────────────────────┐
                    │    RADEK (člověk)   │
                    │   zadává směr       │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   CLAUDE CODE       │
                    │  (Mozek projektu)   │
                    │  Orchestrátor       │
                    └──┬───┬───┬───┬──────┘
                       │   │   │   │
          ┌────────────┘   │   │   └────────────┐
          │                │   │                │
   ┌──────▼──────┐  ┌──────▼───▼──────┐  ┌─────▼───────┐
   │   GROK      │  │   PERPLEXITY    │  │   GEMINI    │
   │  Novinky    │  │   Research      │  │  Dokumenty  │
   │  Twitter    │  │   Fakta         │  │  YouTube    │
   └─────────────┘  └─────────────────┘  └─────────────┘
          │                │                     │
          └────────────────┴─────────────────────┘
                           │
                    ┌──────▼──────────┐
                    │   CHATGPT       │
                    │  Alternativní   │
                    │  perspektivy    │
                    │  DALL-E obrázky │
                    └─────────────────┘
```

## Role každého AI modelu

### Claude Code — Orchestrátor (mozek)
**Co dělá:**
- Přijímá zadání od Radka
- Rozděluje úkoly ostatním modelům
- Syntetizuje výstupy do finálního obsahu
- Udržuje konzistenci celé platformy
- Rozhoduje o struktuře a strategii
- Generuje dlouhý, komplexní obsah (lekce, tutoriály)

**Kdy ho použít:**
- Plánování strategie
- Psaní dlouhých lekcí
- Revize a editace obsahu
- Technické úkoly (kód, automatizace)
- Finální kontrola kvality

**Free tier:** Dostupný v Claude.ai (omezený) nebo přes API

---

### Grok (xAI) — Novinky a Twitter
**Co dělá:**
- Sleduje aktuální AI novinky v reálném čase
- Generuje Twitter/X posty
- Analyzuje trendy v AI komunitě
- Research z X/Twitter diskusí

**Kdy ho použít:**
- "Jaké jsou nejnovější AI novinky tento týden?"
- "Napiš tweet o vydání GPT-5"
- "Co lidé na Twitteru říkají o [AI téma]?"

**Free tier:** Dostupný přes xAI/Grok zdarma (s limity)

---

### Perplexity — Research a fakta
**Co dělá:**
- Hledá přesné, citované informace
- Verifikuje fakta
- Research pro obsah lekcí
- Přehled studií a výzkumů

**Kdy ho použít:**
- "Najdi mi statistiky o využití AI v ČR"
- "Jaké jsou nejnovější benchmarky GPT vs. Claude?"
- "Ověř toto tvrzení: [X]"

**Free tier:** Perplexity.ai má velkorysý free tier

---

### Gemini — Dokumenty a multimodal
**Co dělá:**
- Zpracování dlouhých dokumentů (PDF, Google Docs)
- Analýza obrázků a screenshotů
- Integrace s Google Workspace
- YouTube popis a titulky

**Kdy ho použít:**
- "Shrň mi tento PDF dokument"
- "Napiš popis k YouTube videu"
- "Analyzuj tento screenshot aplikace"

**Free tier:** Gemini.google.com zdarma

---

### ChatGPT — Alternativní pohled a obrázky
**Co dělá:**
- Alternativní perspektivy k obsahu
- DALL-E 3 generování obrázků pro posty
- GPT-4o Vision analýza obrázků
- Testování promptů z lekcí

**Kdy ho použít:**
- "Vygeneruj obrázek pro Instagram post o AI"
- "Jak by vysvětlil GPT toto téma?"
- Testování promptů, co učíme uživatele

**Free tier:** ChatGPT.com má GPT-4o s limity zdarma

---

## Workflow pro tvorbu obsahu

### 1. Plánování lekce (Claude Code)
```
Radek → Claude Code: "Chci lekci o ChatGPT pro začátečníky"
Claude Code: Vytvoří osnovu, strukturu, klíčové body
```

### 2. Research (Perplexity + Grok)
```
Claude Code → Perplexity: "Najdi aktuální statistiky o ChatGPT"
Claude Code → Grok: "Jaké jsou nejnovější novinky o ChatGPT?"
```

### 3. Tvorba obsahu (Claude Code)
```
Claude Code: Napíše lekci na základě osnovy + research dat
```

### 4. Vizuály (ChatGPT/DALL-E)
```
Claude Code → ChatGPT: "Vygeneruj infografiku k lekci"
```

### 5. Multi-channel adaptace
```
Claude Code: Zkrátí lekci na Twitter thread (10 tweetů)
Claude Code: Vytvoří Instagram popis + hashtags
Claude Code: Napíše YouTube popis a titulky
Gemini: Přidá do YouTube dokumentace
```

### 6. Publikace
```
Radek: Zkontroluje, schválí, publikuje
```

---

## Automatizace workflow (fáze 2)

Jakmile bude platforma stabilní, zapojíme **n8n** (open-source):

```
Každý pondělí:
n8n → Grok: "Jaké jsou AI novinky tento týden?"
n8n → Claude Code: "Napiš newsletter shrnutí"
n8n → Resend: Odešle email subscribers

Každý den:
n8n → Grok: "Jedna AI novinka dnes"
n8n → Claude Code: "Napiš tweet a Instagram caption"
n8n: Uloží do fronty pro manuální schválení
```

---

## Náklady na AI modely

| Model | Free tier | Placený plán |
|-------|-----------|--------------|
| Claude | Claude.ai (omezený) | $20/měs (Pro) |
| ChatGPT | GPT-4o (omezený) | $20/měs (Plus) |
| Gemini | Velmi velkorysý free | $19.99/měs |
| Grok | Dostupný zdarma | V X Premium |
| Perplexity | Velkorysý free | $20/měs (Pro) |

**Strategie:** Začít se zdarma plány. Kombinovat modely tak, aby se limity nekumulovaly na jeden model.
