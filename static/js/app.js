/**
 * Prompteering MVP — Frontend Logic
 * Calls backend APIs for real NLP analysis, caches token data for instant model switching.
 */

// ── STATE ────────────────────────────────────────────────────────
let tokenData = null;  // cached from /api/tokens (all models in one call)
let currentModel = 'gpt-4o';

// ── SVG ICONS ────────────────────────────────────────────────────
const ICONS = {
    'list-ordered': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>`,
    'code': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>`,
    'pen': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>`,
    'info': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
    'list': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>`,
    'chart': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>`,
    'help': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
};

const ARROW_SVG = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`;

// ── WEIGHT COLORS ────────────────────────────────────────────────
function weightColor(s) {
    if (s < 0.18) return { bg: 'rgba(55,55,70,0.35)', border: 'rgba(55,55,70,0.4)', txt: '#55556a' };
    if (s < 0.45) return { bg: 'rgba(79,195,247,0.1)', border: 'rgba(79,195,247,0.28)', txt: '#7dd3fc' };
    if (s < 0.72) return { bg: 'rgba(255,140,66,0.14)', border: 'rgba(255,140,66,0.35)', txt: '#fbbf24' };
    return { bg: 'rgba(200,241,53,0.14)', border: 'rgba(200,241,53,0.4)', txt: '#c8f135' };
}

// ── API HELPER ───────────────────────────────────────────────────
async function postAPI(endpoint, prompt) {
    const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
    });
    if (!res.ok) throw new Error(`${endpoint} returned ${res.status}`);
    return res.json();
}

// ── MAIN ANALYSIS ────────────────────────────────────────────────
async function analyzePrompt() {
    const text = document.getElementById('promptInput').value.trim();
    if (!text) return;

    const btn = document.querySelector('.run-btn');
    btn.classList.add('loading');

    try {
        // Fire all 4 endpoints in parallel
        const [weights, tokens, intent, flow] = await Promise.all([
            postAPI('/api/weights', text),
            postAPI('/api/tokens', text),
            postAPI('/api/intent', text),
            postAPI('/api/flowchart', text),
        ]);

        // Cache token data for model switching
        tokenData = tokens;

        // Render all panels
        renderWeightMap(weights.words);
        renderTokenStats(currentModel);
        renderIntents(intent.intents);
        renderFlowchart(flow.nodes);

        // Show results
        document.getElementById('emptyState').style.display = 'none';
        document.getElementById('results').style.display = 'flex';

    } catch (err) {
        console.error('Analysis failed:', err);
        alert('Analysis failed — is the server running?');
    } finally {
        btn.classList.remove('loading');
    }
}

// ── RENDER: WEIGHT MAP ───────────────────────────────────────────
function renderWeightMap(words) {
    const container = document.getElementById('wordWeights');
    container.innerHTML = '';

    words.forEach(({ word, score }) => {
        const col = weightColor(score);
        const el = document.createElement('span');
        el.className = 'token';
        el.style.cssText = `background:${col.bg};border-color:${col.border};color:${col.txt};`;
        el.innerHTML = `${escapeHtml(word)}<span class="token-tip">weight: ${score.toFixed(2)}</span>`;
        container.appendChild(el);
    });
}

// ── RENDER: TOKEN STATS ──────────────────────────────────────────
function renderTokenStats(modelId) {
    if (!tokenData || !tokenData[modelId]) return;

    const d = tokenData[modelId];
    document.getElementById('tokenStats').innerHTML = `
    <div class="stat">
      <div class="stat-lbl">Prompt Tokens</div>
      <div class="stat-val c-green">${d.promptTokens.toLocaleString()}</div>
      <div class="stat-sub">${d.wordCount} words · ${d.charCount} chars</div>
    </div>
    <div class="stat">
      <div class="stat-lbl">Est. Output Tokens</div>
      <div class="stat-val c-orange">${d.outputMin.toLocaleString()}–${d.outputMax.toLocaleString()}</div>
      <div class="stat-sub">midpoint ~${d.outputMid.toLocaleString()}</div>
    </div>
    <div class="stat">
      <div class="stat-lbl">Max Context Total</div>
      <div class="stat-val c-blue">${d.total.toLocaleString()}</div>
      <div class="stat-sub">of ${formatWindow(d.contextWindow)} limit</div>
    </div>
    <div class="stat">
      <div class="stat-lbl">Est. API Cost</div>
      <div class="stat-val c-red">$${d.cost < 0.001 ? d.cost.toFixed(5) : d.cost.toFixed(4)}</div>
      <div class="stat-sub">${d.label} pricing</div>
    </div>
  `;

    // Context window bar
    const pct = Math.min(98, (d.total / d.contextWindow) * 100);
    document.getElementById('costLabel').textContent = `${pct.toFixed(1)}%  ·  $${d.cost.toFixed(5)}`;
    setTimeout(() => {
        document.getElementById('costFill').style.width = pct + '%';
    }, 60);

    // Update panel subtitle
    document.getElementById('tokenPanelSubtitle').textContent = `tiktoken · ${d.label} rates`;

    // Highlight active tab
    document.querySelectorAll('.model-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.model === modelId);
    });
}

// ── RENDER: INTENTS ──────────────────────────────────────────────
function renderIntents(intents) {
    const top = intents[0];
    const icon = ICONS[top.icon] || ICONS['help'];

    document.getElementById('intentPanel').innerHTML = `
    <div class="intent-badge">${icon} ${escapeHtml(top.name)}</div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:var(--text3);letter-spacing:0.08em;margin-bottom:13px;">CONFIDENCE BREAKDOWN</div>
    ${intents.map((it, i) => `
      <div class="conf-row">
        <div class="conf-lbl">${escapeHtml(it.name)}</div>
        <div class="conf-track">
          <div class="conf-bar-fill" data-w="${it.score * 100}" style="background:${i === 0 ? 'var(--accent)' : 'rgba(79,195,247,0.5)'}"></div>
        </div>
        <div class="conf-pct">${Math.round(it.score * 100)}%</div>
      </div>
    `).join('')}
  `;

    // Animate bars
    setTimeout(() => {
        document.querySelectorAll('.conf-bar-fill').forEach(el => {
            el.style.width = el.dataset.w + '%';
        });
    }, 60);
}

// ── RENDER: FLOWCHART ────────────────────────────────────────────
function renderFlowchart(nodes) {
    const row = document.getElementById('flowRow');
    row.innerHTML = nodes.map((n, i) => `
    <div class="fnode fnode-${n.type}">${escapeHtml(n.label)}</div>
    ${i < nodes.length - 1 ? `<div class="farrow">${ARROW_SVG}</div>` : ''}
  `).join('');
}

// ── UTILS ────────────────────────────────────────────────────────
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function formatWindow(n) {
    if (n >= 1_000_000) return (n / 1_000_000) + 'M';
    if (n >= 1_000) return (n / 1_000) + 'k';
    return n.toString();
}

// ── MODEL TAB SWITCHING ──────────────────────────────────────────
function switchModel(modelId) {
    currentModel = modelId;
    renderTokenStats(modelId);
}

// ── INIT ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    // Ctrl+Enter shortcut
    document.getElementById('promptInput').addEventListener('keydown', e => {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) analyzePrompt();
    });

    // Model tab clicks
    document.querySelectorAll('.model-tab').forEach(tab => {
        tab.addEventListener('click', () => switchModel(tab.dataset.model));
    });
});
