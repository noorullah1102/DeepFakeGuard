// DeepFakeGuard — Dashboard JavaScript

const API = '';

// --- Drop Zone Setup ---

function setupDropZone(dropId, inputId, statusId, endpoint, acceptedExts) {
    const drop = document.getElementById(dropId);
    const input = document.getElementById(inputId);
    const status = document.getElementById(statusId);

    drop.addEventListener('click', () => input.click());

    drop.addEventListener('dragover', (e) => {
        e.preventDefault();
        drop.classList.add('dragover');
    });

    drop.addEventListener('dragleave', () => {
        drop.classList.remove('dragover');
    });

    drop.addEventListener('drop', (e) => {
        e.preventDefault();
        drop.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file) uploadFile(file, status, endpoint);
    });

    input.addEventListener('change', () => {
        const file = input.files[0];
        if (file) uploadFile(file, status, endpoint);
        input.value = '';
    });
}

setupDropZone('audio-drop', 'audio-input', 'audio-status', '/api/v1/detect/audio', ['.wav', '.mp3', '.flac']);
setupDropZone('image-drop', 'image-input', 'image-status', '/api/v1/detect/image', ['.jpg', '.jpeg', '.png', '.webp']);

// --- Upload ---

async function uploadFile(file, statusEl, endpoint) {
    statusEl.classList.remove('hidden');
    statusEl.innerHTML = '<span class="text-blue-400">Analyzing...</span>';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch(API + endpoint, { method: 'POST', body: formData });
        const data = await res.json();

        if (data.error) {
            statusEl.innerHTML = `<span class="text-red-400">${data.error.message}</span>`;
            return;
        }

        showResult(data);
        statusEl.innerHTML = `<span class="text-green-400">Done — ${data.verdict} (${(data.confidence * 100).toFixed(0)}%)</span>`;
        loadHistory();
    } catch (err) {
        statusEl.innerHTML = `<span class="text-red-400">Upload failed: ${err.message}</span>`;
    }
}

// --- Result Display ---

function showResult(data) {
    const section = document.getElementById('results');
    const card = document.getElementById('result-card');
    section.classList.remove('hidden');

    const verdictClass = data.verdict === 'real' ? 'verdict-real' : 'verdict-synthetic';
    const severityColors = { low: 'bg-green-600', medium: 'bg-yellow-600', high: 'bg-orange-600', critical: 'bg-red-600' };
    const sevBadge = severityColors[data.severity] || 'bg-gray-600';
    const confPct = (data.confidence * 100).toFixed(1);

    let analysisRows = '';
    if (data.analysis) {
        for (const [key, value] of Object.entries(data.analysis)) {
            if (key === 'mel_spectrogram' || key === 'sample_rate') continue;
            const display = typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value;
            analysisRows += `<div class="flex justify-between py-1 border-b border-gray-800">
                <span class="text-gray-400">${formatKey(key)}</span>
                <span class="font-mono text-sm">${display}</span>
            </div>`;
        }
    }

    card.innerHTML = `
        <div class="flex items-center justify-between mb-6">
            <div>
                <span class="text-3xl font-bold ${verdictClass} uppercase">${data.verdict}</span>
                <span class="ml-3 text-sm text-gray-400">${data.media_type}</span>
            </div>
            <span class="px-3 py-1 rounded-full text-xs font-bold text-white ${sevBadge}">${data.severity.toUpperCase()}</span>
        </div>

        <div class="mb-6">
            <div class="flex justify-between text-sm mb-1">
                <span>Confidence</span>
                <span class="font-mono">${confPct}%</span>
            </div>
            <div class="w-full bg-gray-800 rounded-full h-3">
                <div class="confidence-bar h-3 rounded-full ${data.verdict === 'real' ? 'bg-green-500' : 'bg-red-500'}"
                     style="width: ${confPct}%"></div>
            </div>
        </div>

        <div class="mb-6">
            <h4 class="font-semibold mb-2">Analysis</h4>
            <div class="bg-gray-800 rounded-lg p-4 text-sm">${analysisRows || '<p class="text-gray-500">No details available</p>'}</div>
        </div>

        ${data.ai_explanation ? `
        <div class="mb-6">
            <h4 class="font-semibold mb-2">AI Explanation</h4>
            <p class="text-gray-300 text-sm leading-relaxed bg-gray-800 rounded-lg p-4">${data.ai_explanation}</p>
        </div>` : ''}

        ${data.action ? `
        <div class="mb-4">
            <h4 class="font-semibold mb-2">Recommended Action</h4>
            <p class="text-yellow-300 text-sm bg-gray-800 rounded-lg p-4">${data.action}</p>
        </div>` : ''}

        <div class="text-xs text-gray-600 mt-4">
            ID: ${data.id} | MITRE ATLAS: ${data.mitre_atlas} | ${data.timestamp}
        </div>
    `;

    section.scrollIntoView({ behavior: 'smooth' });
}

function formatKey(key) {
    return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

// --- Scan History ---

async function loadHistory() {
    try {
        const res = await fetch(API + '/api/v1/scans?limit=20');
        const data = await res.json();
        const tbody = document.getElementById('history-body');

        if (!data.scans || data.scans.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="px-4 py-8 text-center text-gray-500">No scans yet</td></tr>';
            return;
        }

        tbody.innerHTML = data.scans.map(s => {
            const verdictClass = s.verdict === 'real' ? 'text-green-400' : 'text-red-400';
            const sevColors = { low: 'text-green-400', medium: 'text-yellow-400', high: 'text-orange-400', critical: 'text-red-400' };
            const confPct = (s.confidence * 100).toFixed(0);
            return `<tr class="hover:bg-gray-800/50">
                <td class="px-4 py-3 text-gray-400">${new Date(s.timestamp).toLocaleString()}</td>
                <td class="px-4 py-3">${s.filename || '—'}</td>
                <td class="px-4 py-3 text-gray-400">${s.media_type}</td>
                <td class="px-4 py-3 font-semibold ${verdictClass}">${s.verdict}</td>
                <td class="px-4 py-3 font-mono">${confPct}%</td>
                <td class="px-4 py-3 ${sevColors[s.severity] || ''}">${s.severity}</td>
            </tr>`;
        }).join('');
    } catch (err) {
        console.error('Failed to load history:', err);
    }
}

// Load history on page load
loadHistory();
