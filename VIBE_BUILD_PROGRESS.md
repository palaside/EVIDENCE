# 🏗️ VIBE-BUILD: DIGITAL EVIDENCE SYSTEM
## สายพานสร้างระบบ 8 ขั้น (Step 1 ถึง Step 8)
### สถานะ: ดำเนินการตามลำดับ ห้ามข้ามขั้นตอน | Forensic Court-Ready Single User

---

## 📌 ขั้นที่ 1: แบบฟอร์ม (Specification Template & Foundation)
- **ผู้ใช้งาน:** ผู้ใช้คนเดียว (Single Investigator / Forensic Officer)
- **โจทย์ระบบ:** รวมรวมพยานหลักฐานดิจิทัล (สลิปธนาคาร, หน้าแชทต่อเนื่อง, สเตตเมนต์) มาจัดระเบียบ ตรวจสอบความถูกต้อง สกัดข้อมูลระดับพิกเซล และส่งออกสำนวนคดีระดับศาล
- **นิยามความสำเร็จ:** นำไฟล์พยานหลักฐานทั้งหมดเข้าสู่ระบบ แล้วสกัดยอดเงิน คู่ธุรกรรม วันเวลา ล้างยศ/คำนำหน้า จัดวางลงกระดาษ A4 กึ่งกลาง (322.5, 445) โดยไม่บิดเบี้ยว และส่งออกเป็น Master Dossier (PDF + Excel 11 คอลัมน์ + WinRAR SFX Archive) พร้อมผ่านการตรวจ Forensic Quality Gate 100%
- **Design Baseline:**
  - โทน: **Cyber Tactical Navy Dark** (`#12243D` Canvas / `#8E9AA6` Grey / `#00A1E4` Sky Blue / `#fde8e8` Failed Highlight)
  - Spacing: **8-Point Grid** (4, 8, 12, 16, 24, 32, 48px)
  - Radius: **≤ 4px**
  - ตัวเลขและรหัสอ้างอิง: **JetBrains Mono**
  - ภาษาไทย: **Sarabun Light** (16px body, 18-24px headers)

---

## 📌 ขั้นที่ 2: สเปก system-spec (ด่านล็อก spec1 / spec2 / spec3)

### 2.1 `spec1: Society`
- **ทำอะไร:** ระบบแปลงและจัดระเบียบพยานหลักฐานดิจิทัลอัตโนมัติ (Digital Evidence SPA & Pipeline)
- **ให้ใคร:** เจ้าหน้าที่ผู้ปฏิบัติงานด้านคดีความคนเดียว (Single User Standalone)
- **สำเร็จคืออะไร:** ดรอปไฟล์สลิป/แชท $\rightarrow$ สกัดข้อมูลตรงเป๊ะ 100% $\rightarrow$ พรีวิวกระดาษจำลอง $645 \times 890\text{px}$ $\rightarrow$ เซฟ PDF/WinRAR SFX พร้อมรหัสผ่าน

### 2.2 `spec2: Feature & Acceptance Criteria`
- **F-001 (Mode Tabs):** สลับโหมด `[ CHAT ]` และ `[ SLIP ]` ด้วยความเร็ว `< 16ms`
- **F-002 (Evidence Dropzone):** รับไฟล์ลากวาง (Drag & Drop) ได้สูงสุด 500 ภาพต่อแบทช์ พร้อมแผง File List View และปุ่มคัดไฟล์ออก
- **F-003 (Mathematical Stage):** จัดวางรูปภาพลงพิกัดจุดกึ่งกลาง $(322.5, 445)$ รักษาสัดส่วนภาพเดิม (Aspect Ratio Lock) ห้ามยืดเด็ดขาด
- **F-004 (11-Column Ledger Table):** สกัดและแสดงตาราง 11 คอลัมน์ (ลำดับ, วันที่, เวลา, ธนาคารผู้โอน, ชื่อผู้โอนล้างยศ, จำนวนเงิน, ชื่อผู้รับล้างยศ, ธนาคารผู้รับ, บันทึกช่วยจำ, Ref ID, หมายเหตุ) พร้อมไฮไลต์สีแดงอ่อน `#fde8e8` แถวธุรกรรมล้มเหลว
- **F-005 (Summary Row):** แสดงผลรวม (Total Sum) และค่าเฉลี่ยสะสม (Average Sum) ขีดเส้นใต้คู่ (Double Underline)
- **F-006 (Security & Password Toggle):** ระบบล็อกสิทธิ์เปิด/ปิดรหัสผ่าน หากปิดปุ่มเซฟจะแสดงสถานะ Disabled (Opacity 40%)
- **F-007 (WinRAR SFX Exporter):** รองรับการแพ็กเกจเป็นไฟล์ `.exe` พร้อมคำประกาศปฏิเสธความรับผิดชอบอย่างเป็นทางการ

### 2.3 `spec3: Build & Contracts`
- สัญญาของระบบ (Contracts):
  1. `tokens.css`: ศูนย์รวม CSS Variables กลาง
  2. `components.js`: ชิ้นส่วน Primitive, Composite, Page Section
  3. `app.js` & `index.html`: หน้าหลัก SPA รองรับ 4 สถานะ

> 🛡️ **Gatekeeper Verdict (ด่านล็อกขั้นที่ 2):** **[ผ่าน 100%]**  
> *เหตุผล:* สเปกครอบคลุมครบถ้วนตามหลักการของคดีความ มีเกณฑ์ยอมรับชัดเจนและไม่มีการคาดเดาข้อมูล
