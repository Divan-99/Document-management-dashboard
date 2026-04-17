/**
 * dashboard.js — Iscar Process Dashboard
 */

let _config = {};
let _pollTimer = null;
let _logPollTimer = null;
let _currentLogProcess = null;

// ── Init ──────────────────────────────────────────────────────────────────────

function initDashboard(config) {
  _config = config;
  fetchAllStatuses();
  _pollTimer = setInterval(fetchAllStatuses, config.pollInterval);
}

// ── Status polling ────────────────────────────────────────────────────────────

async function fetchAllStatuses() {
  try {
    const res = await fetch(_config.statusAllUrl);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    let running = 0, stopped = 0;
    for (const [id, info] of Object.entries(data)) {
      applyStatus(id, info);
      if (info.status === 'running') running++; else stopped++;
    }

    // Update stat pills
    const el_r = document.getElementById('count-running');
    const el_s = document.getElementById('count-stopped');
    if (el_r) el_r.textContent = running;
    if (el_s) el_s.textContent = stopped;

    const el = document.getElementById('last-updated');
    if (el) el.textContent = 'Last updated ' + new Date().toLocaleTimeString();

  } catch (err) {
    console.warn('Status poll failed:', err);
  }
}

function refreshAll() {
  fetchAllStatuses();
  showToast('Refreshed', 'info', 1500);
}

function applyStatus(id, info) {
  const badge      = document.getElementById(`badge-${id}`);
  const pidEl      = document.getElementById(`pid-${id}`);
  const uptimeEl   = document.getElementById(`uptime-${id}`);
  const card       = document.getElementById(`card-${id}`);
  const btnStart   = document.getElementById(`btn-start-${id}`);
  const btnStop    = document.getElementById(`btn-stop-${id}`);
  const btnRestart = document.getElementById(`btn-restart-${id}`);
  const openLink   = document.getElementById(`open-${id}`);

  if (!badge) return;
  const running = info.status === 'running';

  badge.className = `status-badge status-${running ? 'running' : 'stopped'}`;
  badge.innerHTML = `<span class="badge-dot"></span><span class="badge-text">${running ? 'Running' : 'Stopped'}</span>`;

  if (card) card.classList.toggle('is-running', running);
  if (pidEl)    pidEl.textContent    = running && info.pid ? `PID ${info.pid}` : '';
  if (uptimeEl) uptimeEl.textContent = running && info.started_at ? `Started ${info.started_at}` : '';
  if (openLink) openLink.style.display = running ? 'inline' : 'none';

  if (btnStart)   btnStart.disabled   = running;
  if (btnStop)    btnStop.disabled    = !running;
  if (btnRestart) btnRestart.disabled = !running;
}

// ── Process control ───────────────────────────────────────────────────────────

async function controlProcess(id, action) {
  setCardBusy(id, true, action);

  const urlTemplate = action === 'start'   ? _config.startUrl
                    : action === 'stop'    ? _config.stopUrl
                    :                        _config.restartUrl;

  const url = urlTemplate.replace('PROCESS_ID', id);

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': _config.csrfToken },
    });
    const data = await res.json();

    if (data.ok) {
      const label = action.charAt(0).toUpperCase() + action.slice(1);
      showToast(`${label}ed successfully`, 'success');
      if (data.warning) showToast(data.warning, 'warning');
    } else {
      showToast(data.error || 'Action failed', 'error');
    }
  } catch (err) {
    showToast(`Request failed: ${err.message}`, 'error');
  }

  setTimeout(fetchAllStatuses, 700);
  setCardBusy(id, false, null);
}

// ── Start All / Stop All ──────────────────────────────────────────────────────

async function controlAll(action) {
  const ids = _config.processIds;
  const label = action === 'start' ? 'Starting' : 'Stopping';

  showToast(`${label} all processes…`, 'info', 2000);

  // Disable both buttons during operation
  const btnStart = document.querySelector('.btn-start-all');
  const btnStop  = document.querySelector('.btn-stop-all');
  if (btnStart) btnStart.disabled = true;
  if (btnStop)  btnStop.disabled  = true;

  // Fire all requests in parallel
  const urlTemplate = action === 'start' ? _config.startUrl : _config.stopUrl;
  const requests = ids.map(id => {
    const url = urlTemplate.replace('PROCESS_ID', id);
    return fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': _config.csrfToken },
    }).then(r => r.json()).catch(() => ({ ok: false }));
  });

  const results = await Promise.all(requests);
  const failed  = results.filter(r => !r.ok).length;

  if (failed === 0) {
    showToast(`All processes ${action === 'start' ? 'started' : 'stopped'} successfully`, 'success');
  } else {
    showToast(`${failed} process(es) failed — check logs`, 'warning');
  }

  // Re-enable buttons and refresh
  if (btnStart) btnStart.disabled = false;
  if (btnStop)  btnStop.disabled  = false;
  setTimeout(fetchAllStatuses, 800);
}


function setCardBusy(id, busy, action) {
  const badge      = document.getElementById(`badge-${id}`);
  const btnStart   = document.getElementById(`btn-start-${id}`);
  const btnStop    = document.getElementById(`btn-stop-${id}`);
  const btnRestart = document.getElementById(`btn-restart-${id}`);

  if (busy) {
    if (badge) {
      badge.className = 'status-badge status-checking';
      const label = action === 'start' ? 'Starting…' : action === 'stop' ? 'Stopping…' : 'Restarting…';
      badge.innerHTML = `<span class="badge-dot"></span><span class="badge-text">${label}</span>`;
    }
    if (btnStart)   btnStart.disabled   = true;
    if (btnStop)    btnStop.disabled    = true;
    if (btnRestart) btnRestart.disabled = true;
  }
}

// ── Log drawer ────────────────────────────────────────────────────────────────

function openLogs(processId, label) {
  _currentLogProcess = processId;
  const drawer = document.getElementById('log-drawer');
  const title  = document.getElementById('log-drawer-title');
  if (title) title.textContent = `Output Log — ${label}`;
  drawer.classList.add('open');
  fetchLogs();
  clearInterval(_logPollTimer);
  _logPollTimer = setInterval(fetchLogs, 2000);
}

function closeLogDrawer() {
  document.getElementById('log-drawer').classList.remove('open');
  clearInterval(_logPollTimer);
  _currentLogProcess = null;
}

function clearLogView() {
  const body = document.getElementById('log-body');
  if (body) body.innerHTML = '';
}

async function fetchLogs() {
  if (!_currentLogProcess) return;
  const url = _config.logsUrl.replace('PROCESS_ID', _currentLogProcess) + '?n=150';
  try {
    const res  = await fetch(url);
    const data = await res.json();
    renderLogs(data.logs || []);
  } catch (err) {
    console.warn('Log fetch failed:', err);
  }
}

function renderLogs(lines) {
  const body = document.getElementById('log-body');
  if (!body) return;

  if (lines.length === 0) {
    body.innerHTML = `<div class="log-empty">No output yet — start the process to see logs here.</div>`;
    return;
  }

  const atBottom = body.scrollHeight - body.clientHeight <= body.scrollTop + 32;

  body.innerHTML = lines.map(({ ts, line }) =>
    `<div class="log-line">
      <span class="log-ts">${escapeHtml(ts)}</span>
      <span class="log-text">${escapeHtml(line)}</span>
    </div>`
  ).join('');

  if (atBottom) body.scrollTop = body.scrollHeight;
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
