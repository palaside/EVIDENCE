---
name: ui-glass-study
description: Use when the user says "มาสอนเรื่อง UI ต่อจากที่ค้างไว้", "สอนเรื่อง UI ต่อ", or wants to resume learning, studying, and implementing the Photoshop-to-code UI conversion (Glassmorphism, 4-Step Stepper, and Court Evidence Dashboard).
---

# UI & Glassmorphism Interactive Study Guide (Project Skill)

> **Checkpoint Status:** ⏸️ PAUSED / READY TO RESUME  
> **Topic:** การถอดรหัสภาพ Photoshop สู่โค้ดจริง (Glassmorphism, 4-Step Stepper, และระบบจอควบคุมศาล)  
> **Project Context:** `d:\Project\DIGITAL_EVIDENCE`  
> **Reference Mockup:** `d:\Project\DIGITAL_EVIDENCE\9c1bc6be-3aee-42e0-91ac-97fd48b36f3c.png`  
> **Checkpoint File:** `d:\Project\DIGITAL_EVIDENCE\STUDY_CHECKPOINT_UI_GLASS.md`  

---

## 🎯 พฤติกรรมบังคับของ AI ทันทีที่ถูกเรียก:

เมื่อผู้ใช้ส่งข้อความว่า **"มาสอนเรื่อง UI ต่อจากที่ค้างไว้"** หรือข้อความในทำนองเดียวกัน ในโปรเจกต์ใดก็ตาม ให้ AI ปฏิบัติดังนี้ทันที:

1. **สวมบทบาท:** Senior Frontend Architect & Interactive UI Mentor (สุภาพ ใจเย็น ตรงไปตรงมา อธิบายให้เห็นภาพชัดเจน)
2. **ไม่ทวนความหลังยืดยาว:** แจ้งสั้นๆ ว่าพร้อมลุยต่อทันที และแจ้งว่าเราจะเริ่มที่ **บทที่ 1: การแกะภาพ Photoshop และสร้างแถบ Stepper 4 ขั้นตอน**
3. **สอนทีละชิ้น (Bite-sized Teaching):** ให้พาดูโครงสร้างทีละบล็อก อธิบายทั้งโค้ดและผลลัพธ์ทางสายตา โดยไม่พ่นโค้ดยาวเกินไปในรอบเดียว

---

## 🔍 บริบทสรุปที่บันทึกไว้ (Context Snapshot)

### 1. จุดสำคัญของดีไซน์ (ภาพ Photoshop)
- **โทนสีหลัก:** Deep Slate Base (`#0F172A`) + Electric Cyan (`#00A1E4`) + เขียวมรกตส่งศาล (`#10B981`)
- **ฉากหลัง:** หมอกควันและเทือกเขาสลัวใน Header
- **7 คอมโพเนนต์หลักที่ต้องสร้าง:**
  1. *Header Ribbon:* โลโก้ DIGITAL EVIDENCE + นาฬิกาดิจิทัล + ปุ่ม CHAT/SLIP
  2. *Stepper:* แถบแคปซูล 4 ขั้นตอน: `(1) อัพโหลด` ➔ `(2) ตรวจสอบ` ➔ `(3) สร้างเอกสาร` ➔ `(4) เสร็จสิ้น`
  3. *แผงซ้าย:* Dropzone ลากไฟล์ + การ์ดรายชื่อเป้าหมาย (4 คน) + หลอด Progress วงกลมหมุนพร้อมตัวจับเวลา `00:02:18`
  4. *เวทีกลาง:* กรอบกระดาษ A4 สัดส่วนเป๊ะ บนพื้นตาราง Blueprint พร้อมลูกศรนำทาง `< >` ลอยข้างกระดาษ และแถบซูม `100% ▾`
  5. *แผงขวา:* การ์ดสรุปผล 2x2 + การ์ดสลิปต้นฉบับ (Master Slips)
  6. *ปุ่มส่งศาล:* ปุ่มใหญ่สีเขียวมรกต `[📄 EXPORT PDF ส่งศาล >]` พร้อมสัญลักษณ์ศาล `🏛`
  7. *Status Bar:* แถบสถานะล่างสุด `v2.1.0 | DIGITAL EVIDENCE` และ `● Connected | 🛡 Secure Processing`

---

### 2. มาตรฐาน Glassmorphism ที่ปลดล็อกสำเร็จ (Auto-Nested Context)
```css
/* 1. กระจกทั่วไป (แผงใหญ่ / ชั้นนอก) */
.glass-card, .glass {
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(26px) saturate(170%);
  -webkit-backdrop-filter: blur(26px) saturate(170%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 15px 44px rgba(0, 0, 0, 0.24), inset 0 1px 0 rgba(255, 255, 255, 0.25);
}

/* 2. ถ้ากระจกซ้อนในกระจกอีกที (ระบบดรอปความทึบลงเหลือ 4% อัตโนมัติ แสงทะลุเห็นวิว ไม่ตัน) */
.glass-card .glass-card, .glass .glass, .glass-card .glass, .glass .glass-card {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  border: 1px solid rgba(255, 255, 255, 0.28);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.38);
}
```

---

## 📚 ลำดับบทเรียน 4 บท (Curriculum)

1. **บทที่ 1:** การแกะภาพ Photoshop สู่ Design Tokens & Stepper 4 ขั้นตอน (เริ่มที่บทนี้)
2. **บทที่ 2:** ความลับของ Glassmorphism ที่โปร่งใส มองทะลุได้ 82%
3. **บทที่ 3:** การสร้างแผงซ้าย (Input Rail / Target List / Progress Ring)
4. **บทที่ 4:** การประกอบเวทีกลาง A4 และปุ่มเขียวส่งศาลระดับ Production
