<!-- ============================================================================== -->
<!-- 🔄 SYSTEM DATA FLOW ARCHITECTURE & BUSINESS CONSTRAINTS                      -->
<!-- 👤 ROLE: SENIOR FULL-STACK DEVELOPER AGENT                                     -->
<!-- 📦 PROJECT: DIGITAL_EVIDENCE                                                   -->
<!-- 🌐 LANGUAGE: 🇺🇸 100% ENGLISH SPECIFICATION (OPTIMIZED FOR AI CONTEXT WINDOW)  -->
<!-- 📅 UPDATED: 2026-09-14T12:46:45+07:00                                          -->
<!-- ============================================================================== -->

# 🔄 SYSTEM DATA FLOW & INTERACTION ARCHITECTURE — DIGITAL_EVIDENCE

> **Operational Purpose:** This specification provides an exhaustive, end-to-end technical blueprint of the execution flow, system interaction nodes, and programmatic constraints governing the `DIGITAL_EVIDENCE` suite. Designed specifically to grant subsequent coding agents deterministic context inheritance under the strict constitutional Honesty Rule (Zero-Guessing / Zero-Hallucination), Universal 18-Bank Coverage, and Forensic Duplicate Slip Auditing.

---

## 🧭 1. ⚙️ Step-by-Step Data Pipeline

```
 [STAGE 1: Multi-Channel Ingestion & Polling]
       │
       ▼
 [STAGE 2: Prefix Parsing & Natural Numeric Sorting (List_names)]
       │
       ▼
 [STAGE 3: Image Sanitization & Mobile Edge Band Removal]
       │
       ▼
 [STAGE 4: Quiet Zone Lookahead Slicing (Dicut_Chat)]
       │
       ▼
 [STAGE 5: Slip-Block-Fit Dynamic Background Canvas Standardization]
       │
       ▼
 [STAGE 6: Forensic Quality Gate & PDF Assembly]
       │
       ├──► [STAGE 7A: Post-PDF Slip Detection & Page Indexing (Search_Slip)]
       │
       └──► [STAGE 7B: Universal 18-Bank Slip Engine with Forensic Auditor (OCR_Slip)]
                  ├── Pre-processing: Morphological Background Subtraction + CLAHE
                  ├── QR Cryptographic Parser: EMVCo Tag 02 (Ref ID) + Tag 00/01 (3-Digit BOT Bank Code)
                  ├── Text Engine: Local Tesseract (tha+eng) Multi-Pass OCR
                  ├── Normalization: Thai Ligature Whitespace Stripping
                  ├── SSOT Master Dictionary: 18 Thai Financial Institutions
                  ├── Metadata Enrichment: Bank Branch (สาขา) Extraction into Memo
                  ├── Forensic Audit: In-Batch & Cross-Batch Duplicate Slip Detection
                  ├── Grid Engine & Typography: Sarabun Font + 100% Center-Aligned Cells + 4-Sided Thin Borders
                  ├── Print Layout: A4 Landscape (1406x993 px) + Centered 3-Line Legal Disclaimer
                  └── Legal Ledger: 13-Column Excel (Warning Cell Highlighting) + JSON
```

---

## 🗺️ 2. 🌐 System Interaction Map (Mermaid Architecture)

```mermaid
graph TD
    subgraph INGESTION ["📥 1. Ingestion Layer"]
        InChat["EVIDENCE_CHAT_IN/"]
        InSlip["EVIDENCE_IN/"]
        ExtFolder["External Repositories (e.g. F:/Project/EDOK/)"]
    end

    subgraph CHAT_ENGINE ["📱 2. Chat Processing Pipeline (List_names + Dicut_Chat)"]
        Sort["Natural Sort & Prefix Extraction"]
        CleanBand["Strip Dark Navigation Bands"]
        QuietCut["Smart Quiet Zone Detector (1.30x Lookahead)"]
        BlockFit["Slip-Block-Fit (807x1115 / 645x890 Canvas)"]
        Audit["Auto-Audit Quality Gate (100% Pass)"]
        PDFGen["PDF Synthesis: Evidence_Chat_{prefix}.pdf"]
    end

    subgraph SLIP_SEARCH ["🔍 3. Post-PDF Page Indexing (Search_Slip)"]
        PageRender["Render PDF Page to OpenCV BGR"]
        BadgeScan["HSV Green Success Badge Detection"]
        TextScan["Tesseract OCR Transaction Data Extractor"]
        SlipIndex["Export: Slip_Index.xlsx & Slip_Index.json"]
    end

    subgraph SLIP_OCR ["💳 4. Universal 18-Bank Slip Engine (OCR_Slip)"]
        MorphFilter["Morphological Background Subtraction (gray / bg * 255)"]
        CLAHE["CLAHE Contrast Enhancement"]
        EMVCoRef["EMVCo Tag 02 Ref ID Parser"]
        BOTBankCode["EMVCo Tag 00/01: 3-Digit BOT Bank Code"]
        LocalOCR["Local Tesseract Multi-Pass OCR (tha+eng)"]
        SpaceStrip["Thai Whitespace Stripping & Normalization"]
        Dict18["Master Dictionary: 18 Thai Banks"]
        BranchExt["Bank Branch (สาขา) Extraction -> Memo"]
        PIIGuard["PII Guard: Mask Thai ID 13d, Tel 10d, CC 16d (--mask-pii)"]
        Fingerprint["Text Fingerprint Hashing (SHA-256 slice)"]
        AccountCheck["Bank Account Pattern Validation (10-12 digits)"]
        DupAuditor["Forensic Duplicate Slip Auditor (In-batch + Printed Log)"]
        HotWatcher["Hot Folder Watcher Daemon (slip_hotfolder_watcher.py)"]
        BatchLauncher["One-Click Launcher (RUN_SLIP_EXTRACTOR.bat Drag & Drop)"]
        StartupService["Windows Startup Hook (install_startup.bat)"]
        Ledger13["Export: 13-Column Legal Ledger (Excel & JSON)"]
    end

    subgraph ARCHIVE ["🏛️ 5. Preservation & Constitutional Governance"]
        BatchArch["processed/Case_{ID}/Batch_{TS}/"]
        Memory["memory/behavior.json + memory/mistakes.md"]
        PrintedLog["memory/printed_slips.log"]
        StateBackup["state/ Redundant Backup Mirror"]
        Constitution["AGENTS.md (Strict Zero-Guessing Rule)"]
    end

    InChat --> Sort --> CleanBand --> QuietCut --> BoxFit --> Audit --> PDFGen
    PDFGen --> PageRender --> BadgeScan --> TextScan --> SlipIndex
    InSlip --> MorphFilter
    ExtFolder --> MorphFilter
    MorphFilter --> CLAHE --> LocalOCR
    MorphFilter --> EMVCoRef
    MorphFilter --> BOTBankCode
    LocalOCR --> SpaceStrip --> Dict18
    LocalOCR --> BranchExt
    BranchExt --> DupAuditor
    EMVCoRef --> DupAuditor
    BOTBankCode --> DupAuditor
    PrintedLog --> DupAuditor
    DupAuditor --> Ledger13
    PDFGen --> BatchArch
    Ledger13 --> Memory
    Memory --> StateBackup
    Constitution -.-> Dict18
```

---

## 🔒 3. ⚖️ Business Logic Constraints & Forensic Audit Specifications

### 3.1 Forensic Duplicate Slip & Printed Log Auditing
- **In-Batch Duplicate Detection:** Identifies repeated Transaction Reference IDs or identical filename stems within the same run. Marks repeated entries as `⚠️ สลิปซ้ำ (Ref ซ้ำกับ ลำดับ X)` and points to the original occurrence.
- **Cross-Batch Historical Verification:** Compares Ref IDs and filenames against `memory/printed_slips.log` (or external `printed_slips.txt`). Flags previously processed slips as `⚠️ เคยพิมพ์แล้ว (Printed)`.
- **Visual Evidence Warning:** In the Excel ledger, duplicate rows are styled with an amber background (`#FFF2CC`) and bold red font (`#C00000`) in Column 13 (`สถานะการตรวจสอบ`).

### 3.2 Bank Branch Extraction into Memo
- Scans OCR text for counter slip or ATM identifiers matching `(?:สาขา|Branch)[\s:]*([^\n\r,]+)`.
- Enriches the transaction `memo` field with `สาขา: [Branch Name]` without overwriting user-specified notes.

### 3.3 3-Digit BOT Financial Institution Code Standard
- In compliance with the Bank of Thailand (BOT) National QR Code Standard, embeds a 3-digit institutional code within `Tag 00 -> Sub-tag 01` of the EMVCo payload:
  - `002`: BBL, `004`/`005`: KBANK, `006`: KTB, `011`: TTB, `014`: SCB, `025`: BAY, `030`: GSB, `034`: BAAC, `066`/`069`: KKP, `024`: UOB, `022`: CIMB, `073`: LHBANK, etc.

### 3.4 Strict Zero-Guessing Rule (Constitutional Mandate)
- **Zero Tolerance for Hallucination:** Agents are strictly forbidden from guessing, inferring, or fabricating bank names, counterparty names, account numbers, or financial amounts.
- Distorted OCR tokens (e.g. `Alovdsuma`) MUST NOT be guessed phonetically. They MUST bind to proven ground-truth bank accounts (e.g. `996-5` binds strictly to TTB).

### 3.5 Standard Legal Grid & Typography Protocol (Chat Evidence Blueprint)
- **Strict Center Alignment:** Every data, numerical, and status cell MUST be center-aligned across both horizontal and vertical axes (`Alignment(horizontal='center', vertical='center', wrap_text=True)`). Left or right bias is explicitly prohibited.
- **Official Typography:** The table strictly employs the `Sarabun` font family (`Sarabun` 16pt bold for Title, 12pt bold for Headers, 11pt regular for Data cells, 9pt for Disclaimer).
- **Full Perimeter Borders:** Every active cell is bounded by 4-sided crisp thin borders (`Border(left=thin, right=thin, top=thin, bottom=thin)`).
- **A4 Landscape Dimensions:** Formatted for A4 Landscape printing ($1406 \times 993$ px, `orientation=landscape`, `paperSize=9`), with margins (Top 157px, Bottom 179px, Left/Right 102px).
- **Centered Disclaimer Footer:** A 3-line legal disclaimer is merged and centered at the bottom of the ledger:
  `"DIGITAL EVIDENCE เป็นเพียงการเครื่องมืออำนวยความสะดวกให้กับผู้ว่าจ้าง โดยไม่ได้ดัดแปลง แก้ไข เพิ่ม-ลบ เนื้อหา\nจากต้นฉบับใดๆ และไม่มีส่วนเกี่ยวข้องใดๆกับเนื้อหาในเอกสาร เป็นเพียงเครื่องมือที่ทำงานเกี่ยวกับระบบไฟล์\nเอกสารแบบอิเล็กทรอนิกส์ เท่านั้น"`

---

## 🛡️ 4. 🚨 Failure Recovery & Exception Handling Protocols

| Failure Mode | Trigger Condition | Deterministic Recovery Strategy |
| :--- | :--- | :--- |
| **QR Code Unreadable** | Glare, compression artifacts, or partial crop | Fall back immediately to Multi-Pass OCR regex pattern matching (`202\d{15,19}`, `A[A-Za-z0-9]{14,21}`, `N\d{20,26}`) |
| **Thai Spacing Desync** | Tesseract inserts spaces between glyphs | Execute `t_clean = text.replace(' ', '').lower()` before regex evaluation |
| **Duplicate Detected** | Ref ID or filename matched in batch or historical log | Annotate in Column 13 with sequence reference, apply visual amber fill, and preserve both records for forensic comparison |
| **Unrecognized Bank** | Distorted OCR font not matching string patterns | Apply SSOT Account Mapping: Bind target recipient account numbers to bank entities |

<!-- ============================================================================== -->
<!-- 🏁 END OF PROJECT_FLOW.md                                                     -->
<!-- ============================================================================== -->
