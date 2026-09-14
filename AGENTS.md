# glass-hub/AGENTS.md — กฎคุมเอเจนต์ของ Hub (OpenCode อ่านไฟล์นี้ก่อนเสมอ)

> SSOT: `commands.yaml` (registry) + `hosts.json` (โฮสต์ว่างได้) + `opencode.json` (permission/agents/mcp)
> Constitution หลัก: ใช้ชุดสมอง Universal Brain Set ที่แนบ (root `F:\Project\AGENTS.md`) ทุกข้อมีผลกับ Hub นี้ด้วย

## วิธีทำงาน (บังคับตามชุดที่แนบ)

## ความจำ + ซื่อสัตย์ (บังคับ)
- เปิดงาน/เปิดแชทใหม่ทุกครั้ง: รัน `py tools/understand.py scan` ก่อน (สกิล `skills/understand/SKILL.md` แนว Understand-Anything) แล้วอ่าน `memory/behavior.json` + `memory/mistakes.md`
- พฤติกรรมสั่งซ้ำ ≥3 ครั้ง → บันทึกเป็น preference ใน behavior.json ครั้งต่อไปทำอัตโนมัติ
- ซื่อสัตย์: ไม่รู้บอกไม่รู้ ห้ามเดาแล้วอ้างว่าจริง ห้ามแต่งผลรัน/ผลเทส
- กฎเหล็กห้ามละเมิดเด็ดขาด (Strict Zero-Guessing / Zero-Hallucination): ห้ามเดา/มโนชื่อธนาคาร ชื่อบุคคล ตัวเลข หรือข้อมูลหลักฐานดิจิทัล/สลิปการเงินเองโดยเด็ดขาด การอนุมานชื่อเอง (เช่น เดาคำเพี้ยน Alovdsuma เป็น CIMB) ถือเป็นความผิดร้ายแรงขั้นละเมิดกฎความซื่อสัตย์ ต้องอ่านจากข้อความจริง รหัส EMVCo QR หรือเลขบัญชีคู่สัญญาที่พิสูจน์แล้ว (SSOT Ground Truth Binding) เท่านั้น หากอ่านไม่ออกให้บอกอ่านไม่ออกหรือใช้ค่าดิบ ห้ามแต่งเติมเด็ดขาด
- ทุกคำตอบต้องมีโค้ดหรือไฟล์อ้างอิง (`path:line` หรือผลรันจริง) ห้ามมโน ไม่มีหลักฐานให้บอกว่าไม่มี
- ไม่เข้าข้างผู้ใช้: ผิดบอกผิด ถูกบอกถูก ตรงไปตรงมา ไม่ประจบ
- ผู้ใช้ไม่เก่งโค้ด เอเจนต์ต้องรู้ใจ: ทุกคำตอบเสนอทางเลือกที่ดีที่สุด **2-3 ข้อพร้อมคำแนะนำ** ในครั้งเดียว
- สั่งแล้วต้องจบ: ได้รับคำสั่ง = ทำให้เสร็จครบ ห้ามถามพ่ำเพื่อทีละก้อนอิฐ (ห้าม question tool พร่ำเพรื่อ — ถามเฉพาะจุดที่ไปต่อไม่ได้จริงๆ)
- ผิดพลาดทุกครั้ง → เขียนลง `mistakes.md` ทันที (วัน/สิ่งที่สั่ง/สาเหตุจริง/วิธีแก้) ห้ามลบ อ่านทวนก่อนงานคล้ายกัน
- จบการสนทนาทุกครั้ง → รัน `py tools/save-state.py --quiet` เงียบหลังบ้าน (สกิล `skills/save/SKILL.md` อ้างอิง SAVE.md) แบ็กอัพ 4 ไฟล์ลง `state/`
- DNA: Inspect Before Act (ห้ามเดา path/API), ตรวจ Exit Code/Stderr ทุกคำสั่ง, TDD, แยกโมดูล, Gatekeeping ปฏิเสธโค้ดเสี่ยง/Memory Leak/Technical Debt
- Secrets: อ่านเฉพาะชื่อ Key ใน `.env` ห้ามโชว์ค่า / ห้าม hardcode secret
- API Key: รับผ่านช่องกรอกใน Hub → เขียนลง `.env` ผ่าน `POST /api/key` (allowlist 3 ชื่อ) → โค้ดอ่านจาก env เท่านั้น ห้ามดึงตรง/ฝังใน HTML
- Terminal: ห้าม `rm -rf` วงกว้าง, ห้าม force push, ห้ามล้าง DB จริง, ล้มเหลวไม่รันซ้ำเกิน 2 ครั้ง
- Loop: `/constitution → /clarify → /checklist → /analyze → /converge` + Auto Gap-Closing (ขาด test/validation/loading/error state → สร้างเติมเองก่อนส่ง)
- Self-Review 6 ข้อก่อนส่งมอบทุกครั้ง: Scope ตรง, Syntax ผ่าน, Tests ผ่าน, No Regression, Security, Clean
- 10 Mastery: Grilling ก่อนโค้ด, กำหนด Visual Language/Tokens, WCAG 2.1 AA, 60 FPS/ไม่ re-render มั่ว, Functional Motion, Anti-AI-Slop, Pixel-Perfect (Focus Ring/Empty/Error states), แก้ที่ต้นตอแบบ Call-Graph

## เพิ่มโปรเจกต์ใหม่ทีละตัว (ห้ามลัด)
1. อ่าน `commands.yaml` ส่วน GUARD header ก่อน
2. เติม **1 entry** ใต้ `tools:` (id kebab-case ไม่ซ้ำ, label, icon, kind `iframe|panel`, target, keywords, hint)
3. ถ้าโฮสต์จริงยังไม่มี: ใช้ `panel:<id>` หรือ path ไฟล์ ห้ามเดา localhost
4. Mirror `REGISTRY` + เพิ่ม 1 บรรทัดใน `FIXED` ของ `dashboard-hub.html`
5. ตรวจ: ids ใน YAML = ids ใน REGISTRY, `node --check` ผ่าน

## คำแชทที่เป็นโปรเจกต์ → เดิน SDLC (บังคับ)
- เมื่อคำในแชทส่อเป็นงานสร้างใหม่ (เช่น "ทำ/สร้าง/เขียน/เจน + ชื่อระบบ") ให้ถือเป็นโปรเจกต์แล้วเดิน
  กระบวนการ `vibe-code-sdlc-workflow` 8 ขั้น: 0 Idea → 1 /specify → 2 /plan → 3 /tasks →
  4 /implement → 5 Test & Review → 6 Deploy → 7 Operate แล้วปิดด้วย 5 boosters
  (`/constitution → /clarify → /checklist → /analyze → /converge`)
- แต่ละขั้นฝังสกิลตาม `sdlc-skills.yaml` (สารบัญกลาง ห้ามเรียกนอกบัญชี)
- สกิลสมอง `skills/sdlc/SKILL.md` โหลดอัตโนมัติเมื่อเจองานสร้าง ไม่ต้องพิมพ์เรียก
- กฎด่านรีวิว: `Code_Review` (เร็ว, ทุกรอบ) ก่อน `Code_Review_Quality` (เต็ม 5 มิติ, ก่อน production) ห้ามเรียกซ้อนรอบเดียว

## งานอัตโนมัติ → hotfolder-agent ก่อนเสมอ (ตัวเลือกแรก)

## Notebook คลังสมอง + MCP (บรรณารักษ์)- อีเมล config ผ่านป้าย Notebook ใน Hub → หน้ายืนยัน → เก็บใน `notebook-config.json` (gitignore) ผ่าน `POST /api/notebook`
- ค้นผ่านแชท (`ค้น/หา/find/search`) หรือ MCP `notebook_search`/`notebook_read` (stdio, `tools/notebook-mcp.py`)
- Obsidian ใช้ระบบเดียวกับ Notebook (อีเมลยืนยันเดียวกัน): ป้าย `obvault` ผูก path vault (ว่าง = `memory/` เปิดใน Obsidian ได้เลย) แชท `obsidian X` ค้นเฉพาะโน้ต memory ไม่ต้องสลับ
- Google Drive (toggle ใน Notebook): เปิด/ปิด + folder id เก็บใน `notebook-config.json` แชท `drive X` ค้นผ่าน `GET /api/drive?q=` (คีย์ `GOOGLE_API_KEY` ฝั่ง server เท่านั้น)
- สร้าง index ใหม่เมื่อเพิ่มไฟล์: `py tools/notebook-index.py` · สกิล `skills/librarian/SKILL.md`

## Deploy 6 ที่ (SSOT: deploy.json)

## ลิงก์สกิล GitHub → skill-creator อัตโนมัติ
- ผู้ใช้แปะลิงก์สกิล GitHub ใดๆ = สั่งดึงทันที ไม่ต้องถาม: fetch เนื้อหาลิงก์ → รัน
  `py F:/Project/skill-creator/scripts/extract_skill.py --name <อังกฤษขีดกลาง> --what <ทำอะไร> --triggers <ทริกเกอร์> --when <เงื่อนไข> --steps <ขั้นตอน> --output <ผลลัพธ์> --src <ลิงก์> --out <โฟลเดอร์สกิล>`
  (ดึงแบบส่วนตัวตามแม่แบบ skill-creator ไม่เหมือนคนอื่น) เสร็จแล้วรายงาน path สกิลที่ได้
- Supabase / Vercel / GitHub / Cloudflare Workers / D1 / R2 — ดู `deploy.json` (คำสั่ง + คีย์ที่ต้องใช้)
- คีย์ทุกตัวผ่านช่องกรอก Hub ลง `.env` เท่านั้น · พาเนล 🚀 ใน Hub โชว์ความพร้อมคีย์ก่อนสั่ง deploy
- เรื่องเฝ้าโฟลเดอร์/inbox กฎ routing ประมวลไฟล์อัตโนมัติ รันเงียบพร้อม Windows:
  ใช้ `F:/Project/hotfolder-agent` (SKILL.md + `dashboard/hotfolder-wizard.html` + `scripts/hotfolder.py`) ก่อนคิดวิธีอื่น
- ขั้น deploy/operate ของ SDLC ที่มีงานซ้ำตามเวลา/ไฟล์เข้า ให้ผูก hotfolder rules แทนสคริปต์เฉพาะกิจ

## ข้อห้าม
- ห้ามแตะ entry เดิม, ห้ามแก้ `send/route/openTool`, ห้ามแตะ `dashboard.html` (ของเก่า)
- ห้าม invent host URL — ถามผู้ใช้ครั้งเดียวต่อ session
- ตอบเป็นภาษาไทย กระชับ ตรงประเด็น

## Project Command Hooks (เอเจนต์รันคำสั่งพวกนี้ได้เลยไม่ต้องถาม)
- เจนพอร์ต: `py alloc-port.py <id> "<ชื่อโปรเจกต์>" --kind backend`
- ดูตารางพอร์ต: `py alloc-port.py --list`
- ซ้อมตัวกระตุ้น: `py tools/tick.py --once` (รันจริงเงียบผ่าน tools/run-silent.vbs + install-startup.bat)
- ดูหลักฐานการยิง: `tools/tick.log` (STATE เปลี่ยน + HEARTBEAT ทุก 20 tick)
- ตรวจ JS Hub: `node --check <ไฟล์สคริปต์ที่แยกจาก dashboard-hub.html>`
- ตรวจ JSON: `py -c "import json,pathlib; json.loads(pathlib.Path('<ไฟล์>.json').read_text(encoding='utf-8'))"`
- สแกนคีย์หลุดก่อนทุก commit/PR: `py tools/scan-secrets.py --strict` (ตก = ห้าม merge)
- ห้ามรัน: `rm -rf`, `git push --force`, ล้าง DB, สั่ง `pip install` นอก venv

## Write Scope (ไฟล์ที่เอเจนต์เขียนได้/ห้ามแตะ)
- เขียนได้: `commands.yaml` (เติมท้าย 1 entry), `dashboard-hub.html` (ก้อน REGISTRY/FIXED/PORTS/SDLC), `ports.json` (ผ่าน alloc-port.py เท่านั้น ห้ามแก้เลขมือ), `hosts.json` (เมื่อผู้ใช้ให้ค่าแล้ว), `sdlc-skills.yaml` (แก้ mapping สกิล), `.opencode/agents/*.md`
- ห้ามแตะ: `dashboard.html`, `rail.html`, `python_template/web-dashboard/commands.yaml`, `.env`, `*.bundle`
- ทุกครั้งที่เขียน: อ่านไฟล์จริงก่อน (ห้ามเดา path), แก้ทีละไฟล์, ตรวจ `node --check`/JSON parse ผ่านก่อนส่งมอบ

## สถาปัตยกรรม (หลักการ ไม่ใช่ไฟล์ตายตัว — ปรับได้ตามงาน)
- ดูจากโปรเจกต์ที่จะสร้างก่อนว่าแนวไหน แล้วเลือกโครงให้เหมาะ
- ฟูลสแต็กพื้นฐาน = **Next.js 15 + Tailwind CSS + Java 17 Spring Boot 3** (ความต้องการอันดับ 1, ระดับ Production Ready)
  หมายเหตุ: `Stack/backend` เดิมเป็น NestJS ห้ามรื้อ — กฎนี้ใช้กับงานสร้างใหม่เท่านั้น
- ถ้าไม่ระบุ → ใช้โครงฟูลสแต็กของเราที่ปั้นตอนแรก (`python_template`: frontend Vite → `POST /run backend/main.py` → `route_optimizer.py` core → `outputs/` + DB 4 ตัวเลือก + `scaffold/wizard.html` + `run.bat/run.ps1`) เวลารันยึดแบบสแตนอโลน: รันเอง ทำงานเอง
- ถ้าผู้ใช้บอก "ฟูลสแตค" → ยึด roadmap รูปที่สองเป็นหลักการ (Foundations → Frontend → Backend → Databases → AI Integration → DevOps → Testing → Mastery → Real-World → Growth) ไม่ต้องสร้างไฟล์ย่อยทั้งหมด เลือกเฉพาะชั้นที่งานนั้นต้องใช้

## ลูปเทสต์ (รันบ่อย ลูปไม่เกิน 3 รอบ)
- รันเทสบ่อยทุกครั้งที่แก้โค้ด วิธีเดิมล้มเหลวได้ไม่เกิน **3 รอบ** → รอบที่เกินต้องหาทางแก้แบบอื่น (เปลี่ยนวิธี ไม่ใช่รันคำสั่งเดิมซ้ำ)
- วิธีใหม่ล้มอีกครบ **3 ครั้ง** → หยุดแล้วถามผู้ใช้งาน ห้ามงมต่อเอง

## คำสั่งประจำ: "สร้างระบบ" (Standing Order อันดับหนึ่ง)
- เมื่อผู้ใช้สั่ง "สร้างระบบ" ให้ยึดสแต็กนี้ก่อนเสมอ:
  1. **Autonomous Coding Agent + Live Sandbox** (รัน/ตรวจ/เติมเอง ไม่รอคนกดทีละขั้น)
  2. **Project Scaffolding Wizard / Parametric Configurator** (สร้างตามแบบฟอร์ม ไม่ใช่ไฟล์นิ่ง)
  3. **Design Tokens + Accessibility (WCAG 2.1 AA) + Component Rules** (ความสำคัญอันดับหนึ่งของงานสร้าง)
- จากนั้น **ต้องถามกลับเสมอ**: "สร้างเป็นสแตนอโลนไหม"
- ถ้าตอบใช่ → เสกครบชุด: **Standalone (ดับเบิลคลิกเปิดได้)** + **สคริปต์รัน Windows (`run.bat`/`run.ps1`)** +
  **Autonomous Coding Agent + Live Sandbox** + **หน้าแดชบอร์ดที่เป็น Scaffolding Wizard/Parametric Configurator**
  พร้อม Design Tokens, Accessibility, Component Rules ในตัว
- ทุกชุดสแตนอโลนต้องฝัง **ชุดรันเงียบ** ไปด้วยเสมอ: ก๊อป `tools/tick.py` + `tools/run-silent.vbs` +
  `tools/install-startup.bat` + `tools/uninstall-startup.bat` ลง root ของแพ็กเกจ
  (แก้ path ใน VBS ให้ชี้ tick.py ตำแหน่งใหม่) เพื่อให้รันเงียบพร้อม Windows ได้ทันทีหลังติดตั้ง
