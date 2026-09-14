// Slip Mode GUI MVP - app.js
// All interactions are client‑side using mock data.

(() => {
  // ---------- State ----------
  const state = {
    slipId: null,
    imageDataUrl: null,
    fields: {},
    confidence: {},
    history: [] // loaded from localStorage
  };

  // ---------- DOM Elements ----------
  const uploadArea = document.getElementById('upload-area');
  const browseButton = document.getElementById('browse-button');
  const fileInput = document.getElementById('file-input');
  const resetButton = document.getElementById('reset-button');
  const clearButton = document.getElementById('clear-button');

  const previewSection = document.getElementById('preview-section');
  const imagePreview = document.getElementById('image-preview');

  const ocrSection = document.getElementById('ocr-section');
  const ocrForm = document.getElementById('ocr-form');

  const validationSection = document.getElementById('validation-section');
  const validationList = document.getElementById('validation-list');

  const exportSection = document.getElementById('export-section');
  const exportExcelBtn = document.getElementById('export-excel');
  const exportCsvBtn = document.getElementById('export-csv');
  const exportJsonBtn = document.getElementById('export-json');

  const statusMessage = document.getElementById('status-message');
  const toastContainer = document.getElementById('toast-container');
  const loadingOverlay = document.getElementById('loading-overlay');
  const confirmDialog = document.getElementById('confirm-dialog');
  const confirmMessage = document.getElementById('confirm-message');
  const confirmYes = document.getElementById('confirm-yes');
  const confirmNo = document.getElementById('confirm-no');

  const historyList = document.getElementById('history-list');

  // ---------- Utilities ----------
  function setStatus(msg) { statusMessage.textContent = msg; }

  function showToast(msg, type = 'info') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    toastContainer.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
  }

  function showLoading(show) {
    loadingOverlay.classList.toggle('visible', show);
  }

  function showConfirm(message, onYes, onNo) {
    confirmMessage.textContent = message;
    confirmDialog.classList.add('visible');
    const yesHandler = () => { cleanup(); onYes(); };
    const noHandler = () => { cleanup(); onNo(); };
    confirmYes.addEventListener('click', yesHandler, { once: true });
    confirmNo.addEventListener('click', noHandler, { once: true });
    function cleanup() { confirmDialog.classList.remove('visible'); }
  }

  function loadHistory() {
    const raw = localStorage.getItem('slipHistory');
    if (raw) state.history = JSON.parse(raw);
    renderHistory();
  }

  function saveHistory() {
    localStorage.setItem('slipHistory', JSON.stringify(state.history));
  }

  function renderHistory() {
    historyList.innerHTML = '';
    state.history.slice().reverse().forEach(item => {
      const li = document.createElement('li');
      li.style.cursor = 'pointer';
      li.title = new Date(item.timestamp).toLocaleString();
      li.innerHTML = `<img src="${item.thumbnail}" alt="thumb" style="width:40px;height:40px;object-fit:cover;border-radius:4px;margin-right:4px;"/>${item.timestamp.slice(0,16)}`;
      li.addEventListener('click', () => loadHistoryItem(item));
      historyList.appendChild(li);
    });
  }

  function addToHistory() {
    const thumbnail = state.imageDataUrl;
    const entry = {
      id: state.slipId,
      thumbnail,
      timestamp: new Date().toISOString(),
      fields: { ...state.fields }
    };
    state.history.push(entry);
    saveHistory();
    renderHistory();
  }

  function loadHistoryItem(item) {
    state.slipId = item.id;
    state.imageDataUrl = item.thumbnail;
    state.fields = { ...item.fields };
    // Mock confidence (random for demo)
    state.confidence = generateMockConfidence();
    renderAll();
    showToast('History item loaded');
  }

  // ---------- Mock Data ----------
  function generateMockResult() {
    return {
      fields: {
        date: '2024-03-15',
        time: '14:30',
        amount: '1234.56',
        reference: 'ABC123',
        payer: 'John Doe',
        payee: 'Acme Corp'
      },
      confidence: generateMockConfidence()
    };
  }

  function generateMockConfidence() {
    return {
      date: 0.95,
      time: 0.92,
      amount: 0.98,
      reference: 0.88,
      payer: 0.90,
      payee: 0.93
    };
  }

function parseOCRResult(text) {
  // Simple heuristic parser for bank slip OCR output
  const lines = text.split(/\r?\n/).map(l => l.trim()).filter(l => l);
  const result = {
    fields: {},
    confidence: {}
  };
  // Helper to set field and confidence
  const setField = (key, value) => {
    result.fields[key] = value;
    result.confidence[key] = calculateConfidence(key, value);
  };
  // Regex patterns
  const patterns = {
    date: /\d{4}[\-/]\d{2}[\-/]\d{2}/,
    time: /\d{2}:\d{2}/,
    amount: /[\d,.]+\s?(?:USD|THB|EUR|\$|฿)?/i,
    reference: /ref[:\s]*([A-Za-z0-9]+)/i,
    payer: /payer[:\s]*([A-Za-z\s]+)/i,
    payee: /payee[:\s]*([A-Za-z\s]+)/i
  };
  lines.forEach(line => {
    if (!result.fields.date) {
      const m = line.match(patterns.date);
      if (m) setField('date', m[0]);
    }
    if (!result.fields.time) {
      const m = line.match(patterns.time);
      if (m) setField('time', m[0]);
    }
    if (!result.fields.amount) {
      const m = line.match(patterns.amount);
      if (m) setField('amount', m[0].replace(/[\s]/g, ''));
    }
    if (!result.fields.reference) {
      const m = line.match(patterns.reference);
      if (m) setField('reference', m[1]);
    }
    if (!result.fields.payer) {
      const m = line.match(patterns.payer);
      if (m) setField('payer', m[1].trim());
    }
    if (!result.fields.payee) {
      const m = line.match(patterns.payee);
      if (m) setField('payee', m[1].trim());
    }
  });
  // Fallback to mock data if any field missing
  const mock = generateMockResult();
  for (const key of Object.keys(mock.fields)) {
    if (!result.fields[key]) {
      result.fields[key] = mock.fields[key];
      result.confidence[key] = mock.confidence[key];
    }
  }
  return result;
}

  // ---------- Rendering ----------
  function renderAll() {
    // Image preview
    if (state.imageDataUrl) {
      imagePreview.src = state.imageDataUrl;
      previewSection.classList.remove('hidden');
    }
    // OCR fields
    ['date','time','amount','reference','payer','payee'].forEach(key => {
      const el = document.getElementById(`field-${key}`);
      if (el) el.value = state.fields[key] || '';
    });
    ocrSection.classList.remove('hidden');
    // Validation
    renderValidation();
    validationSection.classList.remove('hidden');
    // Export buttons
    exportSection.classList.remove('hidden');
  }

  function renderValidation() {
    validationList.innerHTML = '';
    Object.entries(state.confidence).forEach(([key, conf]) => {
      const item = document.createElement('div');
      item.className = 'validation-item';
      const label = document.createElement('span');
      label.textContent = `${key.charAt(0).toUpperCase() + key.slice(1)}:`;
      const bar = document.createElement('div');
      bar.className = 'progress-bar';
      const inner = document.createElement('div');
      inner.className = 'progress-bar-inner';
      inner.style.width = `${conf * 100}%`;
      bar.appendChild(inner);
      const percent = document.createElement('span');
      percent.textContent = `${Math.round(conf * 100)}%`;
      item.appendChild(label);
      item.appendChild(bar);
      item.appendChild(percent);
      validationList.appendChild(item);
    });
  }

  // ---------- Event Handlers ----------
  function handleFile(file) {
    if (!file.type.startsWith('image/')) {
      showToast('Only image files are allowed', 'warning');
      return;
    }
    const reader = new FileReader();
    reader.onload = e => {
      state.imageDataUrl = e.target.result;
      state.slipId = crypto.randomUUID();
      renderAll();
      setStatus('Processing OCR...');
    showLoading(true);
    // Perform OCR using Tesseract.js
    Tesseract.recognize(state.imageDataUrl, 'eng', {
      logger: m => console.log(m)
    })
      .then(({ data: { text } }) => {
        const parsed = parseOCRResult(text);
        state.fields = parsed.fields;
        state.confidence = parsed.confidence;
        renderAll();
        addToHistory();
        showLoading(false);
        setStatus('Ready');
        showToast('OCR completed');
      })
      .catch(err => {
        console.error('OCR error:', err);
        showLoading(false);
        setStatus('Error');
        showToast('OCR failed', 'error');
      });
    };
    reader.readAsDataURL(file);
  }

  uploadArea.addEventListener('dragover', e => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
  });
  uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('dragover'));
  uploadArea.addEventListener('drop', e => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });

  browseButton.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', () => {
    if (fileInput.files[0]) handleFile(fileInput.files[0]);
  });

  // Editable fields – live validation
  ocrForm.addEventListener('input', e => {
    const name = e.target.name;
    const value = e.target.value;
    state.fields[name] = value;
    // Simple validation: non‑empty, numeric amount, date pattern
    const confidence = calculateConfidence(name, value);
    state.confidence[name] = confidence;
    renderValidation();
  });

  function calculateConfidence(field, value) {
    if (!value) return 0;
    switch (field) {
      case 'amount':
        return /^\d+(?:[.,]\d{2})?$/.test(value) ? 0.95 : 0.4;
      case 'date':
        return /\d{4}-\d{2}-\d{2}/.test(value) ? 0.9 : 0.3;
      case 'time':
        return /\d{2}:\d{2}/.test(value) ? 0.9 : 0.3;
      default:
        return value.trim().length > 2 ? 0.85 : 0.4;
    }
  }

  resetButton.addEventListener('click', () => {
    if (!state.slipId) return;
    showConfirm('Reset current slip?', () => {
      state.slipId = null;
      state.imageDataUrl = null;
      state.fields = {};
      state.confidence = {};
      previewSection.classList.add('hidden');
      ocrSection.classList.add('hidden');
      validationSection.classList.add('hidden');
      exportSection.classList.add('hidden');
      setStatus('Ready');
      showToast('Slip reset');
    }, () => {});
  });

  clearButton.addEventListener('click', () => {
    showConfirm('Clear all history?', () => {
      state.history = [];
      saveHistory();
      renderHistory();
      showToast('History cleared');
    }, () => {});
  });

  // ---------- Export ----------
  function exportToExcel() {
    const ws_data = [
      ['Field', 'Value'],
      ...Object.entries(state.fields)
    ];
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(ws_data);
    XLSX.utils.book_append_sheet(wb, ws, 'Slip');
    XLSX.writeFile(wb, `Slip_${state.slipId || 'new'}.xlsx`);
    showToast('Exported to Excel');
  }

  function exportToCsv() {
    const header = Object.keys(state.fields).join(',');
    const row = Object.values(state.fields).map(v => `"${v}"`).join(',');
    const csv = `${header}\n${row}`;
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Slip_${state.slipId || 'new'}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Exported to CSV');
  }

  function exportToJson() {
    const json = JSON.stringify(state.fields, null, 2);
    const blob = new Blob([json], { type: 'application/json;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Slip_${state.slipId || 'new'}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Exported to JSON');
  }

  exportExcelBtn.addEventListener('click', exportToExcel);
  exportCsvBtn.addEventListener('click', exportToCsv);
  exportJsonBtn.addEventListener('click', exportToJson);

  // ---------- Keyboard Shortcuts ----------
  document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 's') { // Ctrl+S -> Export Excel
      e.preventDefault();
      exportToExcel();
    }
    if (e.ctrlKey && e.key === 'r') { // Ctrl+R -> Reset
      e.preventDefault();
      resetButton.click();
    }
    if (e.ctrlKey && e.key === 'l') { // Ctrl+L -> Load file picker
      e.preventDefault();
      browseButton.click();
    }
  });

  // ---------- Initialization ----------
  loadHistory();
  setStatus('Ready');
})();
