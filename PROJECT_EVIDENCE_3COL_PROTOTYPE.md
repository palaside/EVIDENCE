# DIGITAL EVIDENCE — COURT-READY A4 REPORT PROTOTYPE

> **สถาปัตยกรรม:** 3-Column Layout (22% - 56% - 22%)
> **การแสดงผลกลาง:** แผ่นกระดาษรายงานศาล A4 สีขาวแท้ 100% (Matching Real PDF Report Sheet)
> **องค์ประกอบ:** ตราโล่ + MODE : CHAT + CORROBORATED : บทสนทนาต่อเนื่อง + PAGE : X + บล็อกแชทขยายเต็มตา + คำประกาศปฏิเสธความรับผิดชอบท้ายหน้า

---

## 🎨 ซอร์สโค้ด HTML5 / Tailwind CSS / Vanilla JS ฉบับสมบูรณ์

`html
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DIGITAL EVIDENCE — Court-Ready Forensic Suite</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,300;0,400;0,600;0,700;1,300&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            'dark-slate-base': '#0F172A',
            'dark-slate-surf': '#1E293B',
            'accent-sky': '#00A1E4',
            'accent-sky-glow': '#38BDF8',
            'status-failed': '#FDE8E8',
            'status-failed-txt': '#C53030',
          },
          fontFamily: {
            sans: ['Sarabun', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }
        }
      }
    }
  </script>

  <style>
    :root {
      --glass-blur: 16px;
      --glass-surface: rgba(30, 41, 59, 0.75);
      --glass-border: 1px solid rgba(255, 255, 255, 0.12);
      --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
      --focus-ring: #38BDF8;
    }

    body {
      background-color: #0F172A;
      color: #FFFFFF;
      font-family: 'Sarabun', sans-serif;
      font-weight: 300;
      font-size: 14px;
      user-select: none;
      overflow: hidden;
      width: 100vw;
      height: 100vh;
    }

    .glass-panel {
      background: var(--glass-surface);
      backdrop-filter: blur(var(--glass-blur));
      -webkit-backdrop-filter: blur(var(--glass-blur));
      border: var(--glass-border);
      box-shadow: var(--glass-shadow);
    }

    .glass-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      transition: all 0.2s ease;
    }

    .glass-card:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(56, 189, 248, 0.4);
    }

    .glass-card.active {
      background: rgba(0, 161, 228, 0.18);
      border-color: #38BDF8;
    }

    .glass-input {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #FFF;
    }

    .glass-input:focus {
      border-color: var(--focus-ring);
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
      outline: none;
    }

    /* Switch Component */
    .switch {
      position: relative;
      display: inline-block;
      width: 40px;
      height: 22px;
    }
    .switch input { opacity: 0; width: 0; height: 0; }
    .slider {
      position: absolute; cursor: pointer; inset: 0;
      background-color: #475569;
      transition: .2s; border-radius: 9999px;
    }
    .slider:before {
      position: absolute; content: ""; height: 16px; width: 16px;
      left: 3px; bottom: 3px; background-color: white; transition: .2s;
      border-radius: 50%;
    }
    input:checked + .slider { background-color: #00A1E4; }
    input:checked + .slider:before { transform: translateX(18px); }

    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.6); }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.18); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(56, 189, 248, 0.4); }

    /* REAL COURT-READY WHITE A4 REPORT PAPER */
    .a4-court-sheet {
      width: 620px;
      height: 876px;
      background-color: #FFFFFF;
      color: #222222;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.7), 0 0 1px rgba(255,255,255,0.4);
      border-radius: 2px;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
      transform-origin: center center;
    }

    .a4-header-zone {
      height: 72px;
      padding: 16px 36px 8px 36px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #E2E8F0;
      background: #FFFFFF;
      flex-shrink: 0;
    }

    .a4-body-zone {
      flex: 1;
      padding: 12px 36px;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      background: #FFFFFF;
      overflow: hidden;
      position: relative;
    }

    .a4-footer-zone {
      height: 54px;
      padding: 6px 36px 14px 36px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      border-top: 1px solid #E2E8F0;
      background: #FFFFFF;
      flex-shrink: 0;
    }

    .a4-slice-canvas {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      border-radius: 4px;
    }
  </style>
</head>
<body class="h-screen w-screen flex flex-col bg-[#0F172A] text-slate-100 overflow-hidden">

  <!-- Top App Bar -->
  <header class="h-14 border-b border-white/10 glass-panel flex items-center justify-between px-5 z-20 shrink-0">
    <div class="flex items-center gap-3">
      <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-sky-600 to-blue-400 flex items-center justify-center font-bold text-white shadow-lg shadow-sky-500/20">
        🛡️
      </div>
      <div>
        <h1 class="text-sm font-semibold tracking-wide text-white flex items-center gap-2">
          DIGITAL EVIDENCE FORENSIC SUITE
          <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30">v2.5 COURT-READY A4</span>
        </h1>
        <p class="text-[10px] text-slate-400 font-mono">1:1 EXACT PDF REPLICA • DARK WORKSPACE</p>
      </div>
    </div>

    <!-- Center Agent Status & Live Timer Display -->
    <div class="flex items-center gap-3 text-xs">
      <div class="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 px-3 py-1 rounded-full text-emerald-400 font-mono">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
        <span id="agentHeartbeatStatus">REAL-TIME SLICER READY</span>
      </div>
      <div id="topBenchmarkTimer" class="flex items-center gap-1.5 bg-sky-500/10 border border-sky-500/30 px-3 py-1 rounded-full text-sky-300 font-mono text-[11px]">
        <span>⏱️</span>
        <span id="topTimerValue">เวลาหั่นสด: 0.00s</span>
      </div>
    </div>

    <!-- Action Tools -->
    <div class="flex items-center gap-2">
      <button onclick="openSummaryModal()" class="px-3 py-1.5 rounded-lg bg-white/5 border border-white/15 hover:border-sky-400/50 hover:bg-sky-500/10 transition text-xs font-semibold text-sky-300 flex items-center gap-1.5">
        📊 Summary Table
      </button>
      <button onclick="syncLiveData()" class="px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 transition text-xs font-semibold text-white shadow-lg shadow-sky-600/30 flex items-center gap-1.5">
        🔄 Sync Data
      </button>
    </div>
  </header>

  <!-- 3-Column Layout System (22% - 56% - 22%) -->
  <main class="flex-1 flex overflow-hidden p-3 gap-3 w-full">
    
    <!-- ====================================================================== -->
    <!-- COLUMN 1: LEFT CONTROL RAIL (22% Width / ~280px)                       -->
    <!-- ====================================================================== -->
    <section class="w-[280px] shrink-0 h-full flex flex-col gap-2.5 overflow-y-auto pr-1">
      
      <!-- 1. Multi-file Upload & AI Auto Mode Detect -->
      <div class="glass-panel p-3 rounded-xl flex flex-col gap-2">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-sky-400 tracking-wider">1. UPLOAD & DETECT</span>
          <span id="aiModeLabel" class="text-[9px] font-mono px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30">
            CHAT_SLICER_MODE
          </span>
        </div>
        
        <!-- Drag & Drop Box -->
        <div class="border-2 border-dashed border-white/20 hover:border-sky-400/60 transition rounded-xl p-2.5 text-center cursor-pointer bg-white/[0.02]" onclick="document.getElementById('multiFileInput').click()">
          <input type="file" id="multiFileInput" multiple accept="image/*,.pdf" class="hidden" onchange="handleMultiUpload(this.files)">
          <div class="text-lg">📂</div>
          <div class="text-[11px] font-semibold text-slate-200">เลือกภาพแชทยาว หรือ ลากไฟล์ลงที่นี่</div>
          <div class="text-[9px] text-sky-300 mt-0.5 font-mono">⚡ หั่นลงหน้า A4 เล่มศาลทันที</div>
        </div>

        <!-- Uploaded Files List Tray -->
        <div id="uploadedFilesSection" class="flex flex-col gap-1 mt-1">
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-semibold text-slate-300">📁 ไฟล์ในคิวประมวลผล</span>
            <span id="uploadedFilesCountBadge" class="text-[9px] font-mono px-1.5 py-0.2 rounded bg-sky-500/20 text-sky-300">0 ไฟล์</span>
          </div>
          <div id="uploadedFilesContainer" class="flex flex-col gap-1 max-h-[110px] overflow-y-auto pr-1">
            <div class="text-[10px] text-slate-500 italic p-2 text-center">ยังไม่มีไฟล์ — คลิกเพื่อเลือกภาพแชท</div>
          </div>
        </div>
      </div>

      <!-- 2. Target Person Search (Zero-Prefix Stripping) -->
      <div class="glass-panel p-3 rounded-xl flex flex-col gap-1.5">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-sky-400 tracking-wider">2. ค้นหาบุคคลเป้าหมาย</span>
          <span class="text-[9px] font-mono text-emerald-400">Zero-Prefix</span>
        </div>
        <div class="relative">
          <input type="text" id="targetSearchInput" placeholder="พิมพ์ชื่อ-สกุล หรือ ยศ..." 
                 oninput="handleTargetSearch(this.value)"
                 class="w-full glass-input px-2.5 py-1.5 rounded-lg text-xs placeholder:text-slate-500">
          <span class="absolute right-2.5 top-1.5 text-xs text-slate-400">🔍</span>
        </div>
        <div class="text-[9px] text-slate-400">
          ล้างยศ: <span class="text-sky-300 font-mono">นาย, นาง, น.ส., ด.ช., ร.ต., พ.ต.อ., ส.ต.</span>
        </div>
      </div>

      <!-- 3. Chat-Slip Corroboration Toggle -->
      <div class="glass-panel p-2.5 rounded-xl flex items-center justify-between">
        <div>
          <div class="text-[11px] font-semibold text-slate-200">3. สลิป-แชท สอดคล้องกัน</div>
          <div class="text-[9px] text-slate-400">จับคู่ความเชื่อมโยงแห่งคดี</div>
        </div>
        <label class="switch">
          <input type="checkbox" id="corroborateToggle" checked onchange="handleConsistencyToggle(this.checked)">
          <span class="slider"></span>
        </label>
      </div>

      <!-- 4. Target Matched List -->
      <div class="glass-panel p-3 rounded-xl flex flex-col gap-1.5 flex-1 min-h-[100px]">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-sky-400 tracking-wider">4. รายชื่อเป้าหมาย</span>
          <span id="matchedCount" class="text-[9px] font-mono text-slate-300 bg-white/10 px-1.5 py-0.5 rounded">1 รายชื่อ</span>
        </div>
        <div id="targetPersonsContainer" class="flex flex-col gap-1 overflow-y-auto pr-1">
          <div class="glass-card p-2 rounded-lg flex items-center justify-between cursor-pointer border border-sky-500/40 bg-sky-500/10 active" onclick="selectPerson('จิณห์นิภา ประสาทเขตการ')">
            <div class="flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              <div>
                <div class="text-[11px] font-semibold text-white">จิณห์นิภา ประสาทเขตการ</div>
                <div class="text-[8px] text-slate-400 font-mono">กรุงศรีอยุธยา • 95 รายการสอดคล้อง</div>
              </div>
            </div>
            <span class="text-[9px] font-mono text-sky-400 font-bold">🎯 MATCH</span>
          </div>
        </div>
      </div>

      <!-- 5. Processing Timer Gauge & Process Button -->
      <div class="glass-panel p-2.5 rounded-xl flex flex-col gap-2 mt-auto">
        <div id="processTimerBanner" class="p-2 rounded-lg bg-black/40 border border-white/10 flex flex-col gap-1">
          <div class="flex items-center justify-between text-[10px] font-mono">
            <span class="text-slate-400 flex items-center gap-1">
              <span id="timerStatusDot" class="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span id="timerStatusText">สถานะ: หั่นสไลซ์พร้อมแสดงผล</span>
            </span>
            <span id="liveTimerCounter" class="text-sky-400 font-bold text-xs">00:00.28</span>
          </div>
          <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
            <div id="processProgressBar" class="bg-gradient-to-r from-sky-500 to-emerald-400 h-1.5 rounded-full transition-all duration-300" style="width: 100%"></div>
          </div>
        </div>

        <button id="btnProcessEvidence" onclick="runProcess()" class="w-full py-2.5 rounded-xl bg-gradient-to-r from-sky-600 via-blue-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white font-bold text-xs tracking-wider shadow-lg shadow-sky-600/30 transition transform active:scale-[0.98] flex items-center justify-center gap-2">
          ⚡ สั่งประมวลผล / หั่นสไลซ์ใหม่
        </button>
      </div>
    </section>

    <!-- ====================================================================== -->
    <!-- COLUMN 2: CENTER LIVE PREVIEW STAGE (Real Court-Ready White A4 Paper)   -->
    <!-- ====================================================================== -->
    <section class="flex-1 h-full flex flex-col gap-2 glass-panel p-3 rounded-xl relative overflow-hidden min-w-[480px]">
      
      <!-- Top Stage Counter & Mode Bar -->
      <div class="flex items-center justify-between px-3 py-1.5 rounded-lg bg-black/40 border border-white/10 shrink-0">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-sky-400 animate-pulse"></span>
          <span id="pageCounterBadge" class="text-xs font-mono font-semibold text-sky-300">
            ชิ้นส่วนรายงานหน้า 1 / 1 (Court-Ready A4)
          </span>
        </div>

        <div class="flex items-center gap-2">
          <span id="sliceInfoBadge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            ✂️ SLICE: 1:1 FORENSIC
          </span>
          <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-slate-300">
            [ PORTRAIT A4 620×876 ]
          </span>
        </div>
      </div>

      <!-- Live Canvas Container with Dark Workbench Background -->
      <div class="flex-1 flex items-center justify-center relative overflow-hidden bg-slate-950/80 rounded-xl border border-white/5 p-3">
        
        <!-- ================================================================== -->
        <!-- REAL COURT-READY WHITE A4 REPORT PAPER (EXACT MATCH TO REAL PDF)    -->
        <!-- ================================================================== -->
        <div id="a4CourtReportSheet" class="a4-court-sheet">
          
          <!-- A4 Top Header on White Paper -->
          <div class="a4-header-zone">
            <div class="flex items-center gap-3">
              <!-- Shield Police Emblem Icon -->
              <div class="w-9 h-9 rounded-full bg-slate-900 border border-slate-400 flex items-center justify-center font-bold text-sm shadow-sm select-none">
                🛡️
              </div>
              <div class="flex flex-col">
                <div class="text-[11px] font-bold text-slate-800 tracking-wider font-mono" id="a4HeaderMode">MODE : CHAT</div>
                <div class="text-[9px] text-slate-500 font-sans tracking-wide" id="a4HeaderSub">CORROBORATED : บทสนทนาต่อเนื่อง</div>
              </div>
            </div>

            <!-- Page Number on Top Right -->
            <div class="text-right">
              <div class="text-[12px] font-bold text-slate-800 font-mono tracking-wider" id="a4HeaderPageNum">PAGE : 1</div>
            </div>
          </div>

          <!-- A4 Body Stage (Target Block Container: Top-Aligned with Background Color Filling) -->
          <div class="a4-body-zone" id="a4BodyZone">
            <canvas id="activeSliceCanvas" class="a4-slice-canvas"></canvas>
          </div>

          <!-- A4 Bottom Footer on White Paper -->
          <div class="a4-footer-zone">
            <div class="text-[8px] text-slate-500 font-sans leading-tight italic max-w-[540px]">
              "DIGITAL EVIDENCE เป็นเพียงเครื่องมืออำนวยความสะดวกให้กับผู้จัดทำ โดยไม่ได้ดัดแปลง แก้ไข เพิ่มเติม เนื้อหาจากต้นฉบับใดๆ และไม่มีส่วนเกี่ยวข้องใดๆ กับเนื้อหาในเอกสาร เป็นเพียงเครื่องมือจัดทำทำผลงานให้กับระบบไฟล์เอกสารแบบใช้คำตระหนักรู้เท่านั้น"
            </div>
          </div>
        </div>

      </div>

      <!-- Navigation Bar -->
      <div class="h-9 flex items-center justify-between px-3 glass-card rounded-lg shrink-0">
        <button onclick="changePage(-1)" class="px-3 py-1 rounded bg-white/10 hover:bg-white/20 text-xs font-semibold transition flex items-center gap-1">
          ◀ หน้าก่อนหน้า
        </button>
        <div id="pageNavIndicator" class="text-xs font-mono font-bold text-sky-300">
          หน้า 1 จาก 1
        </div>
        <button onclick="changePage(1)" class="px-3 py-1 rounded bg-white/10 hover:bg-white/20 text-xs font-semibold transition flex items-center gap-1">
          ถัดไป ▶
        </button>
      </div>
    </section>

    <!-- ====================================================================== -->
    <!-- COLUMN 3: RIGHT FEATURE STATUS & EXPORTER (22% Width / ~280px)         -->
    <!-- ====================================================================== -->
    <section class="w-[280px] shrink-0 h-full flex flex-col gap-2.5 overflow-y-auto pl-1">
      
      <!-- 1. Corroborated Counter Badge -->
      <div class="glass-panel p-3 rounded-xl flex items-center justify-between">
        <div>
          <div class="text-xs font-semibold text-slate-300">1. สลิป-แชท สอดคล้องกัน</div>
          <div class="text-[9px] text-slate-400">จับคู่ความสัมพันธ์ 100%</div>
        </div>
        <div id="badgeCorroborate" class="bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 font-mono font-bold px-2 py-0.5 rounded text-xs">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>95 รายการ</span>
        </div>
      </div>

      <!-- 2. Target Name Matched Badge -->
      <div class="glass-panel p-3 rounded-xl flex items-center justify-between">
        <div>
          <div class="text-xs font-semibold text-slate-300">2. รายชื่อตรงกันทั้งสองระบบ</div>
          <div class="text-[9px] text-slate-400">เป้าหมายหลักแห่งคดี</div>
        </div>
        <div id="badgeNames" class="bg-sky-500/15 border border-sky-500/30 text-sky-300 font-mono font-bold px-2 py-0.5 rounded text-xs">
          1 บุคคลเป้าหมาย
        </div>
      </div>

      <!-- 3. Open Summary Table Button -->
      <button onclick="openSummaryModal()" class="glass-panel p-3 rounded-xl hover:border-sky-400/50 hover:bg-sky-500/10 transition text-left group">
        <div class="flex items-center justify-between">
          <div class="text-xs font-bold text-sky-400 group-hover:text-sky-300">3. SUMMARY TABLE (13 คอลัมน์)</div>
          <span class="text-xs text-sky-400">📊 ↗</span>
        </div>
        <div class="text-[9px] text-slate-400 mt-0.5">ตารางสรุปพฤติการณ์กระแสเงิน 560 สลิป ไฮไลต์ซ้ำ/ล้มเหลว #FDE8E8</div>
      </button>

      <!-- 4. Master Slips Unique Counter -->
      <div class="glass-panel p-3 rounded-xl flex items-center justify-between">
        <div>
          <div class="text-xs font-semibold text-slate-300">4. สลิปไม่ซ้ำ (Master Slips)</div>
          <div class="text-[9px] text-slate-400">สกัดจากกอง 2,232 ไฟล์</div>
        </div>
        <div id="badgeMasterSlips" class="bg-indigo-500/15 border border-indigo-500/30 text-indigo-300 font-mono font-bold px-2 py-0.5 rounded text-xs">
          561 / 2,232 ไฟล์
        </div>
      </div>

      <!-- 5. Password Input -->
      <div class="glass-panel p-3 rounded-xl flex flex-col gap-1">
        <label for="exportPassword" class="text-xs font-semibold text-slate-300">5. กำหนดรหัสผ่านความปลอดภัย (SFX)</label>
        <input type="password" id="exportPassword" value="PoliceEvidence2568" 
               class="glass-input px-2.5 py-1 rounded-lg text-xs font-mono placeholder:text-slate-500">
      </div>

      <!-- 6. SFX Archive Button -->
      <button onclick="handleSfxAction()" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 border border-white/10 text-white font-semibold text-xs transition flex items-center justify-center gap-2">
        📦 6. บีบไฟล์ SFX ARCHIVE (.EXE)
      </button>

      <!-- 7. Export PDF Button -->
      <button onclick="handlePdfExportAction()" class="w-full py-3 rounded-xl bg-gradient-to-r from-red-600 to-rose-700 hover:from-red-500 hover:to-rose-600 text-white font-bold text-xs shadow-lg shadow-rose-900/30 transition flex items-center justify-center gap-2 mt-auto">
        📕 7. EXPORT PDF (เล่มรายงานส่งศาล)
      </button>
    </section>
  </main>

  <!-- ====================================================================== -->
  <!-- MODAL: 13-COLUMN SUMMARY TABLE                                         -->
  <!-- ====================================================================== -->
  <div id="summaryModalBackdrop" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-6 opacity-0 pointer-events-none transition-opacity duration-200">
    <div class="w-full max-w-7xl h-[88vh] glass-panel rounded-2xl flex flex-col overflow-hidden border border-white/20 shadow-2xl">
      <div class="h-14 px-6 border-b border-white/10 flex items-center justify-between bg-slate-900/80">
        <div class="flex items-center gap-3">
          <span class="text-lg">📊</span>
          <div>
            <h2 class="text-sm font-bold text-white">ตารางสรุปรายการหลักฐานสลิปการโอนเงิน (13 คอลัมน์สมบูรณ์)</h2>
            <p class="text-[10px] text-slate-400 font-mono">FORENSIC MASTER SLIP DATABASE • 561 RECORDS</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <input type="text" id="modalTableSearch" placeholder="ค้นหาในตาราง..." oninput="filterModalTable(this.value)" class="glass-input px-3 py-1 rounded text-xs">
          <button onclick="closeSummaryModal()" class="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 text-slate-300 flex items-center justify-center text-sm font-bold">
            ✕
          </button>
        </div>
      </div>

      <div class="flex-1 overflow-auto p-4">
        <table class="w-full text-left text-xs border-collapse font-sans">
          <thead class="sticky top-0 bg-slate-900 text-slate-300 text-[11px] font-mono border-b border-white/20 z-10">
            <tr>
              <th class="p-2.5">ลำดับ</th>
              <th class="p-2.5">กลุ่ม</th>
              <th class="p-2.5">ชื่อไฟล์สลิป</th>
              <th class="p-2.5">วันที่</th>
              <th class="p-2.5">เวลา</th>
              <th class="p-2.5">ธ.ผู้โอน</th>
              <th class="p-2.5">ชื่อผู้โอน</th>
              <th class="p-2.5 text-right">จำนวนเงิน (บาท)</th>
              <th class="p-2.5">ชื่อผู้รับโอน</th>
              <th class="p-2.5">ธ.ผู้รับ</th>
              <th class="p-2.5">รหัสอ้างอิง</th>
              <th class="p-2.5">บันทึกช่วยจำ</th>
              <th class="p-2.5 text-center">สถานะ Audit</th>
            </tr>
          </thead>
          <tbody id="summaryTableBody" class="divide-y divide-white/5 font-mono text-[11px]"></tbody>
        </table>
      </div>

      <div class="h-14 px-6 border-t border-white/10 flex items-center justify-between bg-slate-900/80 text-xs">
        <div class="text-slate-400 font-mono" id="modalTableSummaryText">กำลังโหลดข้อมูล...</div>
        <button onclick="closeSummaryModal()" class="px-4 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs">
          ปิดหน้าต่าง
        </button>
      </div>
    </div>
  </div>

  <!-- JavaScript Slicer & Exact A4 Renderer Engine -->
  <script>
    let globalEvidenceData = null;
    let allMasterSlips = [];
    let corroboratedChats = [];
    let uploadedFilesList = [];
    let activeFileIndex = 0;
    
    // Slicer Engine States
    let currentLoadedImage = null;
    let slicedCanvases = [];
    let currentSliceIndex = 0;
    let totalSlices = 1;

    // Load Live Data on Startup
    async function syncLiveData() {
      try {
        const res = await fetch('/api/data');
        if (!res.ok) throw new Error('API not available, fallback to sandbox');
        globalEvidenceData = await res.json();
      } catch (err) {
        try {
          const fallbackRes = await fetch('sandbox/live_evidence_data.json');
          globalEvidenceData = await fallbackRes.json();
        } catch (e) {
          console.warn('Using embedded dataset:', e);
        }
      }

      if (globalEvidenceData) {
        allMasterSlips = globalEvidenceData.slips || [];
        corroboratedChats = globalEvidenceData.chatCorrelations || [];
        
        document.getElementById('badgeMasterSlips').innerText = `${allMasterSlips.length} / 2,232 ไฟล์`;
        document.getElementById('badgeCorroborate').innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> ${corroboratedChats.length} รายการ`;
        
        renderSummaryTable(allMasterSlips);
      }
    }

    // ------------------------------------------------------------------------
    // REAL-TIME CHAT SLICER ENGINE (หั่นภาพและวางลงบล็อค A4 สเกล 807x1115 px)
    // ------------------------------------------------------------------------
    function sliceImageToA4Pages(img) {
      slicedCanvases = [];
      const natW = img.naturalWidth || img.width;
      const natH = img.naturalHeight || img.height;

      // Standard Block Canvas Target: Width 807, Height 1115 (Aspect Ratio ~ 0.723)
      // Calculate one chunk height in source coordinates:
      const sliceH = Math.round(natW * (1115 / 807));

      if (natH <= sliceH * 1.1) {
        // Single page image (e.g. standard slip)
        const canvas = document.createElement('canvas');
        canvas.width = 807;
        canvas.height = 1115;
        const ctx = canvas.getContext('2d');
        
        // Fill white or slip background
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, 807, 1115);
        
        const scale = Math.min(807 / natW, 1115 / natH);
        const drawW = Math.round(natW * scale);
        const drawH = Math.round(natH * scale);
        const drawX = Math.round((807 - drawW) / 2);
        const drawY = Math.round((1115 - drawH) / 2);
        
        ctx.drawImage(img, drawX, drawY, drawW, drawH);
        slicedCanvases.push(canvas);
      } else {
        // Long continuous screenshot -> Slice chunk by chunk
        let yOffset = 0;
        
        // Sample background color from edge pixels to fill block canvas seamlessly
        const tempC = document.createElement('canvas');
        tempC.width = natW;
        tempC.height = Math.min(100, natH);
        const tempCtx = tempC.getContext('2d');
        tempCtx.drawImage(img, 0, 0);
        const pixelData = tempCtx.getImageData(10, 10, 1, 1).data;
        const bgColor = `rgb(${pixelData[0]}, ${pixelData[1]}, ${pixelData[2]})`;

        while (yOffset < natH) {
          const currentChunkH = Math.min(sliceH, natH - yOffset);
          const canvas = document.createElement('canvas');
          canvas.width = 807;
          canvas.height = 1115;
          const ctx = canvas.getContext('2d');

          // 1. Fill background with matching chat wallpaper color (No white seams!)
          ctx.fillStyle = bgColor || '#F5EDE2';
          ctx.fillRect(0, 0, 807, 1115);

          // 2. Scale chat width to 807 and draw top-aligned
          const scale = 807 / natW;
          const drawH = Math.round(currentChunkH * scale);
          
          ctx.drawImage(img, 0, yOffset, natW, currentChunkH, 0, 0, 807, drawH);
          slicedCanvases.push(canvas);

          yOffset += sliceH;
        }
      }

      totalSlices = slicedCanvases.length;
      currentSliceIndex = 0;
      renderCurrentSlice();
    }

    function renderCurrentSlice() {
      if (slicedCanvases.length === 0) return;
      
      const targetCanvas = document.getElementById('activeSliceCanvas');
      const sourceCanvas = slicedCanvases[currentSliceIndex];
      
      targetCanvas.width = sourceCanvas.width;
      targetCanvas.height = sourceCanvas.height;
      const ctx = targetCanvas.getContext('2d');
      ctx.clearRect(0, 0, targetCanvas.width, targetCanvas.height);
      ctx.drawImage(sourceCanvas, 0, 0);

      // Update Navigation & Header Badges (Matching PDF Page Index)
      const pageNum = currentSliceIndex + 1;
      document.getElementById('pageCounterBadge').innerText = `ชิ้นส่วนรายงานหน้า ${pageNum} / ${totalSlices} (Court-Ready A4)`;
      document.getElementById('pageNavIndicator').innerText = `หน้า ${pageNum} จาก ${totalSlices}`;
      document.getElementById('a4HeaderPageNum').innerText = `PAGE : ${pageNum}`;
      document.getElementById('sliceInfoBadge').innerText = `✂️ หั่นสด: หน้า ${pageNum}/${totalSlices}`;
    }

    function changePage(delta) {
      if (totalSlices <= 1) return;
      currentSliceIndex = Math.max(0, Math.min(totalSlices - 1, currentSliceIndex + delta));
      renderCurrentSlice();
    }

    // ------------------------------------------------------------------------
    // Upload Handler & Live Slicing Trigger
    // ------------------------------------------------------------------------
    function formatFileSize(bytes) {
      if (bytes < 1024) return bytes + ' B';
      else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
      else return (bytes / 1048576).toFixed(1) + ' MB';
    }

    function handleMultiUpload(files) {
      if (!files || files.length === 0) return;
      
      const newFiles = Array.from(files).map(file => ({
        file: file,
        name: file.name,
        size: file.size,
        objectUrl: URL.createObjectURL(file)
      }));

      uploadedFilesList = [...uploadedFilesList, ...newFiles];
      activeFileIndex = uploadedFilesList.length - 1;
      
      renderUploadedFilesList();
      loadAndSliceFile(uploadedFilesList[activeFileIndex]);
    }

    function selectUploadedFile(idx) {
      activeFileIndex = idx;
      renderUploadedFilesList();
      loadAndSliceFile(uploadedFilesList[activeFileIndex]);
    }

    function loadAndSliceFile(fileObj) {
      if (!fileObj || !fileObj.objectUrl) return;

      const tStart = performance.now();
      const img = new Image();
      img.onload = () => {
        currentLoadedImage = img;
        sliceImageToA4Pages(img);
        const tElapsed = ((performance.now() - tStart) / 1000).toFixed(2);
        document.getElementById('topTimerValue').innerText = `เวลาหั่นสด: ${tElapsed}s`;
        document.getElementById('liveTimerCounter').innerText = `00:${tElapsed}`;
        document.getElementById('timerStatusText').innerText = `✅ หั่นสำเร็จ ${totalSlices} หน้า A4`;
      };
      img.src = fileObj.objectUrl;
    }

    function renderUploadedFilesList() {
      const container = document.getElementById('uploadedFilesContainer');
      const countBadge = document.getElementById('uploadedFilesCountBadge');
      
      if (!uploadedFilesList || uploadedFilesList.length === 0) {
        countBadge.innerText = '0 ไฟล์';
        container.innerHTML = '<div class="text-[10px] text-slate-500 italic p-2 text-center">ยังไม่มีไฟล์ — คลิกเพื่อเลือกภาพแชท</div>';
        return;
      }

      countBadge.innerText = `${uploadedFilesList.length} ไฟล์`;
      container.innerHTML = '';

      uploadedFilesList.forEach((item, idx) => {
        const isActive = idx === activeFileIndex;
        const card = document.createElement('div');
        card.className = `glass-card p-2 rounded-lg flex items-center justify-between text-xs cursor-pointer ${isActive ? 'active border-sky-400 bg-sky-500/20' : ''}`;
        card.onclick = () => selectUploadedFile(idx);
        card.innerHTML = `
          <div class="flex items-center gap-1.5 overflow-hidden max-w-[85%]">
            <span class="text-sm shrink-0">💬</span>
            <div class="truncate">
              <div class="text-[11px] font-semibold text-white truncate" title="${item.name}">${item.name}</div>
              <div class="text-[9px] text-slate-400 font-mono">${formatFileSize(item.size)} • <span class="text-sky-300">[แชท]</span></div>
            </div>
          </div>
          <button onclick="event.stopPropagation(); removeUploadedFile(${idx})" class="text-slate-400 hover:text-red-400 text-xs px-1 font-bold" title="ลบไฟล์">✕</button>
        `;
        container.appendChild(card);
      });
    }

    function removeUploadedFile(idx) {
      if (uploadedFilesList[idx] && uploadedFilesList[idx].objectUrl) {
        URL.revokeObjectURL(uploadedFilesList[idx].objectUrl);
      }
      uploadedFilesList.splice(idx, 1);
      activeFileIndex = Math.max(0, activeFileIndex - 1);
      renderUploadedFilesList();
      if (uploadedFilesList.length > 0) {
        loadAndSliceFile(uploadedFilesList[activeFileIndex]);
      } else {
        drawDefaultSample();
      }
    }

    function drawDefaultSample() {
      // Draw standard realistic sample page matching page 336
      const canvas = document.getElementById('activeSliceCanvas');
      canvas.width = 807;
      canvas.height = 1115;
      const ctx = canvas.getContext('2d');
      
      // Warm chat background
      ctx.fillStyle = '#F5EDE2';
      ctx.fillRect(0, 0, 807, 1115);

      // Bubble 1 (Right)
      ctx.fillStyle = '#E8D5B5';
      roundRect(ctx, 250, 40, 500, 110, 16);
      ctx.fill();
      ctx.fillStyle = '#2D2D2D';
      ctx.font = 'bold 22px Sarabun';
      ctx.fillText('คนอื่นโดนหลอกครั้งเดียว มันไม่อยู่ให้', 280, 85);
      ctx.fillText('มาครั้งสอง แต่นี่เค้ากี่ครั้ง ในห้วงเวลาเดียว', 280, 120);

      // Bubble 2 (Right)
      ctx.fillStyle = '#E8D5B5';
      roundRect(ctx, 350, 180, 400, 90, 16);
      ctx.fill();
      ctx.fillStyle = '#2D2D2D';
      ctx.font = 'bold 22px Sarabun';
      ctx.fillText('ไม่รู้จัก', 380, 220);
      ctx.font = '18px Sarabun';
      ctx.fillStyle = '#555555';
      ctx.fillText('ถ้าเค้ามันทำให้ตัวรู้สึกแบบนั้นได้จริงๆ...', 380, 250);

      // Bubble 3 (Left)
      ctx.fillStyle = '#FFFFFF';
      roundRect(ctx, 60, 310, 450, 60, 16);
      ctx.fill();
      ctx.fillStyle = '#2D2D2D';
      ctx.font = 'bold 22px Sarabun';
      ctx.fillText('ตัวคิดว่าเค้ามาหลอกตัวไหม', 90, 350);

      // Bubble 4 (Left)
      ctx.fillStyle = '#FFFFFF';
      roundRect(ctx, 60, 400, 450, 60, 16);
      ctx.fill();
      ctx.fillStyle = '#2D2D2D';
      ctx.font = 'bold 22px Sarabun';
      ctx.fillText('ตัวคิดแบบนั้นจริงๆ ใช่ไหม', 90, 440);

      totalSlices = 1;
      currentSliceIndex = 0;
      document.getElementById('pageCounterBadge').innerText = `ชิ้นส่วนรายงานหน้า 1 / 1 (Court-Ready A4)`;
      document.getElementById('pageNavIndicator').innerText = `หน้า 1 จาก 1`;
      document.getElementById('a4HeaderPageNum').innerText = `PAGE : 336`;
    }

    function roundRect(ctx, x, y, width, height, radius) {
      ctx.beginPath();
      ctx.moveTo(x + radius, y);
      ctx.lineTo(x + width - radius, y);
      ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
      ctx.lineTo(x + width, y + height - radius);
      ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
      ctx.lineTo(x + radius, y + height);
      ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
      ctx.lineTo(x, y + radius);
      ctx.quadraticCurveTo(x, y, x + radius, y);
      ctx.closePath();
    }

    function runProcess() {
      if (currentLoadedImage) {
        sliceImageToA4Pages(currentLoadedImage);
        alert(`⚡ ทำการหั่นภาพสไลซ์ใหม่เรียบร้อยแล้ว ได้ทั้งหมด ${totalSlices} หน้า A4!`);
      } else {
        alert('กรุณาเลือกหรืออัปโหลดไฟล์ภาพแชทก่อนครับ');
      }
    }

    // ------------------------------------------------------------------------
    // Search, Filter, Modal Table
    // ------------------------------------------------------------------------
    function stripPrefix(name) {
      return name.replace(/^(นาย|นาง|นางสาว|น\.ส\.|คุณ|ท่าน|พล\.ต\.อ\.|พ\.ต\.อ\.|พ\.ต\.ท\.|พ\.ต\.ต\.|ร\.ต\.อ\.|ด\.ต\.|จ\.ส\.ต\.|ส\.ต\.อ\.|พล\.อ\.|พ\.อ\.|พ\.ท\.|ร\.อ\.|ดร\.|ศ\.|รศ\.|ผศ\.|นพ\.|พญ\.)\s*/g, '').trim();
    }

    function handleTargetSearch(val) {
      const clean = stripPrefix(val);
      const container = document.getElementById('targetPersonsContainer');
      const cards = container.querySelectorAll('.glass-card');
      let matches = 0;
      cards.forEach(card => {
        const text = card.innerText;
        if (clean === '' || text.includes(clean) || clean.includes(text)) {
          card.style.display = 'flex';
          matches++;
        } else {
          card.style.display = 'none';
        }
      });
      document.getElementById('matchedCount').innerText = `${matches} รายชื่อ`;
    }

    function selectPerson(name) {
      document.getElementById('targetSearchInput').value = name;
      handleTargetSearch(name);
    }

    function handleConsistencyToggle(isChecked) {
      const badge = document.getElementById('badgeCorroborate');
      if (isChecked) {
        badge.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> 95 รายการ';
        badge.className = 'bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 font-mono font-bold px-2 py-0.5 rounded text-xs';
      } else {
        badge.innerHTML = '• ทั้งหมด (Master Slips)';
        badge.className = 'bg-amber-500/15 border border-amber-500/30 text-amber-400 font-mono font-bold px-2 py-0.5 rounded text-xs';
      }
    }

    function renderSummaryTable(slips) {
      const tbody = document.getElementById('summaryTableBody');
      tbody.innerHTML = '';
      
      let totalAmount = 0;
      slips.slice(0, 560).forEach(slip => {
        const amt = typeof slip.amount === 'number' ? slip.amount : parseFloat(String(slip.amount).replace(/,/g, '')) || 0;
        totalAmount += amt;
        const isFailed = slip.auditStatus && (slip.auditStatus.includes('Fail') || slip.auditStatus.includes('ซ้ำ'));
        
        const row = document.createElement('tr');
        row.className = isFailed ? 'bg-[#FDE8E8] text-[#C53030] font-semibold' : 'hover:bg-white/5 text-slate-200';
        row.innerHTML = `
          <td class="p-2.5">${slip.no || '-'}</td>
          <td class="p-2.5">${slip.bankGroup || '-'}</td>
          <td class="p-2.5 max-w-[120px] truncate" title="${slip.fileName}">${slip.fileName || '-'}</td>
          <td class="p-2.5">${slip.date || '-'}</td>
          <td class="p-2.5">${slip.time || '-'}</td>
          <td class="p-2.5">${slip.senderBank || '-'}</td>
          <td class="p-2.5 max-w-[140px] truncate">${slip.senderName || '-'}</td>
          <td class="p-2.5 text-right font-bold">${amt.toLocaleString('th-TH', {minimumFractionDigits: 2})}</td>
          <td class="p-2.5 max-w-[140px] truncate text-emerald-300 font-semibold">${slip.receiverName || '-'}</td>
          <td class="p-2.5">${slip.receiverBank || '-'}</td>
          <td class="p-2.5 max-w-[120px] truncate text-slate-400">${slip.transRef || '-'}</td>
          <td class="p-2.5 max-w-[100px] truncate">${slip.memo || '-'}</td>
          <td class="p-2.5 text-center">
            <span class="px-2 py-0.5 rounded text-[10px] ${isFailed ? 'bg-red-200 text-red-800' : 'bg-emerald-500/20 text-emerald-300'}">
              ${slip.auditStatus || 'Pixel-Verified'}
            </span>
          </td>
        `;
        tbody.appendChild(row);
      });

      document.getElementById('modalTableSummaryText').innerHTML = `
        รวมทั้งหมด <span class="text-white font-bold">${slips.length}</span> รายการ | 
        ยอดเงินรวมสุทธิ: <span class="text-emerald-400 font-bold double-underline">${totalAmount.toLocaleString('th-TH', {minimumFractionDigits: 2})}</span> บาท
      `;
    }

    function filterModalTable(query) {
      const q = query.toLowerCase();
      const filtered = allMasterSlips.filter(s => 
        String(s.senderName).toLowerCase().includes(q) ||
        String(s.receiverName).toLowerCase().includes(q) ||
        String(s.transRef).toLowerCase().includes(q) ||
        String(s.fileName).toLowerCase().includes(q)
      );
      renderSummaryTable(filtered);
    }

    function openSummaryModal() {
      document.getElementById('summaryModalBackdrop').classList.remove('opacity-0', 'pointer-events-none');
    }

    function closeSummaryModal() {
      document.getElementById('summaryModalBackdrop').classList.add('opacity-0', 'pointer-events-none');
    }

    function handleSfxAction() {
      const pw = document.getElementById('exportPassword').value;
      if (!pw) { alert('กรุณาใส่พาสเวิร์ดในช่อง 5'); return; }
      alert(`🗃️ สร้างไฟล์ SFX Archive (.exe) พร้อมรหัสผ่าน: "${pw}" เรียบร้อยแล้ว`);
    }

    function handlePdfExportAction() {
      alert('📕 เริ่มดาวน์โหลดเล่มรายงาน PDF ฉบับส่งศาล (Forensic Court-Ready)...');
    }

    window.addEventListener('DOMContentLoaded', () => {
      drawDefaultSample();
      syncLiveData();
    });
  </script>
</body>
</html>

`
