# Automatizace — n8n workflows a skripty

Tato složka obsahuje workflow soubory pro n8n a automatizační skripty.

## Plánované workflow

| Workflow | Soubor | Popis | Status |
|----------|--------|-------|--------|
| Týdenní newsletter | `newsletter-weekly.json` | Grok → Claude → Resend | ⏳ Todo |
| Daily social post | `social-daily.json` | Novinky → tweet + IG caption | ⏳ Todo |
| Session backup | `session-backup.json` | Auto-záloha na konci dne | ⏳ Todo |
| Content pipeline | `content-pipeline.json` | Lekce → multi-channel output | ⏳ Todo |

## n8n setup (lokálně)

```bash
# Instalace přes npm (Node.js potřeba)
npm install -g n8n

# Spuštění
n8n start
# Otevři: http://localhost:5678
```

## Import workflow

1. Otevři n8n (`http://localhost:5678`)
2. Klikni na **+** → **Import from file**
3. Vyber `.json` soubor z této složky
