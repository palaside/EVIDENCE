/**
 * DIGITAL EVIDENCE — MULTITIER COMPONENTS (LAYER 1 & 2)
 * Pure vanilla component library driven by CSS Tokens
 */

// ----------------------------------------------------------------------------
// Layer 1: Primitive Components
// ----------------------------------------------------------------------------
export function createButton({ label, icon = '', variant = 'primary', onClick, id = '' }) {
  const btn = document.createElement('button');
  btn.className = `btn btn-${variant}`;
  if (id) btn.id = id;
  btn.innerHTML = `${icon ? `<span class="btn-icon">${icon}</span>` : ''}<span>${label}</span>`;
  if (onClick) btn.addEventListener('click', onClick);
  return btn;
}

export function createBadge({ text, variant = 'sky' }) {
  const span = document.createElement('span');
  span.className = `badge badge-${variant}`;
  span.innerText = text;
  return span;
}

// ----------------------------------------------------------------------------
// Layer 2: Composite Components
// ----------------------------------------------------------------------------

/**
 * Mathematical Aspect-Ratio Centered Canvas Component (C-001)
 */
export class MathematicalCanvasComponent {
  constructor({ containerId, mode = 'SLIP', timestamp = '31/6/69 : 12.00' }) {
    this.container = document.getElementById(containerId);
    this.mode = mode;
    this.timestamp = timestamp;
    this.paperW = 645;
    this.paperH = 890;
    this.render();
  }

  setMode(mode) {
    this.mode = mode;
    const modeEl = this.container.querySelector('.canvas-mode-tag');
    if (modeEl) modeEl.innerText = `[ MODE : ${mode} ]`;
  }

  setImage(src) {
    const img = this.container.querySelector('#activeEvidenceImg');
    if (img) {
      img.src = src;
      img.onload = () => this.calculatePlacement(img);
    }
  }

  calculatePlacement(img) {
    const W_orig = img.naturalWidth || 800;
    const H_orig = img.naturalHeight || 1000;
    const stageW = 645;
    const stageH = 760;

    // Mathematical Scale Factor
    const scale = Math.min(stageW / W_orig, stageH / H_orig);
    const W_new = Math.floor(W_orig * scale);
    const H_new = Math.floor(H_orig * scale);

    const x_start = Math.floor((stageW - W_new) / 2);
    const y_start = Math.floor((stageH - H_new) / 2);

    img.style.width = `${W_new}px`;
    img.style.height = `${H_new}px`;
    img.style.left = `${x_start}px`;
    img.style.top = `${y_start}px`;
    img.style.position = 'absolute';

    console.log(`[Math Centered] Size: ${W_new}x${H_new} at (${x_start}, ${y_start}) | Center: (${x_start + W_new/2}, ${y_start + H_new/2})`);
  }

  render() {
    this.container.innerHTML = `
      <div class="evidence-paper-frame">
        <div class="canvas-header-bar">
          <div class="canvas-brand-tag">
            <span style="color: var(--color-accent-primary);">🛡️ DIGITAL EVIDENCE</span>
            <span class="canvas-mode-tag">[ MODE : ${this.mode} ]</span>
          </div>
          <div class="canvas-timestamp">${this.timestamp}</div>
        </div>
        <div class="canvas-stage-area" style="position: relative; flex: 1; margin: 12px 0;">
          <img id="activeEvidenceImg" class="evidence-img" alt="พยานหลักฐานดิจิทัล" style="max-width: 100%; max-height: 100%; border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
        </div>
        <div class="canvas-footer-disclaimer">
          DIGITAL EVIDENCE เป็นเพียงการเครื่องมืออำนวยความสะดวกให้กับผู้ว่าจ้าง โดยไม่ได้ดัดแปลง แก้ไข เพิ่ม-ลบ เนื้อหา จากต้นฉบับใดๆ<br>
          และไม่มีส่วนเกี่ยวข้องใดๆกับเนื้อหาในเอกสาร เป็นเพียงเครื่องมือที่ทำงานเกี่ยวกับระบบไฟล์ เอกสารแบบอิเล็กทรอนิกส์ เท่านั้น
        </div>
      </div>
    `;
  }
}

/**
 * 11-Column Forensic Ledger Table Component (C-002)
 */
export class LedgerTableComponent {
  constructor({ containerId, records = [] }) {
    this.container = document.getElementById(containerId);
    this.records = records;
    this.render();
  }

  setRecords(records) {
    this.records = records;
    this.render();
  }

  render() {
    let totalSum = 0;
    const rowsHtml = this.records.map((r, idx) => {
      const isFailed = r.status === 'failed' || (r.note && r.note.includes('ล้มเหลว'));
      if (!isFailed && typeof r.amount === 'number') {
        totalSum += r.amount;
      }
      return `
        <tr class="${isFailed ? 'row-failed' : ''}">
          <td>${idx + 1}</td>
          <td>${r.date || '-'}</td>
          <td>${r.time || '-'}</td>
          <td>${r.sourceBank || '-'}</td>
          <td>${r.payer || '-'}</td>
          <td style="font-family: var(--font-family-mono);">${typeof r.amount === 'number' ? r.amount.toLocaleString('th-TH', {minimumFractionDigits: 2}) : '-'}</td>
          <td>${r.payee || '-'}</td>
          <td>${r.destBank || '-'}</td>
          <td>${r.memo || '-'}</td>
          <td style="font-family: var(--font-family-mono); font-size: 11px;">${r.refId || '-'}</td>
          <td>${isFailed ? `<span style="color: var(--color-state-failed-text); font-weight: 700;">⚠️ ${r.note}</span>` : `<span style="color: var(--color-state-success);">✓ สำเร็จ</span>`}</td>
        </tr>
      `;
    }).join('');

    const avgSum = this.records.length > 0 ? totalSum / this.records.length : 0;

    this.container.innerHTML = `
      <div class="ledger-wrapper">
        <table class="forensic-table">
          <thead>
            <tr>
              <th>ลำดับ</th><th>วันที่</th><th>เวลา</th><th>ธนาคารผู้โอน</th><th>ชื่อผู้โอน</th>
              <th>จำนวนเงิน (บาท)</th><th>ชื่อผู้รับ</th><th>ธนาคารผู้รับ</th><th>บันทึกช่วยจำ</th>
              <th>รหัสอ้างอิง</th><th>หมายเหตุ</th>
            </tr>
          </thead>
          <tbody>
            ${rowsHtml || '<tr><td colspan="11" style="text-align: center; color: var(--color-text-secondary); padding: 24px;">ยังไม่มีข้อมูลในตาราง</td></tr>'}
          </tbody>
          <tfoot>
            <tr class="table-summary-row">
              <td colspan="5" style="text-align: right; font-weight: 700;">ยอดรวมทั้งหมด (Total Sum):</td>
              <td><span class="double-underline">${totalSum.toLocaleString('th-TH', {minimumFractionDigits: 2})}</span></td>
              <td colspan="2" style="text-align: right; font-weight: 700;">ยอดเฉลี่ยสะสม (Average):</td>
              <td><span class="double-underline">${avgSum.toLocaleString('th-TH', {minimumFractionDigits: 2})}</span></td>
              <td colspan="2"></td>
            </tr>
          </tfoot>
        </table>
      </div>
    `;
  }
}
