ต่อไปนี้คือเอกสาร UI Specification ฉบับปรับปรุงล่าสุดสำหรับโปรเจกต์ DIGITAL_EVIDENCE โดยยึดภาพ Dashboard ที่อีฟส่งมาเป็นต้นแบบหลัก เปลี่ยนสีฟ้าของ UI เป็นสีเทา คงธีมสีดำและโลโก้ต้นฉบับ พร้อมกำหนดให้หน้าจอ Responsive และ Review แสดงไฟล์ PDF จริงที่ใช้พิมพ์ได้

เอกสารนี้ใช้เป็นข้อกำหนดให้ผู้พัฒนาออกแบบและเขียนโค้ดบน StackBlitz โดยไม่เปลี่ยนแปลงระบบ Python Pipeline เดิม

DIGITAL_EVIDENCE
UI/UX DESIGN SPECIFICATION
UI DESIGN SPEC · REVISION 02
Digital Evidence Dashboard

Responsive Dark Gray Interface & Real PDF Review

Design Reference

ภาพ Dashboard ล่าสุดของผู้ใช้

Target Platform

StackBlitz / Windows

Frontend

HTML / CSS / JavaScript

Backend เดิม

Python Pipeline

สถานะเอกสาร

Design Specification
1. ข้อกำหนดหลักของงานออกแบบ

REQ-01 — Reference Fidelity

ยึดภาพ Dashboard ล่าสุดเป็นต้นแบบหลักของ Layout, Header, Panel, Navigation, Spacing, Typography และลำดับความสำคัญของข้อมูล

REQ-02 — Black & Gray Theme

ใช้สีดำเป็นพื้นหลังหลัก เปลี่ยนสีฟ้าที่ใช้เป็น Accent ใน UI เป็นสีเทา โดยยังอนุญาตให้ใช้สีเขียว ส้ม และแดงสำหรับแสดงสถานะระบบ

REQ-03 — Responsive Layout

รองรับ Desktop, Tablet และ Mobile โดยองค์ประกอบต้องไม่ทับซ้อนกัน และหน้าต่าง Review ต้องปรับขนาดตามพื้นที่ที่มีอยู่จริง

REQ-04 — Actual PDF Review

แสดง PDF จากไฟล์จริง ไม่ใช้ภาพ A4 จำลองแทนไฟล์ PDF และต้องรองรับการเปิดเอกสารต้นฉบับเพื่อพิมพ์

REQ-05 — Original Brand Identity

ใช้โลโก้ DIGITAL EVIDENCE ที่ผู้ใช้ส่งมา โดยไม่วาดใหม่หรือเปลี่ยนองค์ประกอบภายในโลโก้

REQ-06 — Existing System Compatibility

ไม่เปลี่ยนแปลง Python Pipeline, OCR, Quality Gate, Database Model และโครงสร้างหลักฐานเดิมโดยไม่ได้รับอนุญาต

2. Design System — สีและรูปแบบ
2.1 Color Palette

DIGITAL EVIDENCE — MONOCHROME DARK

Background

#080A0D

Panel

#111418

Surface

#1B2026

Elevated

#252B32

Primary Gray

#747D87

Hover

#929AA3

Border

#343B44

Text

#F3F4F6

สีแสดงสถานะ

Success

#16A34A

Warning

#F59E0B

Error

#DC2626

กฎการใช้สี: ทุกองค์ประกอบ UI ที่เดิมเป็นสีน้ำเงินหรือสีฟ้า เช่น Active Tab, Button, Border, Focus Ring, Progress Bar และ Selected Item ต้องเปลี่ยนเป็นโทนสีเทา ส่วนสีเขียว ส้ม และแดงให้ใช้เฉพาะเมื่อสื่อถึงสถานะที่มีความหมายจริง

โลโก้ต้นฉบับและเนื้อหาภายในเอกสาร PDF ไม่อยู่ภายใต้กฎการเปลี่ยนสีนี้ โดยเฉพาะ PDF ต้องแสดงสีตามไฟล์จริงทุกประการ

2.2 Typography และ Spacing

องค์ประกอบ

	

ข้อกำหนด




ฟอนต์ภาษาไทย

	

Sarabun




ฟอนต์ภาษาอังกฤษ

	

Sarabun




ฟอนต์ตัวเลข / RefID

	

JetBrains Mono




Page Title

	

20–24px




Panel Title

	

15–17px




Body Text

	

13–14px




Secondary Text

	

12–13px




Panel Radius

	

10–12px




Input / Button Radius

	

6–8px




Panel Padding

	

16px




ระยะห่างระหว่าง Panel

	

12px

ขนาดทั้งหมดเป็นค่าเริ่มต้นสำหรับพัฒนา สามารถปรับตามความละเอียดหน้าจอเพื่อรักษาความอ่านง่ายได้

3. Main Dashboard Layout
3.1 Desktop Layout

กำหนดสัดส่วนคอลัมน์เริ่มต้นที่ 28% / 44% / 28% โดยคิดจากพื้นที่เนื้อหาหลังหักระยะห่างระหว่างคอลัมน์

DIGITAL EVIDENCE

หลักฐานดิจิทัล

ONLINE

CHAT

SLIP

UPLOAD → PROCESS → DOCUMENT → REVIEW

CONTROLS

Upload

Search

Targets

Process

PDF REVIEW

‹　1 / 12　›　−　100%　+

SUMMARY

KPI 1

KPI 2

KPI 3

KPI 4

Master Slips

EXPORT PDF

แผนผังแสดงสัดส่วนและลำดับส่วนประกอบ ไม่ใช่ภาพหน้าจอที่ Render จากโค้ดจริง
3.2 Responsive Breakpoints

ขนาดหน้าจอ

	

พฤติกรรม




Desktop ≥ 1440px

	

แสดง 3 คอลัมน์ 28/44/28




Laptop 1024–1439px

	

ปรับสัดส่วนตามพื้นที่จริง โดยให้ PDF Review อ่านได้ชัดเจน




Tablet 768–1023px

	

PDF Review อยู่ด้านบน แผง Controls และ Summary อยู่ด้านล่าง




Mobile ต่ำกว่า 768px

	

แสดงเป็นคอลัมน์เดียว พร้อม Navigation สำหรับสลับส่วน

ข้อกำหนดเพิ่มเติม:

ห้ามกำหนดความกว้าง PDF Viewer แบบตายตัวจนเกิดการล้นหน้าจอ

ทุก Panel ต้องจัดการ Overflow ของตนเอง

ตารางข้อมูลจำนวนมากต้องเลื่อนในแนวนอนได้

ปุ่มสำคัญต้องกดได้โดยไม่ต้องซูมหน้าเว็บไซต์

PDF ต้องรักษาอัตราส่วนของหน้ากระดาษต้นฉบับ

4. Header Specification
HEADER — Global Navigation

ตำแหน่งด้านบนสุดของ Dashboard

องค์ประกอบที่ต้องมี

โลโก้ DIGITAL EVIDENCE ต้นฉบับ

ชื่อระบบภาษาไทยและภาษาอังกฤษ

ปุ่ม CHAT / SLIP

สถานะระบบ

ตัวจับเวลาการประมวลผล

ปุ่ม SYNC

ปุ่มสรุปทั้งหมด

พฤติกรรม

เมื่อเลือก CHAT หรือ SLIP ต้องเปลี่ยน Active State ให้ตรงกับโหมดที่เลือก และแสดงข้อมูลหรือเครื่องมือที่เกี่ยวข้องกับโหมดนั้น

สถานะระบบต้องอ่านจากข้อมูลสถานะจริงเมื่อเชื่อมต่อระบบหลักแล้ว ห้ามแสดง ONLINE หรือ READY ตลอดเวลาโดยไม่มีข้อมูลรองรับ

5. Left Panel — Controls
LEFT PANEL

Upload · Search · Target · Processing

01 — Upload & File Queue

เลือกไฟล์ภาพหรือ PDF จากเครื่อง

รองรับ Drag & Drop ตามประเภทไฟล์ที่ระบบกำหนด

แสดงชื่อไฟล์ ขนาด และสถานะ

เลือกไฟล์ที่ต้องการตรวจสอบ

ลบไฟล์ออกจากคิวก่อนส่งประมวลผล

02 — Search & Target Matching

ค้นหาชื่อบุคคลหรือข้อมูลตามเงื่อนไขที่ระบบรองรับ

แสดงรายการเป้าหมายที่ค้นพบ

เลือกเป้าหมายเพื่อกรองข้อมูล

แสดงจำนวนหลักฐานที่สัมพันธ์กับเป้าหมายเมื่อมีข้อมูลจริง

03 — Corroboration

แสดงสถานะการตรวจสอบความสอดคล้องระหว่างสลิปกับแชท

มี Switch สำหรับเปิดหรือปิดตัวกรองผลลัพธ์ตามที่กำหนดใน UI เดิม

ห้ามใช้การเปลี่ยนสถานะ Switch เป็นหลักฐานยืนยันว่าข้อมูลสอดคล้องกันจริง

04 — Processing

ปุ่มเริ่มประมวลผลหลักฐาน

Progress Bar

เวลาที่ใช้ประมวลผล

จำนวนไฟล์ที่ดำเนินการแล้ว

สถานะผิดพลาดหรือรายการที่ต้องตรวจซ้ำ

ส่วน Upload, Processing และ Target Matching อ้างอิงจากต้นแบบ HTML และข้อกำหนดของ Pipeline เดิม อย่างไรก็ตาม การเรียกประมวลผลจากหน้าเว็บยังต้องออกแบบจุดเชื่อมต่อกับ Python บน Windows ในขั้น Integration 
PROJECT_EVIDENCE_3COL_PROTOTYPE.html
03-ARCHITECTURE.md

6. Center Panel — Real PDF Review
Critical Requirement

หน้าจอ Review ต้องแสดงผลจาก PDF ต้นฉบับที่ระบบสร้างขึ้นหรือไฟล์ PDF ที่ผู้ใช้เลือก ไม่ใช่ภาพเอกสารจำลอง

6.1 PDF Viewer Features

ID

	

ฟีเจอร์

	

พฤติกรรมที่ต้องการ




PDF-01

	

Open PDF

	

เปิดไฟล์ PDF จริง




PDF-02

	

Page Navigation

	

ก่อนหน้า / ถัดไป / ระบุเลขหน้า




PDF-03

	

Zoom

	

ขยายและย่อ PDF




PDF-04

	

Fit to Width

	

ปรับหน้ากระดาษให้พอดีกับพื้นที่




PDF-05

	

Fullscreen

	

ขยายพื้นที่ Review




PDF-06

	

Print

	

เปิดไฟล์ PDF ต้นฉบับเพื่อพิมพ์




PDF-07

	

Download

	

ดาวน์โหลดไฟล์ PDF ต้นฉบับ




PDF-08

	

Page Link

	

เปิด PDF ตามหมายเลขหน้าจากสารบัญหลักฐาน




PDF-09

	

Loading / Error

	

แสดงสถานะเมื่อโหลดไฟล์หรือแสดงผลไม่สำเร็จ

6.2 PDF Review Flow
เลือกไฟล์ PDF
โหลดไฟล์ด้วย PDF Viewer
อ่านจำนวนหน้าและแสดงผลจาก PDF จริง
ผู้ใช้ตรวจทานเอกสาร

เปิด PDF ต้นฉบับเพื่อพิมพ์หรือดาวน์โหลด

ข้อห้าม: ไม่ใช้ html2canvas หรือการจับภาพหน้าจอ Dashboard เพื่อสร้างไฟล์พิมพ์ เพราะไฟล์ที่พิมพ์ต้องเป็น PDF ต้นฉบับเดียวกับที่ใช้ตรวจทาน

การสร้างเนื้อหา PDF, การจัดหน้า และการรับรองเอกสารยังคงเป็นหน้าที่ของ Pipeline เดิม ไม่ใช่หน้าที่ของ PDF Viewer 
02-SRS.md

7. Right Panel — Summary & Actions
RIGHT PANEL

Statistics · Audit · Export

01 — KPI Summary

จำนวนหลักฐานที่ตรวจพบ

จำนวนรายการสลิปและแชทที่สอดคล้องกัน

จำนวนรายชื่อที่พบ

จำนวนรายการในตารางสรุป

02 — Evidence Summary Table

ปุ่มเปิดตารางสรุปทั้งหมด

แสดงข้อมูลตามคอลัมน์ที่ระบบส่งออกจริง

ค้นหาและกรองรายการ

แสดงสถานะ Audit และรายการซ้ำ

03 — Master Slips

จำนวนสลิปต้นฉบับ

จำนวนรายการซ้ำ

ปุ่มดูรายการสลิปต้นฉบับ

เชื่อมโยงไปยังหลักฐานที่เกี่ยวข้อง

04 — Document Actions

เปิด PDF สำหรับตรวจทาน

แสดงสถานะ Quality Gate

พิมพ์ PDF ต้นฉบับ

ดาวน์โหลด PDF ต้นฉบับ

หมายเหตุ: ภาพต้นแบบมีช่องรหัสผ่านและปุ่ม SFX Archive ด้วย แต่ PRD ปัจจุบันยังไม่ได้กำหนดให้ Dashboard Read-only ทำหน้าที่สร้าง SFX หรือกำหนดรหัสผ่านให้ไฟล์ PDF โดยตรง จึงให้คงตำแหน่งองค์ประกอบเหล่านี้ตามภาพไว้ในแบบ UI แต่ยังไม่กำหนดให้เชื่อมต่อการสร้างไฟล์จริงจนกว่าจะยืนยันขอบเขตการทำงาน 
PROJECT_EVIDENCE_3COL_PROTOTYPE.html
01-PRD.md

8. UI Component States

ทุกองค์ประกอบที่มีการโต้ตอบต้องรองรับสถานะต่อไปนี้

State

	

ข้อกำหนด




Default

	

สีเทาตาม Theme




Hover

	

เพิ่มความสว่างของพื้นหลังหรือเส้นขอบ




Active

	

ใช้สีเทาเงินแสดงรายการที่เลือก




Focus

	

มี Focus Ring ที่มองเห็นชัด




Disabled

	

สีเทาหม่นและไม่สามารถดำเนินการได้




Loading

	

แสดงสถานะกำลังทำงาน




Empty

	

แจ้งว่ายังไม่มีข้อมูล




Error

	

แสดงข้อความอธิบายข้อผิดพลาด

การออกแบบต้องไม่ใช้สีเพียงอย่างเดียวในการแยกสถานะสำเร็จ คำเตือน หรือข้อผิดพลาด แต่ต้องมีข้อความหรือสัญลักษณ์ประกอบด้วย

9. ขอบเขตการพัฒนาและการเชื่อมต่อ

ต้องแยกหน้าที่ของ Dashboard ออกจากระบบประมวลผลหลัก เพื่อไม่ให้การแก้ไข UI เปลี่ยนแปลงข้อมูลหลักฐานหรือพฤติกรรมของ Pipeline เดิม

ส่วนงาน

	

ความรับผิดชอบ




StackBlitz UI

	

Layout, Theme, Responsive และการโต้ตอบของหน้าจอ




PDF Viewer

	

อ่านและแสดงไฟล์ PDF จริง




Python Pipeline

	

ประมวลผลภาพแชทและสลิป




OUTPUT

	

เก็บ PDF, Excel, JSON และเอกสารรับรอง




Quality Gate

	

ตรวจสอบความครบถ้วนและความถูกต้อง




Dashboard Data Layer

	

อ่านข้อมูลผลลัพธ์และส่งให้ UI แสดงผล

เอกสาร Architecture ปัจจุบันระบุว่า Dashboard เป็น Local Read-only และไม่มี HTTP API ภายนอกในเฟสนี้ จึงยังไม่ควรสมมติว่าหน้าเว็บบน StackBlitz สามารถสั่ง Python หรืออ่าน Folder_Out บนเครื่อง Windows ได้โดยตรง 
03-ARCHITECTURE.md
03-ARCHITECTURE.md

10. Acceptance Criteria — เกณฑ์รับงาน UI

UI Acceptance Checklist

0 / 12