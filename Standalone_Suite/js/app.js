import { MathematicalCanvasComponent, LedgerTableComponent } from './components.js';

// Application State (Single Source of Truth)
const state = {
  currentMode: 'SLIP',
  files: [
    { name: 'Slip_KBANK_20260312_01.jpg', size: '420 KB', status: 'ready' },
    { name: 'Slip_SCB_20260312_02.png', size: '680 KB', status: 'ready' },
    { name: 'Slip_KTB_20260315_03.jpg', size: '510 KB', status: 'ready' },
    { name: 'Slip_TTB_Failed_04.jpg', size: '390 KB', status: 'failed' }
  ],
  records: [
    { date: '12/03/2026', time: '10:35', sourceBank: 'KBANK', payer: 'สมชาย ดีจริง', amount: 50000.0, payee: 'สุพัตรา มณี', destBank: 'BBL', memo: 'ค่าสินค้างวด 1', refId: '202603120948KBANK01', note: 'สแกนสำเร็จ' },
    { date: '12/03/2026', time: '11:20', sourceBank: 'SCB', payer: 'สมชาย ดีจริง', amount: 120000.0, payee: 'สุพัตรา มณี', destBank: 'KBANK', memo: '-', refId: '202603121120SCB02', note: 'สแกนสำเร็จ' },
    { date: '15/03/2026', time: '14:05', sourceBank: 'KTB', payer: 'วรรณา สดใส', amount: 75000.0, payee: 'สุพัตรา มณี', destBank: 'TTB', memo: 'เงินยืมคืน', refId: '202603151405KTB03', note: 'ล้มเหลว (สลิปซ้ำ)' },
    { date: '18/03/2026', time: '09:15', sourceBank: 'TTB', payer: 'นิภา แจ่มใส', amount: 60000.0, payee: 'กิตติศักดิ์ มีสุข', destBank: 'KBANK', memo: '-', refId: '202603180915TTB04', note: 'สแกนสำเร็จ' }
  ],
  isPasswordLocked: true
};

let canvasComponent = null;
let ledgerComponent = null;

export function initApp() {
  // Initialize Mathematical Canvas
  canvasComponent = new MathematicalCanvasComponent({
    containerId: 'canvasContainer',
    mode: state.currentMode
  });
  
  // Load sample slip
  canvasComponent.setImage('file:///C:/Users/EVE/.gemini/antigravity-ide/brain/bf13989f-db1c-43e1-8ee9-5ad567da74d4/thai_financial_slip_mockup_1789824044464.jpg');

  // Initialize Ledger Table
  ledgerComponent = new LedgerTableComponent({
    containerId: 'ledgerContainer',
    records: state.records
  });

  renderFileList();
  setupEventListeners();
}

function renderFileList() {
  const container = document.getElementById('fileListContainer');
  const countEl = document.getElementById('fileCount');
  if (!container) return;

  countEl.innerText = state.files.length;
  
  if (state.files.length === 0) {
    container.innerHTML = `<div style="text-align: center; color: var(--color-text-secondary); padding: 24px;">ยังไม่มีไฟล์ในคิว (Empty State)</div>`;
    return;
  }

  container.innerHTML = state.files.map((f, i) => `
    <div class="file-item">
      <div class="file-info">
        <span class="file-name">${f.name}</span>
        <span class="file-meta">${f.size}</span>
      </div>
      <button class="btn-trash" data-idx="${i}" title="คัดไฟล์ออก">🗑️</button>
    </div>
  `).join('');

  container.querySelectorAll('.btn-trash').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const idx = parseInt(e.currentTarget.getAttribute('data-idx'));
      state.files.splice(idx, 1);
      renderFileList();
    });
  });
}

function setupEventListeners() {
  // Mode Tabs
  document.getElementById('tabChat').addEventListener('click', () => switchMode('CHAT'));
  document.getElementById('tabSlip').addEventListener('click', () => switchMode('SLIP'));

  // Password Lock Switch
  document.getElementById('pwLockToggle').addEventListener('change', (e) => {
    state.isPasswordLocked = e.target.checked;
    document.getElementById('btnSavePdf').disabled = !state.isPasswordLocked;
    document.getElementById('btnSaveRar').disabled = !state.isPasswordLocked;
  });

  // Modal Openers
  document.getElementById('btnSummary').addEventListener('click', () => openModal('summaryModal'));
  document.getElementById('btnSavePdf').addEventListener('click', () => openModal('pdfModal'));
  document.getElementById('btnSaveRar').addEventListener('click', () => openModal('rarModal'));

  // Modal Closers
  document.querySelectorAll('.modal-close, .modal-cancel').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.modal-backdrop').forEach(m => m.classList.remove('active'));
    });
  });

  // File Upload Dropzone
  const dropzone = document.getElementById('uploadDropzone');
  const fileInput = document.getElementById('fileInput');

  dropzone.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', (e) => {
    for (const f of e.target.files) {
      state.files.push({ name: f.name, size: `${Math.round(f.size/1024)} KB`, status: 'ready' });
    }
    renderFileList();
  });

  document.getElementById('btnProcess').addEventListener('click', () => {
    alert('⚡ กำลังประมวลผล OCR และสไลซ์หน้ากระดาษ A4...');
  });

  document.getElementById('btnGenerate').addEventListener('click', () => {
    alert('🚀 เริ่มกระบวนการประทับตรา Chain-of-Custody และสร้าง Master Dossier...');
  });
}

function switchMode(mode) {
  state.currentMode = mode;
  document.getElementById('tabChat').classList.toggle('active', mode === 'CHAT');
  document.getElementById('tabSlip').classList.toggle('active', mode === 'SLIP');
  canvasComponent.setMode(mode);
}

function openModal(id) {
  document.getElementById(id).classList.add('active');
}

window.addEventListener('DOMContentLoaded', initApp);
