#!/usr/bin/env python3
"""
AI-EDU-CZ — FastAPI server
Spusti: uvicorn server.main:app --reload --port 8765
nebo:   python server/main.py
"""

import sys
import os
import re
import json
import subprocess
import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

import database as db

PROJECT_ROOT = Path(__file__).parent.parent
STATIC_DIR   = Path(__file__).parent / "static"

app = FastAPI(title="AI-EDU-CZ Mission Control", docs_url=None, redoc_url=None)

# ── Static files ──────────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


# ── Security ──────────────────────────────────────────────────────────────────

SECRET_PATTERNS = [
    (r'sk-[a-zA-Z0-9]{20,}',                              'OpenAI API klíč'),
    (r'sk-ant-[a-zA-Z0-9\-]{10,}',                        'Anthropic API klíč'),
    (r'AIza[0-9A-Za-z\-_]{35}',                           'Google API klíč'),
    (r'ghp_[a-zA-Z0-9]{36}',                              'GitHub Personal Token'),
    (r'gho_[a-zA-Z0-9]{36}',                              'GitHub OAuth Token'),
    (r'xai-[a-zA-Z0-9]{30,}',                             'xAI/Grok API klíč'),
    (r'(?i)api[_\-]?key\s*[=:]\s*["\'][a-zA-Z0-9\-_]{10,}["\']', 'API Key v kódu'),
    (r'(?i)password\s*[=:]\s*["\'][^"\']{6,}["\']',       'Heslo v kódu'),
    (r'(?i)secret\s*[=:]\s*["\'][^"\']{6,}["\']',         'Secret v kódu'),
    (r'Bearer\s+[a-zA-Z0-9\-_\.]{20,}',                   'Bearer Token'),
    (r'-----BEGIN [A-Z ]+ PRIVATE KEY-----',               'Privátní klíč (PEM)'),
]
ENV_FILENAMES = {'.env', '.env.local', '.env.production', '.env.development',
                 '.env.staging', '.env.test'}
DANGEROUS_FILENAMES = {'credentials.json', 'secrets.json', 'service-account.json'}
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.astro', 'dist', '.venv', 'venv', 'data'}
SKIP_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip',
             '.mp4', '.mp3', '.wav', '.ttf', '.woff', '.woff2', '.pyc', '.db'}


def _is_gitignored(rel_path):
    r = subprocess.run(['git', 'check-ignore', '-q', str(rel_path)],
                       cwd=PROJECT_ROOT, capture_output=True)
    return r.returncode == 0


def scan_security() -> dict:
    issues = []
    files_scanned = 0
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            rel   = fpath.relative_to(PROJECT_ROOT)
            if fname in ENV_FILENAMES:
                if not _is_gitignored(rel):
                    issues.append({'file': str(rel), 'line': 0,
                                   'type': f'⚠ {fname} není v .gitignore',
                                   'preview': 'Přidej do .gitignore'})
                continue
            if fname in DANGEROUS_FILENAMES and not _is_gitignored(rel):
                issues.append({'file': str(rel), 'line': 0,
                               'type': 'Nebezpečný soubor není v .gitignore',
                               'preview': fname})
            if fpath.suffix.lower() in SKIP_EXTS:
                continue
            try:
                text = fpath.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            files_scanned += 1
            for pattern, label in SECRET_PATTERNS:
                for m in re.finditer(pattern, text):
                    ln = text[:m.start()].count('\n') + 1
                    preview = m.group()[:40] + ('…' if len(m.group()) > 40 else '')
                    issues.append({'file': str(rel), 'line': ln,
                                   'type': label, 'preview': preview})
    return {'ok': len(issues) == 0, 'issues': issues, 'files_scanned': files_scanned}


# ── Git helpers ───────────────────────────────────────────────────────────────

def run_git(args):
    r = subprocess.run(['git'] + args, cwd=PROJECT_ROOT,
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout.strip(), r.stderr.strip(), r.returncode


def generate_commit_msg():
    out, _, _ = run_git(['status', '--short'])
    if not out:
        return None
    paths = [l.strip()[3:] for l in out.splitlines() if l.strip()]
    buckets = []
    if any('SESSION' in p or 'PROGRESS' in p for p in paths):
        buckets.append('session update')
    if any('obsah/' in p for p in paths):
        buckets.append(f'content: {sum(1 for p in paths if "obsah/" in p)} lekcí')
    if any('strategie/' in p for p in paths):
        buckets.append('strategy')
    if any('server/' in p or 'dashboard' in p for p in paths):
        buckets.append('dashboard')
    if any('agenti/' in p for p in paths):
        buckets.append('agents')
    if not buckets:
        buckets.append(f'{len(paths)} files updated')
    return f"{', '.join(buckets)} [{datetime.date.today().isoformat()}]"


def do_push() -> tuple[bool, str, dict]:
    scan = scan_security()
    if not scan['ok']:
        return False, 'SECURITY: nalezeny problémy — push zablokován', scan
    msg = generate_commit_msg()
    if not msg:
        return True, 'Žádné změny k pushnutí.', scan
    run_git(['add', '-A'])
    _, err, code = run_git(['commit', '-m', msg])
    if code != 0 and 'nothing to commit' not in err:
        return False, f'Commit selhal: {err}', scan
    _, err, code = run_git(['push'])
    if code != 0:
        return False, f'Push selhal: {err}', scan
    return True, f'✓ Pushováno: "{msg}"', scan


# ── Progress / session helpers ────────────────────────────────────────────────

def get_progress():
    try:
        text = (PROJECT_ROOT / 'PROGRESS.md').read_text(encoding='utf-8')
        return text.count('✅'), text.count('✅') + text.count('⏳')
    except Exception:
        return 0, 35


def get_next_steps():
    try:
        text = (PROJECT_ROOT / 'SESSION.md').read_text(encoding='utf-8')
    except Exception:
        return []
    steps, capture = [], False
    for line in text.splitlines():
        if 'Příští kroky' in line:
            capture = True; continue
        if capture:
            if line.startswith('##'): break
            if re.match(r'^\d+\.', line.strip()):
                steps.append(line.strip())
    return steps[:5]


# ── API: Status ───────────────────────────────────────────────────────────────

@app.post("/api/status")
def api_status():
    done, total = get_progress()
    gs, _, _ = run_git(['status', '--short'])
    lc, _, _ = run_git(['log', '--oneline', '-7'])
    counts = db.count_items()
    return {
        'done': done, 'total': total,
        'git_status': gs or '— vše commitnuto',
        'last_commits': lc or '(žádné commity)',
        'next_steps': get_next_steps(),
        'feed_total': counts['total'],
        'feed_new': counts['new'],
    }


# ── API: Security + Push ──────────────────────────────────────────────────────

@app.post("/api/security-scan")
def api_security_scan():
    return scan_security()


@app.post("/api/push")
def api_push():
    ok, msg, scan = do_push()
    return {'ok': ok, 'message': msg, 'scan': scan}


# ── API: Session ──────────────────────────────────────────────────────────────

class NextStepsBody(BaseModel):
    next_steps: str = ""


class NoteBody(BaseModel):
    note: str


@app.post("/api/save-session")
def api_save_session(body: NextStepsBody):
    path = PROJECT_ROOT / 'SESSION.md'
    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return {'ok': False, 'message': str(e)}

    today = datetime.date.today().isoformat()
    now   = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    out, _, _ = run_git(['status', '--short'])
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    done_items = ('\n'.join(f'- Upraven soubor: `{l[3:]}`' for l in lines)
                  if lines else '- Žádné nové změny souborů v tomto session')

    content = re.sub(r'\*\*Datum:\*\*.*', f'**Datum:** {today}', content)

    done_marker = '## Co bylo uděláno v tomto sessionu'
    next_marker = '## Aktuální fáze projektu'
    done_block  = f'{done_marker}\n\n*Uloženo automaticky: {now}*\n\n{done_items}\n\n'
    pattern_done = re.compile(
        rf'{re.escape(done_marker)}.*?(?={re.escape(next_marker)})', re.DOTALL)
    if pattern_done.search(content):
        content = pattern_done.sub(done_block, content)

    if body.next_steps.strip():
        ns_marker   = '## Příští kroky — pro nový session'
        oq_marker   = '## Otevřené otázky'
        steps_lines = '\n'.join(
            f'{i+1}. {s.strip()}' for i, s in
            enumerate(body.next_steps.strip().splitlines()) if s.strip()
        )
        steps_block = f'{ns_marker}\n\n{steps_lines}\n\n'
        pattern_steps = re.compile(
            rf'{re.escape(ns_marker)}.*?(?={re.escape(oq_marker)})', re.DOTALL)
        if pattern_steps.search(content):
            content = pattern_steps.sub(steps_block, content)

    try:
        path.write_text(content, encoding='utf-8')
    except Exception as e:
        return {'ok': False, 'message': f'Zápis SESSION.md selhal: {e}'}

    scan = scan_security()
    if not scan['ok']:
        issues = scan['issues']
        detail = '; '.join(f"{i['type']} ({i['file']})" for i in issues[:3])
        return {'ok': False, 'message': f'SECURITY BLOK: {len(issues)} problém(ů) — {detail}'}

    run_git(['add', '-A'])
    msg = generate_commit_msg() or f'session save [{today}]'
    _, err, code = run_git(['commit', '-m', msg])
    if code != 0 and 'nothing to commit' not in err:
        return {'ok': False, 'message': f'Commit selhal: {err}'}
    _, err, code = run_git(['push'])
    if code != 0:
        return {'ok': False, 'message': f'SESSION.md uložen lokálně, push selhal: {err}'}

    return {'ok': True, 'message': f'✓ Security OK · Session uložen · "{msg}"'}


@app.post("/api/add-note")
def api_add_note(body: NoteBody):
    path = PROJECT_ROOT / 'SESSION.md'
    try:
        content = path.read_text(encoding='utf-8')
        today = datetime.date.today().isoformat()
        content = re.sub(r'\*\*Datum:\*\*.*', f'**Datum:** {today}', content)
        marker = '## Co bylo uděláno v tomto sessionu'
        block  = f'\n### Poznámka {today}\n{body.note}\n'
        content = content.replace(marker, marker + block, 1)
        path.write_text(content, encoding='utf-8')
        return {'ok': True, 'message': 'Poznámka přidána do SESSION.md'}
    except Exception as e:
        return {'ok': False, 'message': str(e)}


# ── API: Feed ─────────────────────────────────────────────────────────────────

@app.get("/api/feed")
def api_feed(limit: int = 50, offset: int = 0,
             source: str = None, processed: int = None):
    items = db.get_items(limit=limit, offset=offset,
                         source=source,
                         processed=processed if processed is not None else None)
    counts = db.count_items()
    return {'items': items, 'counts': counts}


@app.post("/api/feed/fetch")
def api_feed_fetch(background_tasks: BackgroundTasks):
    """Spustí RSS agenta na pozadí."""
    def _run():
        from agenti.rss_agent import run as rss_run
        rss_run(verbose=False)

    background_tasks.add_task(_run)
    return {'ok': True, 'message': 'RSS agent spuštěn na pozadí. Obnoř stránku za chvíli.'}


@app.get("/api/feed/{item_id}")
def api_feed_item(item_id: int):
    item = db.get_item(item_id)
    if not item:
        return JSONResponse({'error': 'Položka nenalezena'}, status_code=404)
    generated = db.get_generated(item_id)
    return {'item': item, 'generated': generated}


# ── Startup ───────────────────────────────────────────────────────────────────

@app.on_event("startup")
def startup():
    db.init_db()


# ── Dev runner ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    print("\n  🤖 AI-EDU-CZ Mission Control (FastAPI)")
    print("  ────────────────────────────────────────")
    print("  http://localhost:8765\n")
    uvicorn.run("server.main:app", host="localhost", port=8765,
                reload=True, reload_dirs=[str(PROJECT_ROOT)])
