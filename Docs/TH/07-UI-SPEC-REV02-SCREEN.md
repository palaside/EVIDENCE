# 07 · UI SPEC — Rev02 Dark Gray (Screenshot-Grounded)
# โครงการ DIGITAL_EVIDENCE

> ตำแหน่ง: `Docs/TH/07-UI-SPEC-REV02-SCREEN.md` (สร้างใหม่ ห้ามแก้ต้นฉบับ)
> อ้างอิงภาพ: screenshot 3 คอลัมน์ (header CHAT/SLIP + DONE 100% + timer + SYNC + สรุปทั้งหมด)
> โค้ดอ้างอิง: `DIGITAL_EVIDENCE_REV02.html` (serve 200 :8010), backend `tools/rev02_server.py`

## 1. โทนที่ล็อก (จากจอ)

- พื้นหลังดำล้วนโทนอบอุ่น `#080A0D` + ambient glow เทา (ไม่มีฟ้า): ตามภาพทั้ง 3 พาเนลเป็นการ์ดดำด้านขอบมนบนพื้นดำ
- การ์ด: พื้น `rgba(255,255,255,.03-.075)` + blur 26px + ขอบ `rgba(255,255,255,.12)` + เงา `0 15px 44px rgba(0,0,0,.4)` + highlight ขอบบน
- ปุ่มหลัก (Accept / Generate / พิมพ์ PDF): ไล่เฉดเงิน `linear-gradient(180deg,#E6EBF0,#AEB6BF)` ตัวอักษรดำ `#0B0E12` — ตามภาพปุ่ม Accept/Generate/พิมพ์เป็นแถบเงินเต็มความกว้าง
- ปุ่มรอง (CHAT active / แท็บ PDF / Run): เทา `#747D87` หรือพื้น `#1B2026` ขอบ `#343B44`
- สถานะ: จุดเขียว + `DONE · 100%` (header), chip `queued` เทา, log `[OK]` ขาว/เทา; เขียว `#16A34A` ส้ม `#F59E0B` แดง `#DC2626` ใช้เฉพาะสถานะจริง + มีข้อความประกอบ
- ฟอนต์: Sarabun (ไทย/อังกฤษ), JetBrains Mono (ตัวเลข/Ref/ขนาดไฟล์/log/เวลา) — ตามภาพชื่อไฟล์+ขนาด `1972297 B` และ log `[01/4]` เป็น mono

## 2. Layout (ตามภาพ)

- Header เดียว: โลโก้ DE + `DIGITAL_EVIDENCE หลักฐานดิจิทัล · Rev02 Dark Gray` + seg `CHAT|SLIP` + status pill (`DONE · 100% · กด Generate…`) + timer `00:00` + `⟳ SYNC` + `สรุปทั้งหมด`
- 3 คอลัมน์ 28/44/28 gap 14px padding 14px, fit-to-screen `100dvh` ไม่มี page scroll (scroll ในพาเนลเท่านั้น)
- LEFT: eyebrow `LEFT · CONTROLS` + หัวข้อ `อัปโหลด & ค้นหา`
- CENTER: eyebrow `CENTER · REVIEW` + หัวข้อ `ผลประมวลผล — จากงานที่ Accept`
- RIGHT: eyebrow `RIGHT · SUMMARY` + หัวข้อ `สรุป & ส่งออก`

## 3. LEFT — Controls (ตามภาพ)

1. **Upload & File Queue:** dropzone ประ `ลากไฟล์มาวาง… JPG · PNG · PDF` + แถวไฟล์ 4 แถว (`V1- (1..4).jpg` + ขนาด B + `รอตรวจ`) + chip `queued` ขวา ตามภาพ
2. **Search & Target:** ช่องค้น `⌕ ค้น Ref / ชื่อ / วันที่ / ธนาคาร…` + tags ว่าง + บรรทัดสถานะ `ยังไม่อัปไฟล์ — 0 รายการ` (ห้ามโชว์ชื่อก่อนรัน — กฎ zero-state)
3. **Corroboration:** switch + ข้อความ `กรองเฉพาะสลิป-แชทสอดคล้อง` + หมายเหตุ `สถานะ switch นี้ไม่ใช่หลักฐานยืนยัน`
4. **✓ Accept — เริ่มประมวลผล:** ปุ่มเงินเต็มกว้าง วางระหว่าง Corroboration กับ Processing (ตามคำสั่ง) กดแล้วอัปโหลด→รัน OCR จริง
5. **Processing:** checkbox `--mask-pii (PDPA)` + ปุ่ม `⚡ Generate — แสดงผลกลาง` (disabled จนกว่างานครบ 100%) + แถว `ความคืบหน้า … 100%` + หลอด progress เต็ม + บรรทัด `generated · 4 แถว · REV02_…xlsx` + กล่อง log mono (บรรทัด `$ …ocr_slip.py`, `[01/4] V1-… Amount: … Ref: …`, `[OK] Saved Excel/JSON ledger: …`)

## 4. CENTER — Review (ตามภาพ)

- Toolbar: แท็บ `PDF | ผลลัพธ์` + `‹ 1 / ? ›` + ช่อง `หน้า` + `Fit` + `⛶ Full` + `🖨 พิมพ์ต้นฉบับ` (เงิน) + `⤓ ดาวน์โหลด`
- Stage: พื้นดำลายจุด ก่อน Generate เป็นที่ว่าง (ตามภาพ stage ดำว่าง + บรรทัดล่าง `เนื้อ PDF จากการตรวจสอบ`) หลัง Generate แสดงตารางผลงาน `#/ไฟล์/ธนาคาร/ยอด/Ref/สถานะ` (จาก `/api/result` จริง ไม่ใช่ mock)
- PDF ที่อัปดูแท็บ PDF ผ่าน object URL (ไบต์จริงของผู้ใช้) พิมพ์/โหลด = ต้นฉบับเดียวกัน ห้าม html2canvas

## 5. RIGHT — Summary (ตามภาพ)

- KPI 2×2: `หลักฐาน 4 | ดู audit | รายชื่อ 1 | แถวสรุป 4` (เลข mono ใหญ่, นับจากผลรันจริงเท่านั้น เปิดมาเป็น 0)
- Evidence PDFs: ตาราง `ไฟล์ที่อัป (PDF) | เปิด` (ว่างจนกว่าจะอัป PDF)
- Master Slips: การ์ด `ต้นฉบับ vs ซ้ำ (Auditor ผลรันนี้)` + แถบ unique
- Document Actions: ปุ่มเงิน `🖨 พิมพ์ PDF ต้นฉบับ` + ปุ่มรอง `⤓ ดาวน์โหลด PDF ต้นฉบับ` + หมายเหตุ `SFX / รหัสผ่าน: placeholder`

## 6. Flow (ตามภาพ)

```text
อัปไฟล์ (4 ใบ) → กด Accept → upload → OCR รันจริง (% จาก log [i/n]) → 100% → ปุ่ม Generate ปลดล็อก
→ กด Generate → ตารางกลาง + KPI/tags/hits ขวา (เลขตรง log: generated · 4 แถว · REV02_….xlsx)
```

## 7. States

- เริ่มต้นทุกอย่าง 0 (KPI/tags/ตาราง/หลอด) — ห้าม preload index เก่า 95 แถว
- ระหว่างรัน: status `UPLOADING/RUNNING`, หลอดขยับตาม % จริง, log tail สด, Accept/Generate disabled
- 100%: status `DONE · 100% · กด Generate`, Generate enabled
- พัง: status `FAILED/ERROR` + เหตุผล, หลอด 0, Accept กลับมากดได้

## 8. Acceptance

- [ ] เปิดมา 0 ทุกแผง ไม่ชื่อโผล่ ไม่เลขอ้างของเก่า
- [ ] Accept→100%→Generate จบด้วยไฟล์ `REV02_*.xlsx/.json` จริงบนดิสก์
- [ ] ตารางกลาง = แถวใน JSON จริง, KPI = จำนวนจริง
- [ ] ไม่มีสีฟ้า accent, ตัวอักษร contrast ผ่าน, focus ring เงิน, ลด motion ได้
- [ ] Responsive: ≤1239 สองคอลัมน์, ≤1023 คอลัมน์เดียว (PDF สูง ≥62vh)

## ผลลัพธ์
Spec นี้ = ภาพที่อีฟ approve + พฤติกรรม Accept/Generate จริง ใช้อ้างอิงงาน UI ต่อไปโดยไม่แตะ Pipeline เดิม
