#!/usr/bin/env python3
"""
AI-EDU-CZ — Content Agent
Generuje vzdělávací obsah z RSS článků pomocí Claude API.
Platformy: article, twitter, instagram, youtube
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Načti .env ručně — bez závislosti na python-dotenv
_env = Path(__file__).parent.parent / ".env"
if _env.exists():
    for _line in _env.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip().strip("\"'"))

import anthropic
import database as db

MODEL      = "claude-sonnet-4-6"
MAX_TOKENS = 2048

PLATFORMS = {
    "article":   "Článek (blog)",
    "twitter":   "Twitter thread",
    "instagram": "Instagram post",
    "youtube":   "YouTube scénář",
}


def _prompt(platform: str, title: str, source: str, summary: str) -> str:
    ctx = f"Název: {title}\nZdroj: {source}\nShrnutí: {summary or '(není k dispozici)'}"

    if platform == "article":
        return f"""Jsi redaktor vzdělávacího blogu AI-EDU-CZ — nejlepšího česky psaného zdroje o AI.

Na základě níže uvedené novinky napiš vzdělávací článek v češtině (600–1000 slov).

{ctx}

Struktura:
## [Poutavý název v češtině]

**Úvod** — co se stalo a proč to zajímá česky mluvící čtenáře (2–3 věty).
**Co to znamená** — jednoduché vysvětlení, bez odborného žargonu.
**Proč na tom záleží** — dopad na každodenní život nebo práci.
**Jak to využít** — 3–5 konkrétních praktických tipů.
**Závěr** — shrnutí a co sledovat dál.

Piš přátelsky, srozumitelně. Cílová skupina: lidé, kteří AI teprve poznávají."""

    if platform == "twitter":
        return f"""Jsi social media manažer projektu AI-EDU-CZ.

Na základě novinky napiš Twitter thread v češtině (5–7 tweetů).

{ctx}

Formát — každý tweet na nový řádek, odděl prázdným řádkem:
1/ Silný hook — záchytná věta, max 280 znaků
2/ Klíčová informace č. 1
3/ Klíčová informace č. 2
4/ Klíčová informace č. 3
5/ Praktický tip pro běžného uživatele
6/ Výzva k akci + sledujte AI-EDU-CZ

Max 280 znaků na tweet."""

    if platform == "instagram":
        return f"""Jsi social media manažer Instagram účtu AI-EDU-CZ.

Na základě novinky napiš Instagram příspěvek v češtině.

{ctx}

Struktura:
🔥 [Vizuální hook — první věta co lidi uvidí]

[Tělo: 3–4 krátké odstavce s emoji, přátelský tón]

[Výzva k akci — otázka nebo výzva ke sdílení]

.
.
.
#ai #umělainteligence [dalších 13–17 hashtagů, česky i anglicky]

Max 1500 znaků textu (bez hashtagů)."""

    if platform == "youtube":
        return f"""Jsi scriptwriter pro YouTube kanál AI-EDU-CZ.

Na základě novinky napiš scénář pro vzdělávací video (4–6 minut) v češtině.

{ctx}

Struktura:
## HOOK [0:00–0:20]
Poutavý úvod — co se dozvíš, proč zůstat

## ÚVOD [0:20–0:45]
Krátké představení tématu

## HLAVNÍ OBSAH [0:45–4:00]
2–3 sekce s nadpisy, přidej [VIZUÁL: co ukázat] kde je to relevantní

## PRAKTICKÝ TIP [4:00–5:00]
Konkrétní věc, kterou divák může hned vyzkoušet

## OUTRO [5:00–5:30]
Shrnutí + výzva k odběru + co příště

Piš přirozeně, hovorově."""

    raise ValueError(f"Neznámá platforma: {platform}")


def generate(item_id: int, platforms: list[str]) -> dict:
    """
    Vygeneruje obsah pro zadané platformy a uloží do DB.
    Vrátí dict: {platform: {"content": str, "generated_id": int, "label": str}}
    """
    item = db.get_item(item_id)
    if not item:
        raise ValueError(f"Položka #{item_id} nenalezena v DB")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY není nastaven v .env")

    title   = item["title"]
    source  = item["source"]
    summary = item.get("summary") or ""

    client  = anthropic.Anthropic(api_key=api_key)
    results = {}

    for platform in platforms:
        if platform not in PLATFORMS:
            continue
        prompt  = _prompt(platform, title, source, summary)
        message = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        content = message.content[0].text
        gen_id  = db.save_generated(item_id=item_id, type=platform, content=content)
        results[platform] = {
            "content":      content,
            "generated_id": gen_id,
            "label":        PLATFORMS[platform],
        }

    if results:
        db.mark_processed(item_id)

    return results


if __name__ == "__main__":
    item_id   = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    platforms = sys.argv[2].split(",") if len(sys.argv) > 2 else ["article"]
    print(f"Generuji {platforms} pro item #{item_id}…\n")
    out = generate(item_id, platforms)
    for p, r in out.items():
        print(f"=== {r['label']} (generated_id={r['generated_id']}) ===")
        print(r["content"][:400] + "…\n")
