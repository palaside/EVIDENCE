---
name: vibe-build
description: สายพานสร้าง UI ครบ 8 ขั้นในสกิลเดียว: แบบฟอร์ม → สเปก → โทเค็น → ผังหน้า → พิมพ์เขียว → ชิ้นส่วน → หน้าจริง → เครื่องเสก — สั่ง "vibe-build" เดินยาวยิงเดียวจบ
---

# SKILL: vibe-build — สายพาน 8 ขั้น (เดินตามลำดับ ห้ามข้าม)

## 1. แบบฟอร์ม (SPECIFICATION TEMPLATE)
- ใช้แม่แบบโทน 1: Tactical / Executive / Deep Space; spacing×8, radius≤4, ตัวเลข mono

## 2. สเปก system-spec (ด่านล็อก)
- spec1 Society (ทำอะไร/ให้ใคร/สำเร็จคืออะไร) → spec2 Feature (F-001…+Acceptance) → spec3 Build (ไฟล์+เทสต์)
- 1 contract = 1-3 ไฟล์; จบขั้น gatekeeper ผ่าน/ตก + เหตุผล 1 บรรทัด

## 3. โทเค็น design-system
- 3 ชั้น primitive→semantic→component; ผ่าน WCAG 2.1 AA; รองรับ Dark/Light; ไฟล์ tokens กลาง 1 ไฟล์ ห้าม hardcode ใน component

## 4. ผังหน้า page-architecture
- ลิสต์ทุกหน้า: path/เนื้อหา/มาจากไหน/ไปไหนต่อ + 4 สถานะ (Loading/Empty/Error/Success); ตรวจครบตาม spec2

## 5. พิมพ์เขียว component-blueprint
- ต่อ component: ชื่อ/หน้าที่/props/states/variants; ทุก state มีหน้าตาชัด ใช้ tokens ล้วน

## 6. ชิ้นส่วน multitier-components
- 3 ชั้น primitive→composite→page-section ห้ามข้ามชั้นเรียก; TDD ก่อน implement; คุม re-render 60 FPS

## 7. หน้าจริง component-ui
- ประกอบตาม IA ห้ามสร้าง component กลางทาง; ครบ 4 สถานะ + Focus Ring; ห้าม AI-slop (gradient ซ้ำ/การ์ดลอย/ขอบเบลอรก); motion บอกสถานะเท่านั้น ease-out

## 8. เครื่องเสก project-scaffold-wizard
- เสกชุด Standalone + run.bat/run.ps1 + Silent Suite; จบด้วย run-tests เขียว + build ผ่าน + PROD_CHECKLIST 8 ข้อ
