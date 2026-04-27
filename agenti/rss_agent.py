#!/usr/bin/env python3
"""
AI-EDU-CZ — RSS Agent
Stahuje AI novinky, detekuje témata (tagy), ukládá do SQLite DB.
"""

import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import feedparser
import trafilatura
from datetime import datetime, timezone
from database import init_db, upsert_item

# ── Feedy ─────────────────────────────────────────────────────────────────────

FEEDS = [
    {"url": "https://www.anthropic.com/blog/rss",
     "source": "Anthropic Blog"},
    {"url": "https://openai.com/news/rss.xml",
     "source": "OpenAI Blog",       "filter_ai": True},
    {"url": "https://techcrunch.com/category/artificial-intelligence/feed/",
     "source": "TechCrunch AI"},
    {"url": "https://venturebeat.com/category/ai/feed/",
     "source": "VentureBeat AI"},
    {"url": "https://hnrss.org/newest?q=AI+LLM+ChatGPT+Claude&points=15",
     "source": "HackerNews AI"},
    {"url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
     "source": "The Verge AI"},
    {"url": "https://news.google.com/rss/search?q=%22um%C4%9Bl%C3%A1+inteligence%22+OR+%22ChatGPT%22+OR+%22Claude%22+OR+%22Gemini%22&hl=cs&gl=CZ&ceid=CZ:cs",
     "source": "Google News CZ"},
    {"url": "https://news.google.com/rss/search?q=%22umel%C3%A1+inteligencia%22+OR+%22ChatGPT%22+OR+%22Claude%22+OR+%22Gemini%22&hl=sk&gl=SK&ceid=SK:sk",
     "source": "Google News SK"},
    {"url": "https://www.lupa.cz/rss/clanky/",
     "source": "Lupa.cz",           "filter_ai": True},
    {"url": "https://www.root.cz/rss/clanky/",
     "source": "Root.cz",           "filter_ai": True},
]

MAX_PER_FEED = 25
FETCH_FULLTEXT = True   # stáhne plný text článku přes trafilatura → lepší generování

# ── Filtrovací klíčová slova (musí být aspoň jedno) ───────────────────────────

AI_KEYWORDS = [
    "ChatGPT", "Claude", "Gemini", "Grok", "Llama", "Copilot", "Mistral",
    "GPT-4", "GPT-4o", "o1", "o3", "Sora", "Midjourney", "DALL-E",
    "Anthropic", "OpenAI", "Google DeepMind", "Meta AI", "xAI",
    "LLM", "large language model", "velký jazykový model",
    "AI agent", "AI agenti", "generativní AI", "generative AI",
    "umělá inteligence", "umelá inteligencia",
    "machine learning", "strojové učení",
    "neural network", "neuronová síť",
    "prompt", "fine-tuning", "RAG", "vector database",
]

_AI_RE = re.compile(
    "|".join(r"\b" + re.escape(k) + r"\b" for k in AI_KEYWORDS),
    re.IGNORECASE
)

# ── Tagy — co konkrétně je v článku zmíněno ───────────────────────────────────

TAG_RULES = [
    ("Claude",      ["claude", "anthropic", "claude code", "claude cowork",
                     "claude opus", "claude sonnet", "claude haiku"]),
    ("ChatGPT",     ["chatgpt", "openai", "gpt-4", "gpt-4o", "gpt4", "o1 ", "o3 ",
                     "sora", "dall-e", "whisper"]),
    ("Gemini",      ["gemini", "google deepmind", "google ai", "bard", "google gemma",
                     "notebooklm"]),
    ("Grok",        ["grok", "xai", "x.ai"]),
    ("Llama",       ["llama", "meta ai", "meta llama"]),
    ("Copilot",     ["copilot", "github copilot", "microsoft ai", "bing ai"]),
    ("Mistral",     ["mistral"]),
    ("Perplexity",  ["perplexity"]),
    ("Midjourney",  ["midjourney"]),
    ("Sora",        ["sora"]),
    ("LLM",         ["large language model", "velký jazykový model", "llm"]),
    ("Agenti",      ["ai agent", "ai agenti", "multi-agent", "agentic"]),
]

def detect_tags(title: str, summary: str) -> list[str]:
    text = (title + " " + summary).lower()
    tags = []
    for tag, keywords in TAG_RULES:
        if any(kw in text for kw in keywords):
            tags.append(tag)
    return tags


def _is_ai_relevant(title: str, summary: str) -> bool:
    return bool(_AI_RE.search(title) or _AI_RE.search(summary))


def _parse_date(entry) -> str | None:
    t = entry.get("published_parsed") or entry.get("updated_parsed")
    if t:
        try:
            return datetime(*t[:6], tzinfo=timezone.utc).isoformat()
        except Exception:
            pass
    return None


def _fetch_fulltext(url: str) -> str | None:
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return trafilatura.extract(downloaded, include_comments=False,
                                       include_tables=False)
    except Exception:
        pass
    return None


def run(verbose: bool = True) -> dict:
    init_db()
    total_fetched = 0
    total_new = 0
    total_skipped = 0
    source_stats = []

    for feed_cfg in FEEDS:
        feed_url  = feed_cfg["url"]
        source    = feed_cfg["source"]
        filter_ai = feed_cfg.get("filter_ai", False)

        try:
            parsed = feedparser.parse(feed_url)
        except Exception as e:
            if verbose:
                print(f"  x {source}: chyba — {e}")
            continue

        if not parsed.entries:
            if verbose:
                print(f"  - {source}: zadne polozky (HTTP {parsed.get('status','?')})")
            continue

        entries    = parsed.entries[:MAX_PER_FEED]
        new_count  = 0
        skip_count = 0

        for entry in entries:
            url   = entry.get("link", "").strip()
            title = entry.get("title", "").strip()
            if not url or not title:
                continue

            summary = entry.get("summary", "") or entry.get("description", "") or ""
            summary = re.sub(r"<[^>]+>", "", summary).strip()[:500]

            if filter_ai and not _is_ai_relevant(title, summary):
                skip_count += 1
                continue

            published_at = _parse_date(entry)
            tags         = detect_tags(title, summary)
            content      = _fetch_fulltext(url) if FETCH_FULLTEXT else None

            item_id = upsert_item(
                url=url, title=title, source=source,
                published_at=published_at, content=content,
                summary=summary, tags=tags,
            )
            if item_id:
                new_count += 1

        total_fetched  += len(entries)
        total_new      += new_count
        total_skipped  += skip_count
        source_stats.append({"source": source, "fetched": len(entries),
                              "new": new_count, "skipped": skip_count})

        if verbose:
            parts = [f"+{new_count} novych"]
            if skip_count:
                parts.append(f"{skip_count} preskoceno")
            if new_count == 0 and skip_count == 0:
                parts = ["vse jiz ulozeno"]
            print(f"  {'+'if new_count else '.'} {source}: {', '.join(parts)}")

    if verbose:
        print(f"\n  Celkem: {total_fetched} stazeno, {total_new} novych, "
              f"{total_skipped} preskoceno")

    return {"fetched": total_fetched, "new": total_new,
            "skipped": total_skipped, "sources": source_stats}


if __name__ == "__main__":
    print("AI-EDU-CZ RSS Agent\n")
    run(verbose=True)
