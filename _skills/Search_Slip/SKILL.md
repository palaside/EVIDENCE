---
name: Search_Slip
description: สกิลตรวจจับและสกัดตำแหน่งหน้าที่มีการแปะสลิปโอนเงิน (Slip Detection & Page Indexing) จากไฟล์เอกสารหลักฐาน PDF ที่สร้างเสร็จแล้ว ส่งออกตารางสารบัญสลิปคดีความทั้งรูปแบบ Markdown, JSON และ Excel 10 คอลัมน์
---

# 🔎 Search_Slip Skill

สกิลนี้ถูกออกแบบมาเพื่ออำนวยความสะดวกในการค้นหา ระบุตำแหน่งเลขหน้า (Page Indexing) และสกัดข้อมูลสลิปโอนเงินที่ปรากฏอยู่ในไฟล์หลักฐาน PDF (เช่น `Evidence_Chat_V1.pdf`) โดยอัตโนมัติทันทีหลังจากการสร้างเล่ม PDF เสร็จสิ้น

---

## 🏛️ คุณสมบัติหลัก (Core Features)

### 1. ตรวจจับตำแหน่งหน้าสลิปอัตโนมัติ (Automated Page Detection)
- สแกนทุกหน้าในเอกสาร PDF ด้วย Computer Vision (ตรวจจับ Badge โอนเงินสำเร็จสีเขียว, การ์ดสลิป และ Header ธนาคาร)
- ระบุหมายเลขหน้าที่พบสลิปอย่างแม่นยำ เช่น **หน้า 64, 65, 97**

### 2. สกัดข้อมูลธุรกรรมสำคัญ (Forensic Transaction Extraction)
- **ยอดเงิน (Amount):** ดึงยอดเงินโอนทศนิยม 2 ตำแหน่ง (เช่น `2,000.00`, `4,000.00`)
- **รหัสอ้างอิงธุรกรรม (Reference ID):** ดึง Transaction Hash เช่น `A8bf6e4dda8fb4300`
- **วัน-เวลาที่ทำรายการ (Datetime):** สกัดวันและเวลา เช่น `23 ม.ค. 2568 - 14:42`
- **คู่ธุรกรรม (Sender & Receiver):** สกัดชื่อและเลขบัญชีตัดทอนของผู้โอนและผู้รับ
- **บันทึกช่วยจำ (Memo):** สกัดข้อความโน้ต เช่น `คืน 2500`

### 3. ป้องกันการนับสลิปซ้ำซ้อน (Intelligent Deduplication)
- กรณีที่สลิปใบเดียวกันปรากฏคาบเกี่ยว 2 หน้า (เช่น รอยต่อระหว่างหน้า 64 กับ 65) ระบบจะกรองและรวมรายการโดยอ้างอิงจากรหัสธุรกรรม (Reference ID) เดียวกัน

### 4. ส่งออกผลลัพธ์พร้อมใช้งาน 3 รูปแบบ (Triple Output Delivery)
1. **ตารางสรุปในคอนโซล (Markdown Table):** แสดงให้เห็นภาพรวมทันที
2. **ไฟล์ JSON สารบัญสลิป:** `Folder_Out/{PDF_NAME}_Slip_Index.json`
3. **ไฟล์ Excel สารบัญคดีความ:** `Folder_Out/{PDF_NAME}_Slip_Index.xlsx` (10 คอลัมน์มาตรฐานคดีความ)

---

## 🚀 วิธีการใช้งาน (Usage)

### 1. ใช้งานผ่านคำสั่ง (Standalone CLI)
```powershell
# สแกนไฟล์ PDF ที่ระบุ
python _skills/Search_Slip/scripts/search_slip.py "Folder_Out/Evidence_Chat_V1.pdf"

# หรือสแกนทุกไฟล์ PDF ในโฟลเดอร์ผลลัพธ์
python _skills/Search_Slip/scripts/search_slip.py "Folder_Out"
```

### 2. ทำงานอัตโนมัติหลังสร้าง PDF (Automated Pipeline Integration)
- สกิลนี้ถูกผูกเข้ากับ `List_names` และ `Dicut_Chat` โดยตรง เมื่อระบบประมวลผลเย็บแชทและสร้างไฟล์ PDF หลักฐานเสร็จ จะเรียก `search_slips_in_pdf` สกัดสารบัญสลิปออกมาให้ทันทีโดยอัตโนมัติ

### 3. เรียกใช้งานผ่าน Python Code
```python
from search_slip import search_slips_in_pdf

results = search_slips_in_pdf("Folder_Out/Evidence_Chat_V1.pdf", output_excel=True)
for item in results:
    print(f"หน้า {item['page']}: {item['amount']} บาท ({item['ref_id']})")
```
