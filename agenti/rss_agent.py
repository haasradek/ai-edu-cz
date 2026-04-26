#!/usr/bin/env python3
"""
AI-EDU-CZ — RSS Agent
Stahuje novinky ze svobodných RSS feedů a ukládá do SQLite DB.
Spusti: python agenti/rss_agent.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import feedparser
import trafilatura
from datetime import datetime, timezone
from database import init_db, upsert_item

# ── Seznam RSS feedů (všechny zdarma) ────────────────────────────────────────

FEEDS = [
    # Anglické AI zdroje
    {"url": "https://www.anthropic.com/rss.xml",               "source": "Anthropic Blog"},
    {"url": "https://openai.com/news/rss.xml",                 "source": "OpenAI Blog"},
    {"url": "https://techcrunch.com/category/artificial-intelligence/feed/", "source": "TechCrunch AI"},
    {"url": "https://venturebeat.com/category/ai/feed/",       "source": "VentureBeat AI"},
    {"url": "https://hnrss.org/newest?q=LLM+AI+Claude+ChatGPT&points=10", "source": "HackerNews AI"},
    {"url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml", "source": "The Verge AI"},
    # České / slovenské zdroje
    {"url": "https://news.google.com/rss/search?q=umela+inteligence&hl=cs&gl=CZ&ceid=CZ:cs", "source": "Google News CZ"},
    {"url": "https://news.google.com/rss/search?q=AI+umela+inteligencia&hl=sk&gl=SK&ceid=SK:sk", "source": "Google News SK"},
    {"url": "https://www.lupa.cz/rss/clanky/",                "source": "Lupa.cz"},
    {"url": "https://www.root.cz/rss/clanky/",               "source": "Root.cz"},
]

MAX_PER_FEED = 20  # max článků z jednoho feedu na jedno spuštění
FETCH_FULLTEXT = False  # True = pomalejší, ale máme plný text přes trafilatura


def _parse_date(entry) -> str | None:
    """Vrátí ISO datum z feedparser entry."""
    t = entry.get("published_parsed") or entry.get("updated_parsed")
    if t:
        try:
            return datetime(*t[:6], tzinfo=timezone.utc).isoformat()
        except Exception:
            pass
    return None


def _fetch_fulltext(url: str) -> str | None:
    """Stáhne plný text článku přes trafilatura (zdarma)."""
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return trafilatura.extract(downloaded, include_comments=False,
                                       include_tables=False)
    except Exception:
        pass
    return None


def run(verbose: bool = True) -> dict:
    """
    Projde všechny RSS feedy, uloží nové položky do DB.
    Vrátí {'fetched': int, 'new': int, 'sources': list}.
    """
    init_db()
    total_fetched = 0
    total_new = 0
    source_stats = []

    for feed_cfg in FEEDS:
        feed_url = feed_cfg["url"]
        source   = feed_cfg["source"]

        try:
            parsed = feedparser.parse(feed_url)
        except Exception as e:
            if verbose:
                print(f"  ✗ {source}: chyba parsování — {e}")
            continue

        entries = parsed.entries[:MAX_PER_FEED]
        new_count = 0

        for entry in entries:
            url   = entry.get("link", "").strip()
            title = entry.get("title", "").strip()
            if not url or not title:
                continue

            summary = entry.get("summary", "") or entry.get("description", "") or ""
            # Odstraň HTML tagy ze summary
            import re
            summary = re.sub(r"<[^>]+>", "", summary).strip()[:500]

            published_at = _parse_date(entry)
            content = _fetch_fulltext(url) if FETCH_FULLTEXT else None

            item_id = upsert_item(
                url=url,
                title=title,
                source=source,
                published_at=published_at,
                content=content,
                summary=summary,
            )
            if item_id:
                new_count += 1

        total_fetched += len(entries)
        total_new += new_count
        source_stats.append({"source": source, "fetched": len(entries), "new": new_count})

        if verbose:
            status = f"+{new_count} nových" if new_count else "vše již uloženo"
            print(f"  {'✓' if new_count else '·'} {source}: {len(entries)} položek, {status}")

    if verbose:
        print(f"\n  Celkem: {total_fetched} načteno, {total_new} nových uloženo do DB")

    return {"fetched": total_fetched, "new": total_new, "sources": source_stats}


if __name__ == "__main__":
    print("\n🤖 AI-EDU-CZ RSS Agent\n")
    run(verbose=True)
