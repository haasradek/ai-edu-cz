# Agenti — AI skripty a automatizace

Tato složka obsahuje Python skripty pro AI agenty projektu.

## Plánovaní agenti

| Agent | Soubor | Popis | Status |
|-------|--------|-------|--------|
| News agent | `news-agent.py` | Sbírá denní AI novinky (Grok + Perplexity) | ⏳ Todo |
| Content agent | `content-agent.py` | Generuje obsah pro sociální sítě | ⏳ Todo |
| Research agent | `research-agent.py` | Hloubkový research pro lekce | ⏳ Todo |
| Summary agent | `summary-agent.py` | Denní shrnutí projektu | ⏳ Todo |

## Jak spustit agenta

```bash
# Ujisti se, že máš vyplněné klíče v .env
python agenti/news-agent.py
```

## Závislosti (instalace)

```bash
pip install anthropic openai python-dotenv requests
```
