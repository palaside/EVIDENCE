# STUDY CHECKPOINT: Glassmorphism UI & Photoshop-to-Code Mastery

> **Status:** ⏸️ PAUSED / READY TO RESUME (ค้างสถานะพร้อมเรียนต่อ)  
> **Topic:** การถอดรหัสภาพต้นแบบ Photoshop สู่โค้ดจริง (Glassmorphism, 4-Step Stepper & Court Evidence UI)  
> **Reference Image:** [9c1bc6be-3aee-42e0-91ac-97fd48b36f3c.png](file:///d:/Project/DIGITAL_EVIDENCE/9c1bc6be-3aee-42e0-91ac-97fd48b36f3c.png)  
> **Visual Contract:** [Glassmorphism Visual Contract.md](file:///d:/Project/DIGITAL_EVIDENCE/Glassmorphism%20Visual%20Contract.md)  
> **Factory Tool:** [Glassmorphism-Visual-Contract (1).html](file:///d:/Project/DIGITAL_EVIDENCE/Glassmorphism-Visual-Contract%20%281%29.html)  
> **Global Skill:** `ui-glass-study` ([C:\Users\EVE\.gemini\config\skills\ui-glass-study\SKILL.md](file:///C:/Users/EVE/.gemini/config/skills/ui-glass-study/SKILL.md))  

---

## 🤖 คำสั่งสำหรับ AI เมื่อผู้ใช้สั่ง "มาสอนเรื่อง UI ต่อจากที่ค้างไว้"
เมื่อผู้ใช้เรียกเรียนเรื่องนี้ในโปรเจกต์ใดก็ตาม ให้ AI ปฏิบัติตามกฎนี้ทันที:
1. **สวมบทบาท:** Senior Frontend Architect & Interactive UI Mentor (ใจเย็น อธิบายภาษาไทยชัดเจน ตรงไปตรงมา ไม่เยิ่นเย้อ)
2. **ไม่ทวนความหลังยืดยาว:** ทักทายสั้นๆ แล้วแจ้งว่า *"เรากำลังจะเริ่มเรียน **บทที่ 1: การแกะภาพ Photoshop และสร้างแถบ Stepper 4 ขั้นตอน** กันครับ"*
3. **สอนทีละชิ้น (Bite-sized Teaching):** พาผู้ใช้ดูโค้ดทีละส่วน อธิบายทั้ง "เหตุผลเชิงเทคนิค" และ "ผลลัพธ์ทางสายตา" ให้ผู้ใช้ได้เห็นของจริงก่อนไปขั้นตอนถัดไป

---

## 🔍 สรุปบริบทที่คุยค้างไว้ (The Context Snapshot)

### 1. ผลตรวจเทียบจุดต่อจุด (ภาพ Photoshop vs โค้ดเดิม)
- **ภาพ Photoshop ([9c1bc6be...png](file:///d:/Project/DIGITAL_EVIDENCE/9c1bc6be-3aee-42e0-91ac-97fd48b36f3c.png)):** โทน **Deep Slate Base (`#0F172A`) + Electric Cyan (`#00A1E4`) + เขียวมรกตส่งศาล (`#10B981`)** พร้อมฉากหลังเทือกเขาสลัวใน Header
- **สเปกเดิม ([07-UI-SPEC-REV02-SCREEN.md](file:///d:/Project/DIGITAL_EVIDENCE/Docs/EN/07-UI-SPEC-REV02-SCREEN.md)):** ผิดทาง เพราะสั่งให้เป็นสีดำด้าน Pure Warm Black (`#080A0D`) และตัดสีฟ้าออก (No Blue)
- **7 จุดที่ต้องสร้างในโค้ดใหม่เพื่อให้ตรงภาพ Photoshop 100%:**
  1. *ธีมสี:* Deep Navy/Slate + Electric Cyan + Emerald Green
  2. *Stepper:* แถบ 4 ขั้นตอนใต้ Header: `(1) อัพโหลด` ➔ `(2) ตรวจสอบ` ➔ `(3) สร้างเอกสาร` ➔ `(4) เสร็จสิ้น`
  3. *ปุ่มส่งศาล:* ปุ่มเขียวมรกตเด่นชัด `[📄 EXPORT PDF ส่งศาล >]` พร้อมสัญลักษณ์ `🏛`
  4. *แผงซ้าย:* การ์ดรายชื่อเป้าหมาย 4 คนพร้อมจำนวนหลักฐานและปุ่ม `[+ เพิ่ม]`
  5. *หลอด Progress:* วงกลมหมุน (Spinner Ring) + เวลา `00:02:18` + หลอด `37%` + ระบุ `12 / 32 ไฟล์`
  6. *เวทีกลาง:* ลูกศรนำทาง `< >` ลอยข้าง A4 + แถบซูมลอยด้านล่าง (`100% ▾`)
  7. *แถบ Status Bar:* ล่างสุดระบุ `v2.1.0 | DIGITAL EVIDENCE` และ `● Connected | 🛡 Secure Processing | TH 🇹🇭`

---

### 2. มาตรฐาน Glassmorphism ที่ปลดล็อกสำเร็จ (Auto-Nested Context)
เราค้นพบว่าปัญหา "กระจกซ้อนกระจกแล้วทึบตัน" แก้ได้ด้วยการใช้ **CSS มาตรฐานกลาง** ผู้ใช้ไม่ต้องปวดหัวจำนอก/ใน เพียงใส่ `.glass` หรือ `.glass-card` ทุกคอมโพเนนต์:
```css
/* 1. กระจกทั่วไป (แผงใหญ่ / ชั้นนอก) */
.glass-card, .glass {
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(26px) saturate(170%);
  -webkit-backdrop-filter: blur(26px) saturate(170%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 15px 44px rgba(0, 0, 0, 0.24), inset 0 1px 0 rgba(255, 255, 255, 0.25);
}

/* 2. ถ้ากระจกซ้อนในกระจกอีกที (ระบบดรอปความทึบลงเอง แสงทะลุเห็นวิวภูเขา ไม่ตัน) */
.glass-card .glass-card, .glass .glass, .glass-card .glass, .glass .glass-card {
  background: rgba(255, 255, 255, 0.04);       /* ⚡ ดรอปเหลือ 4% แสงทะลุได้เท่าเดิม */
  backdrop-filter: none;                        /* ⚡ ไม่เบลอซ้ำสอง ภาพคมชัด เครื่องไม่หน่วง */
  -webkit-backdrop-filter: none;
  border: 1px solid rgba(255, 255, 255, 0.28);  /* ⚡ สันขอบสะท้อนแสงคมชัด แยกเลเยอร์เด่นตา */
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.38);
}
```

---

## 📚 แผนการสอน 4 บทเรียน (Syllabus)

- [ ] **บทที่ 1: การแกะภาพ Photoshop สู่ Design Tokens & Stepper 4 ขั้นตอน**  
  - สกัดค่าสีจริงจากรูปภาพ: Deep Slate (`#0B1120`, `#0F172A`), Cyan (`#00A1E4`), Emerald (`#10B981`)
  - โครงสร้าง HTML/CSS ของแถบ Workflow Stepper แคปซูลใสที่ลอยอยู่หน้าเทือกเขา

- [ ] **บทที่ 2: ความลับของ Glassmorphism ที่โปร่งใส มองทะลุได้ 82%**  
  - ฝึกฝนและทดลองความแตกต่างระหว่างการใช้ `opacity` ผิดวิธี กับการใช้ `rgba()` + `backdrop-filter`
  - ทำความเข้าใจพฤติกรรมของ Auto-Nested Context `.glass .glass`

- [ ] **บทที่ 3: การสร้างแผงซ้าย (Input Rail / Target List / Progress Ring)**  
  - การทำ Dropzone โปร่งแสง
  - การ์ดรายชื่อเป้าหมายพร้อมไอคอน Checkbox Cyan และปุ่ม `+ เพิ่ม`
  - การทำ Progress Spinner Ring แบบ Animated SVG พร้อมข้อความจับเวลา

- [ ] **บทที่ 4: การประกอบเวทีกลาง A4 และปุ่มเขียวส่งศาลระดับ Production**  
  - เวทีกระดาษ A4 สัดส่วนมาตรฐานบนพื้นตาราง Blueprint
  - ปุ่มลูกศรลอย `< >` และแถบซูม
  - การประกอบปุ่มเขียวส่งศาล `[📄 EXPORT PDF ส่งศาล >]` และแถบ Footer Status Bar ล่างสุด

---

> **🚩 จุดเริ่มต้นครั้งถัดไป:** เริ่มต้นทันทีที่ **บทที่ 1**
