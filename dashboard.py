#!/usr/bin/env python3
"""
AI-EDU-CZ Dashboard — Mission Control
Spusti: python dashboard.py  |  Otevri: http://localhost:8765
"""

import http.server
import json
import os
import re
import subprocess
import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
PORT = 8765

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

DANGEROUS_FILENAMES = {'.env', '.env.local', '.env.production', '.env.development',
                       'credentials.json', 'secrets.json', 'service-account.json'}

SKIP_DIRS  = {'.git', '__pycache__', 'node_modules', '.astro', 'dist', '.venv', 'venv'}
SKIP_EXTS  = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip',
              '.mp4', '.mp3', '.wav', '.ttf', '.woff', '.woff2', '.pyc'}


def scan_security():
    issues = []
    files_scanned = 0

    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            rel = fpath.relative_to(PROJECT_ROOT)

            if fname in DANGEROUS_FILENAMES:
                # Check if properly gitignored
                r = subprocess.run(['git', 'check-ignore', '-q', str(rel)],
                                   cwd=PROJECT_ROOT, capture_output=True)
                if r.returncode != 0:
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
                    line_no = text[:m.start()].count('\n') + 1
                    preview = m.group()[:40] + ('…' if len(m.group()) > 40 else '')
                    issues.append({'file': str(rel), 'line': line_no,
                                   'type': label, 'preview': preview})

    return {'ok': len(issues) == 0, 'issues': issues, 'files_scanned': files_scanned}


# ── Git helpers ───────────────────────────────────────────────────────────────

def run_git(args):
    r = subprocess.run(['git'] + args, cwd=PROJECT_ROOT,
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout.strip(), r.stderr.strip(), r.returncode


def generate_commit_msg():
    changed_out, _, _ = run_git(['status', '--short'])
    if not changed_out:
        return None

    lines = [l.strip() for l in changed_out.splitlines() if l.strip()]
    paths = [l[3:] for l in lines]

    buckets = []
    if any('SESSION' in p or 'PROGRESS' in p for p in paths):
        buckets.append('session update')
    lekce = [p for p in paths if 'obsah/' in p]
    if lekce:
        buckets.append(f'content: {len(lekce)} lekce')
    if any('strategie/' in p for p in paths):
        buckets.append('strategy')
    if any('dashboard' in p for p in paths):
        buckets.append('dashboard')
    if any('scripts/' in p or 'prompt-knihovna/' in p for p in paths):
        buckets.append('tools')
    if any('sablony/' in p for p in paths):
        buckets.append('templates')
    if not buckets:
        buckets.append(f'{len(paths)} files updated')

    date = datetime.date.today().isoformat()
    return f"{', '.join(buckets)} [{date}]"


def do_push_github():
    # 1. Security scan
    scan = scan_security()
    if not scan['ok']:
        return False, 'SECURITY: nalezeny problémy — push zablokován', scan

    # 2. Auto commit message
    msg = generate_commit_msg()
    if msg is None:
        return True, 'Žádné změny k pushnutí.', scan

    # 3. Commit + push
    run_git(['add', '-A'])
    _, err, code = run_git(['commit', '-m', msg])
    if code != 0 and 'nothing to commit' not in err:
        return False, f'Commit selhal: {err}', scan

    _, err, code = run_git(['push'])
    if code != 0:
        return False, f'Push selhal: {err}', scan

    return True, f'✓ Pushováno: "{msg}"', scan


# ── Status data ───────────────────────────────────────────────────────────────

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
            capture = True
            continue
        if capture:
            if line.startswith('##'):
                break
            if re.match(r'^\d+\.', line.strip()):
                steps.append(line.strip())
    return steps[:5]


def get_git_status():
    out, _, _ = run_git(['status', '--short'])
    return out or '— vše commitnuto'


def get_last_commits():
    out, _, _ = run_git(['log', '--oneline', '-7'])
    return out or '(žádné commity)'


# ── HTML ─────────────────────────────────────────────────────────────────────

HTML = r"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI-EDU-CZ · Mission Control</title>
<style>
:root{
  --bg:#000;--bg1:rgba(255,255,255,.03);--bg2:rgba(255,255,255,.06);
  --border:rgba(255,255,255,.07);--border2:rgba(255,255,255,.14);
  --c:#00d4ff;--c2:#7c3aed;--c3:#00ff88;--red:#ff3355;--yellow:#ffaa00;
  --txt:#e8eaf0;--muted:#556;
  --r:16px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:var(--bg);color:var(--txt);min-height:100vh;
  background-image:
    radial-gradient(ellipse 80% 60% at 10% 10%,rgba(0,212,255,.06) 0%,transparent 60%),
    radial-gradient(ellipse 60% 80% at 90% 90%,rgba(124,58,237,.07) 0%,transparent 60%),
    repeating-linear-gradient(0deg,transparent,transparent 59px,rgba(255,255,255,.02) 59px,rgba(255,255,255,.02) 60px),
    repeating-linear-gradient(90deg,transparent,transparent 59px,rgba(255,255,255,.02) 59px,rgba(255,255,255,.02) 60px);
}

/* Header */
header{
  padding:28px 36px 24px;
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  background:rgba(0,0,0,.6);backdrop-filter:blur(20px);
  position:sticky;top:0;z-index:50;
}
.logo{display:flex;align-items:center;gap:14px}
.logo-icon{
  width:42px;height:42px;border-radius:12px;
  background:linear-gradient(135deg,var(--c),var(--c2));
  display:flex;align-items:center;justify-content:center;
  font-size:1.3rem;box-shadow:0 0 20px rgba(0,212,255,.3);
}
.logo h1{font-size:1.25rem;font-weight:700;letter-spacing:-.02em}
.logo h1 span{color:var(--c)}
.logo p{font-size:.75rem;color:var(--muted);margin-top:2px}
#clock{font-size:.8rem;color:var(--muted);text-align:right}
#clock b{display:block;font-size:1rem;color:var(--txt);font-variant-numeric:tabular-nums}

/* Layout */
.wrap{max-width:1200px;margin:0 auto;padding:32px 24px}
.grid{display:grid;gap:18px}
.grid-3{grid-template-columns:repeat(3,1fr)}
.grid-2{grid-template-columns:repeat(2,1fr)}
@media(max-width:900px){.grid-3,.grid-2{grid-template-columns:1fr}}

/* Card */
.card{
  background:var(--bg1);
  border:1px solid var(--border);
  border-radius:var(--r);
  padding:24px;
  transition:border-color .2s;
}
.card:hover{border-color:var(--border2)}
.card-label{
  font-size:.7rem;font-weight:700;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);
  margin-bottom:18px;display:flex;align-items:center;gap:8px;
}
.card-label::before{content:'';display:block;width:16px;height:2px;background:var(--c);border-radius:2px}

/* Stat */
.stat-num{font-size:3.5rem;font-weight:800;line-height:1;
  background:linear-gradient(135deg,var(--c),var(--c2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.stat-sub{font-size:.8rem;color:var(--muted);margin-top:6px}

/* Progress bar */
.pbar-bg{background:rgba(255,255,255,.05);border-radius:99px;height:6px;margin-top:20px;overflow:hidden}
.pbar{height:100%;border-radius:99px;background:linear-gradient(90deg,var(--c),var(--c2));transition:width .8s ease}

/* Pre / code */
pre{
  background:rgba(0,0,0,.5);border:1px solid var(--border);
  border-radius:10px;padding:14px;font-size:.75rem;
  color:rgba(255,255,255,.5);overflow:auto;max-height:180px;
  font-family:'Cascadia Code','Fira Code',monospace;line-height:1.6;
}

/* Steps */
.steps{list-style:none}
.steps li{
  padding:9px 0;border-bottom:1px solid rgba(255,255,255,.04);
  font-size:.85rem;color:rgba(255,255,255,.75);
  display:flex;gap:10px;align-items:flex-start;
}
.steps li::before{content:'→';color:var(--c);flex-shrink:0;margin-top:1px}
.steps li:last-child{border-bottom:none}

/* Buttons */
.btn{
  display:inline-flex;align-items:center;gap:8px;
  padding:11px 22px;border-radius:10px;border:none;
  font-size:.875rem;font-weight:600;cursor:pointer;
  transition:all .2s;letter-spacing:-.01em;
}
.btn:disabled{opacity:.4;cursor:not-allowed;transform:none!important;box-shadow:none!important}
.btn-push{
  background:linear-gradient(135deg,var(--c) 0%,var(--c2) 100%);
  color:#fff;box-shadow:0 0 28px rgba(0,212,255,.25);
}
.btn-push:hover:not(:disabled){box-shadow:0 0 40px rgba(0,212,255,.45);transform:translateY(-2px)}
.btn-scan{
  background:rgba(255,170,0,.12);color:var(--yellow);
  border:1px solid rgba(255,170,0,.25);
}
.btn-scan:hover{background:rgba(255,170,0,.2)}
.btn-save{
  background:rgba(0,255,136,.1);color:var(--c3);
  border:1px solid rgba(0,255,136,.2);
}
.btn-save:hover{background:rgba(0,255,136,.18)}
.btn-note{
  background:var(--bg2);color:var(--txt);
  border:1px solid var(--border2);
}
.btn-note:hover{background:rgba(255,255,255,.1)}
.btn-refresh{
  background:transparent;color:var(--muted);
  border:1px solid var(--border);font-size:.8rem;padding:8px 14px;
}
.btn-refresh:hover{color:var(--txt);border-color:var(--border2)}
.actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:4px}

/* Security panel */
.sec-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
.sec-badge{
  display:inline-flex;align-items:center;gap:6px;
  padding:4px 12px;border-radius:99px;font-size:.75rem;font-weight:700;
}
.badge-ok{background:rgba(0,255,136,.12);color:var(--c3);border:1px solid rgba(0,255,136,.2)}
.badge-warn{background:rgba(255,51,85,.12);color:var(--red);border:1px solid rgba(255,51,85,.2)}
.badge-idle{background:rgba(255,255,255,.06);color:var(--muted);border:1px solid var(--border)}
.sec-issue{
  background:rgba(255,51,85,.06);border:1px solid rgba(255,51,85,.15);
  border-radius:10px;padding:12px 16px;margin-bottom:8px;font-size:.8rem;
}
.sec-issue .issue-type{color:var(--red);font-weight:700;margin-bottom:4px}
.sec-issue .issue-file{color:var(--muted)}
.sec-issue .issue-preview{
  font-family:'Cascadia Code','Fira Code',monospace;
  color:rgba(255,255,255,.4);font-size:.72rem;margin-top:4px;
}
.sec-ok{
  display:flex;align-items:center;gap:10px;
  color:var(--c3);font-size:.875rem;padding:12px 0;
}
.sec-info{font-size:.75rem;color:var(--muted);margin-top:10px}

/* Textarea / input */
textarea,input[type=text]{
  width:100%;background:rgba(0,0,0,.4);
  border:1px solid var(--border);border-radius:10px;
  color:var(--txt);padding:12px 16px;font-size:.875rem;
  transition:border-color .2s;font-family:inherit;
}
textarea{resize:vertical;min-height:90px}
textarea:focus,input[type=text]:focus{outline:none;border-color:rgba(0,212,255,.4)}
.field-label{font-size:.75rem;color:var(--muted);margin-bottom:8px;font-weight:600;letter-spacing:.04em;text-transform:uppercase}

/* Toast */
#toast{
  position:fixed;bottom:28px;right:28px;
  padding:14px 22px;border-radius:12px;font-size:.875rem;font-weight:600;
  display:none;z-index:999;
  box-shadow:0 8px 32px rgba(0,0,0,.5);
  animation:slideIn .25s ease;
  max-width:360px;
}
@keyframes slideIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.toast-ok{background:linear-gradient(135deg,rgba(0,255,136,.15),rgba(0,212,255,.1));
  border:1px solid rgba(0,255,136,.3);color:var(--c3)}
.toast-err{background:rgba(255,51,85,.12);border:1px solid rgba(255,51,85,.3);color:var(--red)}

/* Spinner */
.spin{display:inline-block;width:14px;height:14px;border:2px solid rgba(255,255,255,.2);
  border-top-color:var(--c);border-radius:50%;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

/* Divider */
.section-title{
  font-size:.7rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  color:var(--muted);margin:28px 0 14px;
  display:flex;align-items:center;gap:12px;
}
.section-title::after{content:'';flex:1;height:1px;background:var(--border)}

/* Pulse dot */
.pulse{width:8px;height:8px;border-radius:50%;background:var(--c3);
  box-shadow:0 0 0 0 rgba(0,255,136,.4);animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(0,255,136,.4)}
  70%{box-shadow:0 0 0 8px transparent}100%{box-shadow:0 0 0 0 transparent}}
</style>
</head>
<body>

<header>
  <div class="logo">
    <div class="logo-icon">🤖</div>
    <div>
      <h1>AI-EDU-<span>CZ</span></h1>
      <p>Mission Control Dashboard</p>
    </div>
  </div>
  <div id="clock"><span id="date-str"></span><b id="time-str"></b></div>
</header>

<div class="wrap">

  <!-- Row 1: Stats -->
  <div class="grid grid-3">
    <div class="card">
      <div class="card-label">Obsah</div>
      <div class="stat-num" id="stat-done">—</div>
      <div class="stat-sub" id="stat-sub">z — lekcí dokončeno</div>
      <div class="pbar-bg"><div class="pbar" id="pbar" style="width:0%"></div></div>
    </div>
    <div class="card">
      <div class="card-label">Git stav</div>
      <pre id="git-status" style="max-height:120px">Načítám…</pre>
    </div>
    <div class="card">
      <div class="card-label">Příští kroky</div>
      <ul class="steps" id="next-steps"><li>Načítám…</li></ul>
    </div>
  </div>

  <!-- Section: Actions -->
  <div class="section-title">⚡ Akce</div>

  <!-- Security + Push card -->
  <div class="card" style="margin-bottom:18px">
    <div class="sec-header">
      <div class="card-label" style="margin-bottom:0">Security audit &amp; GitHub Push</div>
      <span class="sec-badge badge-idle" id="sec-badge">Nespuštěno</span>
    </div>

    <div id="sec-results" style="margin-bottom:16px;display:none"></div>

    <div class="actions">
      <button class="btn btn-scan" id="btn-scan" onclick="runScan()">🔍 Spustit Security Audit</button>
      <button class="btn btn-push" id="btn-push" onclick="pushGithub()" disabled>⬆ Push na GitHub</button>
      <button class="btn btn-refresh" onclick="refreshStatus()">↻ Obnovit</button>
    </div>
    <div class="sec-info" id="sec-info">Před každým pushem proběhne automaticky security scan.</div>
  </div>

  <!-- Save session + note -->
  <div class="grid grid-2">
    <div class="card">
      <div class="card-label">Uložit Session</div>
      <p style="font-size:.85rem;color:var(--muted);margin-bottom:16px">Aktualizuje SESSION.md s dnešním datem a commitne stav projektu.</p>
      <button class="btn btn-save" onclick="saveSession()">💾 Uložit Session</button>
    </div>
    <div class="card">
      <div class="card-label">Přidat poznámku</div>
      <textarea id="note-text" placeholder="Co bylo uděláno… co řeším… příští kroky…"></textarea>
      <button class="btn btn-note" onclick="addNote()" style="margin-top:10px">📌 Přidat do SESSION.md</button>
    </div>
  </div>

  <!-- Commits -->
  <div class="section-title">🕐 Historie commitů</div>
  <div class="card">
    <pre id="commits" style="max-height:220px">Načítám…</pre>
  </div>

</div><!-- /wrap -->

<div id="toast"></div>

<script>
// ── Clock ──
function tick(){
  const n=new Date();
  document.getElementById('date-str').textContent=
    n.toLocaleDateString('cs-CZ',{weekday:'long',day:'numeric',month:'long',year:'numeric'});
  document.getElementById('time-str').textContent=n.toLocaleTimeString('cs-CZ');
}
setInterval(tick,1000);tick();

// ── Toast ──
function toast(msg,ok=true){
  const el=document.getElementById('toast');
  el.textContent=msg;el.className=ok?'toast-ok':'toast-err';
  el.style.display='block';
  clearTimeout(el._t);el._t=setTimeout(()=>el.style.display='none',4500);
}

// ── API ──
async function api(path,data={}){
  const r=await fetch(path,{method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify(data)});
  return r.json();
}

// ── Status refresh ──
async function refreshStatus(){
  const d=await api('/api/status');
  const pct=d.total?Math.round(d.done/d.total*100):0;
  document.getElementById('stat-done').textContent=d.done;
  document.getElementById('stat-sub').textContent=`z ${d.total} lekcí dokončeno`;
  document.getElementById('pbar').style.width=pct+'%';
  document.getElementById('git-status').textContent=d.git_status;
  document.getElementById('commits').textContent=d.last_commits;
  const ul=document.getElementById('next-steps');
  ul.innerHTML=d.next_steps.length
    ? d.next_steps.map(s=>`<li>${s}</li>`).join('')
    : '<li>Viz SESSION.md</li>';
}

// ── Security scan ──
let scanPassed=false;
async function runScan(){
  const btn=document.getElementById('btn-scan');
  const badge=document.getElementById('sec-badge');
  const info=document.getElementById('sec-info');
  const results=document.getElementById('sec-results');
  const pushBtn=document.getElementById('btn-push');

  btn.innerHTML='<span class="spin"></span> Skenuji…';
  btn.disabled=true;
  badge.className='sec-badge badge-idle';badge.textContent='Skenuju…';
  results.style.display='none';scanPassed=false;pushBtn.disabled=true;

  const d=await api('/api/security-scan');

  btn.innerHTML='🔍 Spustit Security Audit';btn.disabled=false;
  results.style.display='block';

  if(d.ok){
    badge.className='sec-badge badge-ok';badge.textContent='✓ Čisto';
    results.innerHTML=`<div class="sec-ok"><span style="font-size:1.4rem">✅</span>
      Sken dokončen — žádné tajné klíče ani citlivá data nenalezena.</div>`;
    info.textContent=`Prohledáno ${d.files_scanned} souborů. Push je povolen.`;
    scanPassed=true;pushBtn.disabled=false;
  } else {
    badge.className='sec-badge badge-warn';badge.textContent=`⚠ ${d.issues.length} problémů`;
    results.innerHTML=d.issues.map(i=>`
      <div class="sec-issue">
        <div class="issue-type">⚠ ${i.type}</div>
        <div class="issue-file">${i.file}${i.line?` · řádek ${i.line}`:''}</div>
        ${i.preview?`<div class="issue-preview">${i.preview}</div>`:''}
      </div>`).join('');
    info.textContent='Push zablokován. Odstraň problémy a spusť sken znovu.';
    toast(`Security: ${d.issues.length} problémů nalezeno — oprav je!`,false);
  }
}

// ── Push ──
async function pushGithub(){
  if(!scanPassed){toast('Nejdříve spusť security scan!',false);return;}
  const btn=document.getElementById('btn-push');
  btn.innerHTML='<span class="spin"></span> Pushuji…';btn.disabled=true;

  const d=await api('/api/push');
  btn.innerHTML='⬆ Push na GitHub';
  if(d.ok){
    scanPassed=false;btn.disabled=true;
    toast(d.message);refreshStatus();
    document.getElementById('sec-badge').className='sec-badge badge-idle';
    document.getElementById('sec-badge').textContent='Nespuštěno';
    document.getElementById('sec-results').style.display='none';
    document.getElementById('sec-info').textContent='Před každým pushem proběhne automaticky security scan.';
  } else {
    btn.disabled=false;toast(d.message,false);
  }
}

// ── Save session ──
async function saveSession(){
  const d=await api('/api/save-session');
  toast(d.message,d.ok);if(d.ok)refreshStatus();
}

// ── Add note ──
async function addNote(){
  const note=document.getElementById('note-text').value.trim();
  if(!note){toast('Napiš poznámku nejdřív.',false);return;}
  const d=await api('/api/add-note',{note});
  toast(d.message,d.ok);if(d.ok)document.getElementById('note-text').value='';
}

refreshStatus();
</script>
</body>
</html>"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def read_file(name):
    try:
        return (PROJECT_ROOT / name).read_text(encoding='utf-8')
    except Exception:
        return ''


def get_progress():
    text = read_file('PROGRESS.md')
    done = text.count('✅')
    total = done + text.count('⏳')
    return done, total or 35


def get_next_steps():
    text = read_file('SESSION.md')
    steps, on = [], False
    for line in text.splitlines():
        if 'Příští kroky' in line:
            on = True; continue
        if on:
            if line.startswith('##'): break
            if re.match(r'^\d+\.', line.strip()):
                steps.append(line.strip())
    return steps[:5]


def save_session_note(note):
    path = PROJECT_ROOT / 'SESSION.md'
    try:
        content = path.read_text(encoding='utf-8')
        today = datetime.date.today().isoformat()
        content = re.sub(r'\*\*Datum:\*\*.*', f'**Datum:** {today}', content)
        marker = '## Co bylo uděláno v tomto sessionu'
        block = f'\n### Poznámka {today}\n{note}\n'
        content = content.replace(marker, marker + block, 1)
        path.write_text(content, encoding='utf-8')
        return True, 'SESSION.md aktualizován'
    except Exception as e:
        return False, str(e)


# ── HTTP Handler ───────────────────────────────────────────────────────────────

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            body = HTML.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length) or b'{}')

        if self.path == '/api/status':
            done, total = get_progress()
            gs, _, _ = run_git(['status', '--short'])
            lc, _, _ = run_git(['log', '--oneline', '-7'])
            self._json({
                'done': done, 'total': total,
                'git_status': gs or '— vše commitnuto',
                'last_commits': lc or '(žádné commity)',
                'next_steps': get_next_steps(),
            })

        elif self.path == '/api/security-scan':
            self._json(scan_security())

        elif self.path == '/api/push':
            ok, msg, scan = do_push_github()
            self._json({'ok': ok, 'message': msg, 'scan': scan})

        elif self.path == '/api/save-session':
            note = f'Session uložen automaticky {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}'
            ok, msg = save_session_note(note)
            self._json({'ok': ok, 'message': msg})

        elif self.path == '/api/add-note':
            ok, msg = save_session_note(body.get('note', ''))
            self._json({'ok': ok, 'message': msg})

        else:
            self._json({'error': 'not found'}, 404)


if __name__ == '__main__':
    os.chdir(PROJECT_ROOT)
    srv = http.server.HTTPServer(('localhost', PORT), Handler)
    print(f'\n  🤖 AI-EDU-CZ Mission Control')
    print(f'  ──────────────────────────────')
    print(f'  http://localhost:{PORT}')
    print(f'  Ctrl+C pro zastavení\n')
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\n  Dashboard zastaven.')
