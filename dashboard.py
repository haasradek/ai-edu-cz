#!/usr/bin/env python3
"""
AI-EDU-CZ Dashboard
Spusti: python dashboard.py
Pak otevri: http://localhost:8765
"""

import http.server
import json
import os
import subprocess
import datetime
import re
from urllib.parse import urlparse, parse_qs

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8765


def run_git(args):
    result = subprocess.run(
        ["git"] + args,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def read_file(path):
    try:
        with open(os.path.join(PROJECT_ROOT, path), encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def get_progress_stats():
    content = read_file("PROGRESS.md")
    done = content.count("✅")
    todo = content.count("⏳")
    total = done + todo
    return done, total


def get_next_steps():
    content = read_file("SESSION.md")
    steps = []
    in_section = False
    for line in content.splitlines():
        if "Příští kroky" in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("##"):
                break
            if line.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
                steps.append(line.strip())
    return steps[:5]


def get_git_status():
    stdout, _, _ = run_git(["status", "--short"])
    return stdout


def get_last_commits():
    stdout, _, _ = run_git(["log", "--oneline", "-5"])
    return stdout


def do_push_github(commit_msg=None):
    if not commit_msg:
        commit_msg = f"Session update {datetime.date.today()}"

    run_git(["add", "-A"])
    out, err, code = run_git(["commit", "-m", commit_msg])
    if code != 0 and "nothing to commit" not in err and "nothing to commit" not in out:
        return False, f"Commit selhal: {err or out}"

    out, err, code = run_git(["push"])
    if code != 0:
        return False, f"Push selhal: {err}"
    return True, "Push na GitHub probehl uspesne!"


def save_session_note(note):
    session_path = os.path.join(PROJECT_ROOT, "SESSION.md")
    with open(session_path, encoding="utf-8") as f:
        content = f.read()

    today = datetime.date.today().isoformat()
    update_line = f"**Datum:** {today}"
    content = re.sub(r"\*\*Datum:\*\*.*", update_line, content)

    note_block = f"\n### Poznámka přidána {today}\n{note}\n"
    marker = "## Co bylo uděláno v tomto sessionu"
    content = content.replace(marker, marker + note_block, 1)

    with open(session_path, "w", encoding="utf-8") as f:
        f.write(content)
    return True, "SESSION.md aktualizovan"


HTML = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI-EDU-CZ Dashboard</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; }
  header { background: linear-gradient(135deg, #1e3a5f, #0f172a); padding: 24px 32px; border-bottom: 1px solid #1e293b; }
  header h1 { font-size: 1.8rem; color: #38bdf8; font-weight: 700; }
  header p { color: #94a3b8; font-size: 0.9rem; margin-top: 4px; }
  .container { max-width: 1100px; margin: 0 auto; padding: 32px 24px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 28px; }
  .card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; }
  .card h2 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; margin-bottom: 16px; }
  .stat-big { font-size: 3rem; font-weight: 800; color: #38bdf8; line-height: 1; }
  .stat-label { color: #94a3b8; font-size: 0.85rem; margin-top: 6px; }
  .progress-bar-bg { background: #0f172a; border-radius: 8px; height: 12px; margin-top: 16px; overflow: hidden; }
  .progress-bar { background: linear-gradient(90deg, #0ea5e9, #38bdf8); height: 100%; border-radius: 8px; transition: width 0.6s ease; }
  .btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; border: none; transition: all 0.2s; }
  .btn-primary { background: #0ea5e9; color: white; }
  .btn-primary:hover { background: #38bdf8; transform: translateY(-1px); }
  .btn-success { background: #10b981; color: white; }
  .btn-success:hover { background: #34d399; transform: translateY(-1px); }
  .btn-warning { background: #f59e0b; color: #0f172a; }
  .btn-warning:hover { background: #fbbf24; transform: translateY(-1px); }
  .btn-danger { background: #ef4444; color: white; }
  .btn-danger:hover { background: #f87171; }
  .actions { display: flex; flex-wrap: wrap; gap: 12px; }
  pre { background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 16px; font-size: 0.8rem; color: #94a3b8; overflow-x: auto; white-space: pre-wrap; max-height: 200px; overflow-y: auto; }
  ul.steps { list-style: none; padding: 0; }
  ul.steps li { padding: 8px 0; border-bottom: 1px solid #0f172a; color: #cbd5e1; font-size: 0.9rem; }
  ul.steps li:before { content: "→ "; color: #38bdf8; }
  .toast { position: fixed; bottom: 24px; right: 24px; background: #10b981; color: white; padding: 14px 24px; border-radius: 10px; font-weight: 600; display: none; z-index: 100; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
  .toast.error { background: #ef4444; }
  textarea { width: 100%; background: #0f172a; border: 1px solid #334155; border-radius: 8px; color: #e2e8f0; padding: 12px; font-size: 0.9rem; resize: vertical; margin-bottom: 12px; }
  input[type=text] { width: 100%; background: #0f172a; border: 1px solid #334155; border-radius: 8px; color: #e2e8f0; padding: 10px 14px; font-size: 0.9rem; margin-bottom: 12px; }
  .badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; background: #0ea5e9; color: white; margin-left: 8px; }
</style>
</head>
<body>
<header>
  <h1>🤖 AI-EDU-CZ Dashboard</h1>
  <p id="datetime"></p>
</header>
<div class="container">

  <div class="grid">
    <!-- Progress -->
    <div class="card">
      <h2>📚 Obsah projektu</h2>
      <div class="stat-big" id="done-count">—</div>
      <div class="stat-label">lekcí dokončeno</div>
      <div class="progress-bar-bg">
        <div class="progress-bar" id="progress-bar" style="width:0%"></div>
      </div>
      <div class="stat-label" id="progress-label" style="margin-top:8px">Načítám...</div>
    </div>

    <!-- Git status -->
    <div class="card">
      <h2>🔀 Git Status</h2>
      <pre id="git-status">Načítám...</pre>
    </div>

    <!-- Příští kroky -->
    <div class="card">
      <h2>📋 Příští kroky</h2>
      <ul class="steps" id="next-steps"><li>Načítám...</li></ul>
    </div>
  </div>

  <!-- Akce -->
  <div class="card" style="margin-bottom:20px">
    <h2>⚡ Akce</h2>
    <div style="margin-bottom:16px">
      <label style="color:#94a3b8; font-size:0.85rem;">Commit zpráva (volitelné):</label>
      <input type="text" id="commit-msg" placeholder="Session update — co bylo uděláno..." />
    </div>
    <div class="actions">
      <button class="btn btn-success" onclick="pushGithub()">⬆️ Push na GitHub</button>
      <button class="btn btn-primary" onclick="saveSession()">💾 Uložit Session</button>
      <button class="btn btn-warning" onclick="refreshStatus()">🔄 Obnovit stav</button>
    </div>
  </div>

  <!-- Poznámka pro session -->
  <div class="card" style="margin-bottom:20px">
    <h2>📝 Přidat poznámku do SESSION.md</h2>
    <textarea id="session-note" rows="4" placeholder="Co bylo uděláno... co řeším... příští kroky..."></textarea>
    <button class="btn btn-primary" onclick="addNote()">📌 Uložit poznámku</button>
  </div>

  <!-- Poslední commity -->
  <div class="card">
    <h2>🕐 Poslední commity</h2>
    <pre id="last-commits">Načítám...</pre>
  </div>

</div>

<div class="toast" id="toast"></div>

<script>
function showToast(msg, error=false) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast' + (error ? ' error' : '');
  t.style.display = 'block';
  setTimeout(() => t.style.display='none', 4000);
}

async function api(endpoint, data={}) {
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
  return res.json();
}

async function refreshStatus() {
  const data = await api('/api/status');
  document.getElementById('done-count').textContent = data.done;
  document.getElementById('progress-bar').style.width = (data.done / data.total * 100) + '%';
  document.getElementById('progress-label').textContent = `${data.done} z ${data.total} lekcí (${Math.round(data.done/data.total*100)}%)`;
  document.getElementById('git-status').textContent = data.git_status || '✅ Vše commitnuto';
  document.getElementById('last-commits').textContent = data.last_commits || 'Žádné commity';
  const ul = document.getElementById('next-steps');
  ul.innerHTML = data.next_steps.map(s => `<li>${s}</li>`).join('') || '<li>Viz SESSION.md</li>';
}

async function pushGithub() {
  const msg = document.getElementById('commit-msg').value || '';
  showToast('Probíhá push na GitHub...');
  const data = await api('/api/push', {commit_msg: msg});
  showToast(data.message, !data.ok);
  refreshStatus();
}

async function saveSession() {
  showToast('Ukládám session stav...');
  const data = await api('/api/save-session');
  showToast(data.message, !data.ok);
}

async function addNote() {
  const note = document.getElementById('session-note').value.trim();
  if (!note) { showToast('Napiš poznámku nejdřív.', true); return; }
  const data = await api('/api/add-note', {note});
  showToast(data.message, !data.ok);
  if (data.ok) document.getElementById('session-note').value = '';
}

// Datetime
function updateTime() {
  const now = new Date();
  document.getElementById('datetime').textContent =
    now.toLocaleDateString('cs-CZ', {weekday:'long', year:'numeric', month:'long', day:'numeric'}) +
    ' — ' + now.toLocaleTimeString('cs-CZ');
}
setInterval(updateTime, 1000);
updateTime();

refreshStatus();
</script>
</body>
</html>"""


class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass  # Tiché logy

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            body = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")

        if self.path == "/api/status":
            done, total = get_progress_stats()
            git_stat = get_git_status()
            commits = get_last_commits()
            steps = get_next_steps()
            self.send_json({
                "done": done,
                "total": total,
                "git_status": git_stat,
                "last_commits": commits,
                "next_steps": steps,
            })

        elif self.path == "/api/push":
            msg = body.get("commit_msg") or f"Session update {datetime.date.today()}"
            ok, message = do_push_github(msg)
            self.send_json({"ok": ok, "message": message})

        elif self.path == "/api/save-session":
            ok, message = save_session_note(
                f"Session ulozen automaticky {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            self.send_json({"ok": ok, "message": message})

        elif self.path == "/api/add-note":
            note = body.get("note", "")
            ok, message = save_session_note(note)
            self.send_json({"ok": ok, "message": message})

        else:
            self.send_json({"error": "Not found"}, 404)


if __name__ == "__main__":
    os.chdir(PROJECT_ROOT)
    server = http.server.HTTPServer(("localhost", PORT), Handler)
    print(f"✅ AI-EDU-CZ Dashboard bezi na http://localhost:{PORT}")
    print("   Stiskni Ctrl+C pro zastaveni.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard zastaven.")
