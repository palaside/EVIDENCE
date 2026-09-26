# 06 · UI SPECIFICATION (Rev02 + Glassmorphism + PDF Supplement)
# โครงการ DIGITAL_EVIDENCE

> ตำแหน่ง: `Docs/TH/06-UI-SPECIFICATION.md` (สร้างใหม่ ห้ามแก้ต้นฉบับ)
> ต้นฉบับอ้างอิง (อ่านอย่างเดียว):
> - `D:\Project\DIGITAL_EVIDENCE\UI Specification.md:1-753` (Rev02, 19,007B)
> - `C:\Users\EVE\OneDrive\เดสก์ท็อป\Glassmorphism Visual Contract.md:1-227` (Factory V3, ทุกคอมโพเนนต์, anchor=live)
> - `D:\Project\DIGITAL_EVIDENCE\PROJECT_EVIDENCE_3COL_PROTOTYPE.html` (56,769B)

## 1. บทบาทเอกสารและขอบเขต (ห้าม Drift)

- StackBlitz ทำเฉพาะ UI (HTML/CSS/JS): Layout, Theme, Responsive, Interaction
- Python Pipeline เดิมเป็นเจ้าของ: ประมวลผลแชท/สลิป, สร้าง PDF, Quality Gate, OUTPUT (`Folder_Out`, `Portable/OUTPUT`)
- Dashboard เป็น Local Read-only ในเฟสนี้ (`Docs/TH/03-ARCHITECTURE.md`): ไม่มี HTTP API ภายนอก ห้ามสมมติว่าเว็บ StackBlitz สั่ง Python หรืออ่าน `Folder_Out` บน Windows ได้ตรง
- ไฟล์ต้นฉบับทั้ง 2 ฉบับคงไว้ ไม่คัดลอกทับ ไม่ดัดแปลง

## 2. UI Spec Rev02 — ข้อบังคับ (REQ-01..06)

- REQ-01 Reference Fidelity: ยึดภาพ Dashboard ล่าสุดเป็นต้นแบบ Layout/Header/Panel/Spacing/Typography
- REQ-02 Black & Gray: พื้น `#080A0D`, Panel `#111418`, Surface `#1B2026`, Elevated `#252B32`, Primary Gray `#747D87`, Hover `#929AA3`, Border `#343B44`, Text `#F3F4F6`; ฟ้าที่เคยเป็น Accent → เทาทั้งหมด (Active Tab/Button/Border/Focus/Progress/Selected); เขียว `#16A34A` ส้ม `#F59E0B` แดง `#DC2626` ใช้เฉพาะสถานะจริง + ต้องมีข้อความ/สัญลักษณ์ประกอบ ห้ามใช้สีอย่างเดียว
- REQ-03 Responsive: Desktop ≥1440 (3 คอลัมน์ 28/44/28 ของพื้นที่เนื้อหาหลังหัก gap 12px) / Laptop 1024–1439 (ยืด PDF Review ให้อ่านชัด) / Tablet 768–1023 (PDF บน, Controls+Summary ล่าง) / Mobile <768 (คอลัมน์เดียว + Navigation สลับส่วน); ห้ามล็อกความกว้าง PDF Viewer จนล้นจอ; ตารางใหญ่ scroll-x ใน panel; ปุ่มสำคัญกดได้ไม่ต้องซูม; PDF รักษาอัตราส่วนกระดาษ
- REQ-04 Actual PDF Review: แสดง PDF จริงเท่านั้น ห้ามใช้ภาพ A4 จำลอง; ฟีเจอร์ PDF-01..09 (Open/Navigate/Zoom/Fit-width/Fullscreen/Printต้นฉบับ/Download/Page-Link/Loading-Error)
- REQ-05 Brand: ใช้โลโก้ DIGITAL EVIDENCE ต้นฉบับ ห้ามวาดใหม่; กฎสีเทาไม่ลามเข้าโลโก้และเนื้อใน PDF (PDF แสดงสีตามไฟล์จริง)
- REQ-06 Compatibility: ห้ามเปลี่ยน Pipeline/OCR/Gate/Data Model โดยไม่ได้รับอนุญาต
- Typography: ไทย+อังกฤษ Sarabun, ตัวเลข/RefID JetBrains Mono; Title 20–24 / Panel 15–17 / Body 13–14 / Secondary 12–13; Radius Panel 10–12 / Input-Button 6–8; Padding 16; Gap 12
- Header: โลโก้ + ชื่อไทย/อังกฤษ + CHAT/SLIP + สถานะระบบ (อ่านค่าจริง ห้ามโชว์ ONLINE ค้าง) + Timer + SYNC + สรุปทั้งหมด
- Left (Controls): Upload/Drag-Drop + Queue (ชื่อ/ขนาด/สถานะ/ลบก่อนประมวลผล) / Search-Target / Corroboration Switch (ห้ามใช้สถานะ Switch เป็นหลักฐานว่าสอดคล้องจริง) / Processing (ปุ่ม+Progress+เวลา+จำนวน+error/recheck)
- Center (PDF Review): โฟลว์ เลือก PDF → โหลดด้วย Viewer → อ่านจำนวนหน้าจริง → ตรวจทาน → เปิดต้นฉบับพิมพ์/ดาวน์โหลด
- Right (Summary): KPI (หลักฐาน/สลิป-แชทสอดคล้อง/รายชื่อ/แถวสรุป) / Evidence Table (คอลัมน์ตาม export จริง + ค้น/กรอง + audit/ซ้ำ) / Master Slips (ต้นฉบับ/ซ้ำ + ดูรายการ + โยงหลักฐาน) / Document Actions (เปิดตรวจ + Gate + พิมพ์/โหลดต้นฉบับ); ช่องรหัสผ่าน + SFX ในภาพต้นแบบให้คงตำแหน่ง UI ไว้ก่อน แต่ยังไม่ต่อสร้างไฟล์จริง (นอกขอบเขต PRD)

## 3. PDF Supplement (ส่วนเสริมวันนี้ — สร้างไฟล์ PDF ได้)

- การสร้างเนื้อหา/จัดหน้า/รับรอง PDF ยังเป็นของ Pipeline เดิม (PyMuPDF C-Binding) ไม่ใช่ของ Viewer
- Viewer ทำได้แค่: เปิด/นำทาง/ซูม/fit/fullscreen/เปิดต้นฉบับเพื่อพิมพ์/ดาวน์โหลด/กระโดดตาม Page-Link จากสารบัญ
- ห้ามใช้ `html2canvas` หรือจับภาพ Dashboard มาทำไฟล์พิมพ์ — ไฟล์พิมพ์ต้องเป็น PDF ต้นฉบับเดียวกับที่ใช้ตรวจทาน (`UI Specification.md` §6.2)
- Dashboard Data Layer อ่านจาก OUTPUT (`*.pdf|*.xlsx|*.json` + Hash Cert/Manifest) เท่านั้น
- SFX/Password: ยังไม่สั่งเชื่อม (คง UI placeholder ตาม §7 หมายเหตุ)

## 4. Glassmorphism Visual Contract — การปรับใช้กับธีมดำ (แก้ Conflict)

**Conflict ที่พบ:** Factory V3 ให้ ambient `#7dd3fc/#c084fc` บน base `#0f172a` ซึ่งขัด REQ-02 (ดำ `#080A0D` + เทา, ห้ามฟ้าเป็น Accent)

**คำตัดสิน (ยึด REQ-02 เหนือ Factory default):**
- Ambient Background: ใช้ gradient ดำ-เทาเข้ม (`#080A0D → #111418 → #1B2026`) เท่านั้น ห้ามใช้ฟ้า/ม่วงสว่างเป็นพื้น (blur ต้องเห็นผลบนพื้นดำ)
- Glass Surface: อนุญาต `rgba(255,255,255,0.18)` + `blur(26px) saturate(170%)` + border `rgba(255,255,255,0.32)` + radius 28px + highlight `inset 0 1px 0 rgba(255,255,255,0.38)` + shadow `0 15px 44px rgba(0,0,0,0.24)` เฉพาะการ์ด overlay (Controls/Summary/Header) บนพื้นดำ
- Text: แยก opacity — surface โปร่งแต่ตัวอักษรต้อง `#F3F4F6` อ่านชัด ห้าม `opacity` ทั้งก้อน (ใช้ rgba แยกชั้นตาม Component Rules ข้อ 6–7)
- Shape Mode `ทุกคอมโพเนนต์`: ไม่ล็อก Width/Height ใน `.glass-card` ปล่อยให้ grid context (28/44/28 + breakpoints) กำหนด; fluid panels ใช้ `minmax()/clamp()/fr`
- Fit-to-Screen Shell: `html,body{height:100%;overflow:hidden}` + `.app-shell{100vw/100dvh; grid auto minmax(0,1fr)}` + `.workspace{min-height:0; grid minmax(280px,390px) minmax(0,1fr)}` + children `min-height:0` + preview `overflow:hidden`; Tablet ≤980 → คอลัมน์เดียว, Mobile ≤620 → ซ่อน non-critical panel; `@supports not backdrop-filter` → fallback `rgba(255,255,255,0.4)` ให้ยังอ่านได้
- Anchor `live`: fixed/sticky panel มีพื้นที่แน่นอน ไม่ถูกเบียด; fluid รอบข้างยืดหดไม่ดัน viewport overflow; ห้าม page-level scroll (internal panel scroll เท่านั้น)

## 5. Component States (ทุก interactive)

Default เทา / Hover สว่างขึ้น / Active เทาเงิน / Focus มี Focus Ring ชัด / Disabled เทาหม่น / Loading-Empty-Error มีข้อความแจ้ง ไม่ใช้สีอย่างเดียว

## 6. Acceptance (UI)

- [ ] ตรงภาพอ้างอิง + ธีมดำ-เทา + โลโก้เดิม + Sarabun/JetBrains Mono
- [ ] 3 breakpoints ไม่ทับซ้อน PDF ไมล์ล้น ตาราง scroll-x ได้
- [ ] PDF Viewer เปิดไฟล์จริงครบ PDF-01..09 พิมพ์/โหลด = ต้นฉบับเดียวกัน ไม่มี html2canvas
- [ ] Glass: blur เห็นบนพื้นดำ การ์ดลอย ขอบไม่หนัก ตัวอักษร contrast ผ่าน มี fallback
- [ ] สถานะระบบอ่านค่าจริง Corroboration Switch ไม่เคลมหลักฐาน
- [ ] ไม่แตะ Pipeline/Gate/Data Model; SFX/Password เป็น placeholder

## ผลลัพธ์
StackBlitz สร้าง UI ดำ-เทา Glass overlay ตาม Rev02 + Contract ที่ปรับแล้วได้ทันที โดย PDF ที่พิมพ์ = PDF ต้นฉบับจาก Pipeline เดิม
