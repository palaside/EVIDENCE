---
name: ask-junior
description: Use when needing quick chat responses, summarizing text, chain-of-thought logical verification, or rapid conversational assistance powered by local deepseek-r1:8b.
---

# SKILL: ask-junior — Fast Chat & Summarizer (deepseek-r1:8b)

## Role & Profile
- **ตำแหน่ง:** จูเนียร์ (Fast Conversational Assistant, Summarizer & CoT Reasoner)
- **เครื่องยนต์ประมวลผล:** `deepseek-r1:8b` (4.87 GB) / Fallback: `qwen2.5:latest` (4.36 GB) บน Central Local Brain (`http://127.0.0.1:11434`)
- **ความเชี่ยวชาญ:** แชทตอบไว, สรุปข้อความยาวให้กระชับ, คิดหาเหตุผลแบบเป็นขั้นเป็นตอน (Chain-of-Thought), แปลภาษาและจัดหมวดหมู่ข้อมูล

## When to Use
- ต้องการแชทบอทตอบคำถามทันใจใน 1-3 วินาที
- สรุปบันทึกการประชุม, สรุปเนื้อหาเอกสาร, หรือสรุป Log
- ช่วยตรวจทานตรรกะเบื้องต้น (Sanity Check / Brainstorming)
- ตอบคำถามทั่วไปในแชทบอทหน้าบ้าน

## Quick Invocation (วิธีเรียกใช้งาน)
```powershell
python F:\Project\tools\ask-team.py junior "สรุปเนื้อหาสำคัญของรายงานฉบับนี้เป็น 3 ข้อย่อย"
```
