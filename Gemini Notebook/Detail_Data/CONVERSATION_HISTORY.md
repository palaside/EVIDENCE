# 📜 บันทึกประวัติการสนทนาและการพัฒนาระบบ EVIDENCE (Conversation History)

เอกสารบันทึกทุกขั้นตอนการปรึกษา การออกแบบ การแก้ปัญหา และผลลัพธ์ที่ได้ ตั้งแต่เริ่มต้นจนถึงเวอร์ชันปัจจุบัน

---

## 📅 ลำดับเหตุการณ์และคำขอของผู้ใช้ (Chronological Milestones)

### 1. จุดเริ่มต้นและการวางโครงสร้างระบบ Excel (Detail_Data)
- **ความต้องการ**: แปลงข้อมูลสลิปที่สกัดได้จาก Gemini ให้เป็นไฟล์ Excel (.xlsx) ที่จัดหน้า A4 แนวนอน พร้อมแบ่งหน้าละ 20 บรรทัดอัตโนมัติ (Page Break)
- **การดำเนินการ**:
  - สร้างไฟล์ `schema.json` กำหนด 10 คอลัมน์มาตรฐาน
  - สร้างสคริปต์ `generate_excel.py` วางบล็อคละ 20 แถว พร้อมหัวเรื่อง โลโก้ EVIDENCE และข้อความ Disclaimer 3 บรรทัดจัดกึ่งกลาง
  - สร้าง `GEMINI_GEM_MASTER_PROMPT.md` เพื่อสร้าง Gemini Gem อ่านสลิปและส่งออกเป็น JSON

### 2. การสร้างระบบ Background Watcher & Google Drive Integration
- **ความต้องการ**: "โยนไฟล์ปุ๊บ อีกแปปออกมา" อยากได้ระบบอัตโนมัติที่ไม่ต้องพิมพ์คำสั่งในคอนโซล
- **การดำเนินการ**:
  - พัฒนา `gdrive_watcher.py` รองรับทั้ง Google Drive (`1zIo9YAXDsuxHXCWnFDdBS9hv7r1JvLct`) และโฟลเดอร์บน Desktop (`EVIDENCE_IN`, `EVIDENCE_CHAT_IN`, `Folder_Out`)
  - แก้ไขปัญหา Encoding ภาษาไทยบน Windows (cp1252 / charmap) และ stdout บน `pythonw.exe` โดยดักจับข้อความลง `watcher.log`
  - สร้าง `start_evidence_watcher.vbs` และเชื่อมเข้ากับ `Windows Startup` ให้รันเงียบสนิททุกครั้งที่เปิดเครื่อง

### 3. การพัฒนาสลิปเดี่ยวและใบสรุปแนวนอน (Dicut_Chat & Legal-Grade Evidence)
- **ฟีดแบคจากผู้ใช้**:
  1. *สลิปต้องอยู่กึ่งกลางกล่องทั้งแกน X และ Y*
  2. *สลิปละ 1 หน้าเดี่ยวๆ ห้ามซ้อนกัน*
  3. *หน้าสุดท้ายให้เป็นใบสรุป 10 คอลัมน์*
  4. *ใบสรุปต้องใช้ฟอนต์ Sarabun Light*
  5. *ปรับเป็นแนวนอนแค่แผ่นสรุปแผ่นเดียว*
  6. *ช่องตารางขยายออกกว้างขึ้น และตัวอักษรอยู่กึ่งกลางช่องทุกช่อง*
- **การดำเนินการ**:
  - เพิ่มฟังก์ชัน `trim_outer_padding()` ลบขอบขาวรอบสลิปอัตโนมัติ
  - ปรับการวางภาพสลิปเดี่ยว (Single Slip) บนหน้า A4 แนวตั้ง (Portrait 993 × 1406 px) วางตรงกึ่งกลางแกน X และ Y
  - เพิ่มฟังก์ชัน `add_10col_landscape_summary_page()` สลับหน้าสุดท้ายเป็น **A4 แนวนอน (1406 × 993 px)** ตารางกว้าง 1,202 px ใช้ฟอนต์ **`Sarabun-Light.ttf`** ข้อความและตัวเลขทุกเซลล์จัด **กึ่งกลาง (Center-Aligned)** ทั้งแนวนอนและแนวตั้ง

### 4. การต่อยอดสถาปัตยกรรม Automation และการส่งต่อ Gemini Notebook
- **ความต้องการ**: อธิบายชื่อทางเทคนิคของระบบนี้ (Hot Folder / Drop-and-Go Pattern) แนะนำแนวคิดระบบ Automation รูปแบบอื่นๆ และบันทึกข้อมูลทั้งหมดเป็น JSON, README, และ PROJECT_STATUS สำหรับนำไปวางใน Gemini Notebook

---

## 🛠️ รายการโมดูลและโค้ดสำคัญในระบบ

```
C:\Users\EVE\.gemini\config\skills\
├── Detail_Data/
│   ├── config/
│   │   ├── schema.json               # โครงสร้าง 10 คอลัมน์
│   │   └── gdrive_config.json        # ตั้งค่าโฟลเดอร์ Google Drive & Desktop
│   ├── scripts/
│   │   ├── generate_excel.py         # วาดตาราง Excel A4 แนวนอน 20 แถว/หน้า
│   │   ├── gdrive_watcher.py         # Master Watcher ตรวจจับ JSON & รูปภาพ
│   │   └── start_evidence_watcher.vbs # รันเบื้องหลังแบบ Silent Background
│   ├── GEMINI_GEM_MASTER_PROMPT.md   # พรอมต์สำหรับ Gem สกัดสลิป
│   ├── SKILL.md                      # นิยามสกิล Detail_Data
│   └── README.md                     # คู่มือและสถาปัตยกรรม Detail_Data
└── Dicut_Chat/
    ├── assets/
    │   └── EVIDENCE.png              # โลโก้สำหรับประทับหัวเอกสาร
    ├── scripts/
    │   └── process_chat.py           # Smart Slicing, Slip Center & Landscape Summary PDF
    ├── SKILL.md                      # นิยามสกิล Dicut_Chat
    └── README.md                     # คู่มือและสเปค Dicut_Chat
```
