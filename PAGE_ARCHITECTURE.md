# 🗺️ PAGE ARCHITECTURE (IA & 4 STATES)
## Digital Evidence Court-Ready SPA

---

## 1. Single Page View Routing & Hierarchy

```
[ Root: / ]
 ├── [Header Section (15%)]: Mode Selector (CHAT vs SLIP) + Brand Header
 └── [Main Section (85%)]: 3-Column Working Grid
      ├── [Column Left (25%)]: Upload Zone + Queue List + Process Button
      ├── [Column Middle (50%)]: Aspect-Ratio Locked 645x890px Canvas Preview
      └── [Column Right (25%)]: Summary Button + Password Switch + Save Buttons + Generate
```

---

## 2. The 4 Mandatory States Matrix

| คอมโพเนนต์ / ส่วน | 1. Loading State | 2. Empty State | 3. Error State | 4. Success / Ready State |
|---|---|---|---|---|
| **Mode Tabs** | Shimmer indicator | Default to `[ SLIP ]` | Border red if sync fails | Glow on active tab |
| **Upload Zone** | Progress spinner | Cloud icon + "ลากไฟล์มาวาง" | "ไฟล์เกิน 500 ภาพ" / Red border | แสดงจำนวนไฟล์ในคิว |
| **File List View** | Skeleton rows | "ยังไม่มีไฟล์ในคิว" | Highlight ไฟล์ที่ชำรุด | แสดงรายการไฟล์ + ขนาด |
| **Canvas Stage** | กระดาษขาว + Shimmer | แสดงโครงกระดาษเปล่า 645x890 | แจ้งเตือน "ไฟล์ภาพเสีย" | ภาพสลิปจัดกึ่งกลาง (322.5, 445) |
| **Summary Table** | Skeleton 4 แถว | "ยังไม่มีข้อมูลที่สกัดได้" | ไฮไลต์แถว `#fde8e8` | 11 คอลัมน์ + Double Underline |
| **Save / Generate** | Spinner "กำลังสร้าง PDF..." | Disabled ถ้าไม่มีไฟล์ | แจ้งเตือนรหัสผ่านไม่ตรง | ดาวน์โหลดไฟล์ Master Dossier |
