// DeepFakeGuard — Dashboard JavaScript

const API = '';

// ── State ──
const state = {
    audio: { file: null, endpoint: '/api/v1/detect/audio' },
    image: { file: null, endpoint: '/api/v1/detect/image' }
};

// ── Drop Zone Setup ──

function setupCard(type) {
    const drop = document.getElementById(`${type}-drop`);
    const input = document.getElementById(`${type}-input`);
    const preview = document.getElementById(`${type}-preview`);
    const filename = document.getElementById(`${type}-filename`);
    const filesize = document.getElementById(`${type}-filesize`);
    const removeBtn = document.getElementById(`${type}-remove`);
    const analyseBtn = document.getElementById(`${type}-analyse`);

    // Click to browse
    drop.addEventListener('click', () => input.click());

    // Drag over
    drop.addEventListener('dragover', (e) => {
        e.preventDefault();
        drop.classList.add('dragover');
    });
    drop.addEventListener('dragleave', () => {
        drop.classList.remove('dragover');
    });

    // Drop
    drop.addEventListener('drop', (e) => {
        e.preventDefault();
        drop.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file) selectFile(type, file);
    });

    // File input change
    input.addEventListener('change', () => {
        const file = input.files[0];
        if (file) selectFile(type, file);
        input.value = '';
    });

    // Remove file
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        clearFile(type);
    });

    // Analyse button
    analyseBtn.addEventListener('click', () => {
        if (state[type].file) {
            analyseFile(type);
        }
    });
}

function selectFile(type, file) {
    state[type].file = file;
    const preview = document.getElementById(`${type}-preview`);
    const filename = document.getElementById(`${type}-filename`);
    const filesize = document.getElementById(`${type}-filesize`);
    const analyseBtn = document.getElementById(`${type}-analyse`);

    filename.textContent = file.name;
    filesize.textContent = formatSize(file.size);
    preview.classList.add('active');
    analyseBtn.disabled = false;
}

function clearFile(type) {
    state[type].file = null;
    const preview = document.getElementById(`${type}-preview`);
    const analyseBtn = document.getElementById(`${type}-analyse`);

    preview.classList.remove('active');
    analyseBtn.disabled = true;
}

function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
}

setupCard('audio');
setupCard('image');

// ── Analyse ──

async function analyseFile(type) {
    const file = state[type].file;
    if (!file) return;

    const loadingOverlay = document.getElementById('loading-overlay');
    const resultEmpty = document.getElementById('result-empty');
    const resultContent = document.getElementById('result-content');

    // Show loading
    loadingOverlay.classList.add('active');
    resultEmpty.style.display = 'none';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch(API + state[type].endpoint, { method: 'POST', body: formData });
        const data = await res.json();

        if (data.error) {
            loadingOverlay.classList.remove('active');
            showResultError(data.error.message || 'Detection failed');
            return;
        }

        // Small delay for UX even if fast
        setTimeout(() => {
            loadingOverlay.classList.remove('active');
            showResult(data);
            clearFile(type);
            loadHistory();
        }, 300);
    } catch (err) {
        loadingOverlay.classList.remove('active');
        showResultError('Upload failed: ' + err.message);
    }
}

// ── Result Display ──

function showResult(data) {
    const resultEmpty = document.getElementById('result-empty');
    const resultContent = document.getElementById('result-content');

    resultEmpty.style.display = 'none';
    resultContent.style.display = 'block';

    const isReal = data.verdict === 'real';
    const verdictClass = isReal ? 'real' : 'fake';
    const confPct = (data.confidence * 100).toFixed(1);
    const emoji = isReal ? '&#9989;' : '&#9888;&#65039;';
    const verdictText = isReal ? 'Authentic' : 'Deepfake Detected';
    const verdictDesc = isReal
        ? 'This media appears to be genuine'
        : 'This media shows signs of AI manipulation';

    const severityMap = {
        low: { cls: 'severity-low', text: 'LOW' },
        medium: { cls: 'severity-medium', text: 'MEDIUM' },
        high: { cls: 'severity-high', text: 'HIGH' },
        critical: { cls: 'severity-critical', text: 'CRITICAL' }
    };
    const sev = severityMap[data.severity] || severityMap.low;

    resultContent.innerHTML = `
        <div class="verdict-block ${verdictClass}">
            <div class="verdict-left">
                <span class="verdict-emoji">${emoji}</span>
                <div class="verdict-info">
                    <span class="verdict-label ${verdictClass}">${verdictText}</span>
                    <span class="verdict-desc">${verdictDesc} &middot; ${data.media_type}</span>
                </div>
            </div>
            <span class="verdict-confidence ${verdictClass}">${confPct}%</span>
        </div>
        <div class="confidence-bar-track">
            <div class="confidence-bar-fill ${verdictClass}" id="conf-bar-fill"></div>
        </div>
        <div class="detail-grid">
            <div class="detail-cell">
                <div class="detail-label">Model</div>
                <div class="detail-value">${data.model || 'Ensemble'}</div>
            </div>
            <div class="detail-cell">
                <div class="detail-label">Severity</div>
                <div class="detail-value ${sev.cls}">${sev.text}</div>
            </div>
            <div class="detail-cell">
                <div class="detail-label">Processing Time</div>
                <div class="detail-value">${data.processing_time ? data.processing_time.toFixed(2) + 's' : 'N/A'}</div>
            </div>
        </div>
        ${data.ai_explanation ? `
        <div class="explanation-block">
            <div class="explanation-title">AI Explanation</div>
            <div class="explanation-text">${data.ai_explanation}</div>
        </div>` : ''}
        ${data.action ? `
        <div class="explanation-block" style="border-color: rgba(245,158,11,0.15);">
            <div class="explanation-title" style="color: var(--warning);">Recommended Action</div>
            <div class="explanation-text">${data.action}</div>
        </div>` : ''}
        <div class="meta-row">
            <span>ID: ${data.id}</span>
            <span>MITRE ATLAS: ${data.mitre_atlas || 'N/A'}</span>
            <span>${data.timestamp}</span>
        </div>
    `;

    // Animate confidence bar
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            const bar = document.getElementById('conf-bar-fill');
            if (bar) bar.style.width = confPct + '%';
        });
    });

    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function showResultError(message) {
    const resultEmpty = document.getElementById('result-empty');
    const resultContent = document.getElementById('result-content');
    resultEmpty.style.display = 'none';
    resultContent.style.display = 'block';
    resultContent.innerHTML = `
        <div style="text-align:center;padding:24px;">
            <div style="font-size:24px;margin-bottom:12px;opacity:0.6;">&#10060;</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;color:var(--danger);">${message}</div>
        </div>
    `;
}

// ── Scan History ──

async function loadHistory() {
    try {
        const res = await fetch(API + '/api/v1/scans?limit=20');
        const data = await res.json();
        const tbody = document.getElementById('history-body');
        const countEl = document.getElementById('history-count');

        const scans = data.scans || [];
        countEl.textContent = scans.length + ' scan' + (scans.length !== 1 ? 's' : '');

        if (scans.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="empty-history">&mdash; no scans yet &mdash;</td></tr>';
            return;
        }

        tbody.innerHTML = scans.map(s => {
            const isReal = s.verdict === 'real';
            const typeBadge = s.media_type === 'audio'
                ? '<span class="badge badge-audio">Audio</span>'
                : '<span class="badge badge-image">Image</span>';
            const verdictBadge = isReal
                ? '<span class="badge badge-real">Real</span>'
                : '<span class="badge badge-fake">Deepfake</span>';
            const confPct = (s.confidence * 100).toFixed(0);
            const confClass = isReal ? 'real' : 'fake';

            const sevMap = {
                low: 'badge-sev-low',
                medium: 'badge-sev-medium',
                high: 'badge-sev-high',
                critical: 'badge-sev-critical'
            };
            const sevClass = sevMap[s.severity] || 'badge-sev-low';

            return `<tr>
                <td class="td-time">${new Date(s.timestamp).toLocaleString()}</td>
                <td class="td-file">${s.filename || '&mdash;'}</td>
                <td>${typeBadge}</td>
                <td>${verdictBadge}</td>
                <td class="td-conf ${confClass} col-confidence">${confPct}%</td>
                <td><span class="badge ${sevClass}">${(s.severity || 'low').toUpperCase()}</span></td>
            </tr>`;
        }).join('');
    } catch (err) {
        console.error('Failed to load history:', err);
    }
}

// Load history on page load
loadHistory();
