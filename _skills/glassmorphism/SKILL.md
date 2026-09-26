---
name: glassmorphism
description: Use when building, styling, or refactoring UI components to have Apple-grade frosted glassmorphism that is highly translucent, reveals ambient backgrounds, and automatically handles nested glass-on-glass hierarchy without user micromanagement.
---

# Glassmorphism Visual Standard Skill

> **SSOT Reference:** `Glassmorphism Visual Contract.md` & `Glassmorphism-Visual-Contract (1).html`  
> **Source Engine:** Standalone Browser Glassmorphism Visual Contract Factory V8 Base  
> **Gatekeeper Mode:** `FORCED` (Guarantees zero regression into flat SaaS / clean card UI)  
> **Core Principle:** Apply `.glass` or `.glass-card` to ANY component. The engine automatically handles outer vs inner stacking without opacity buildup, GPU lag, or murky blur.

---

## 1. Authoritative CSS Engine (SSOT)

Embed this exact CSS into your application stylesheet or `<style>` block:

```css
/* ==========================================================================
   GLASSMORPHISM SSOT ENGINE (Apple Frosted Glass + Auto-Context Hierarchy)
   ========================================================================== */

/* 1. กระจกทั่วไป (แผงใหญ่ / ชั้นนอก / คอมโพเนนต์เดี่ยว) */
.glass-card,
.glass {
  width: auto;
  min-height: auto;
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(26px) saturate(170%);
  -webkit-backdrop-filter: blur(26px) saturate(170%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 
    0 15px 44px rgba(0, 0, 0, 0.24), 
    inset 0 1px 0 rgba(255, 255, 255, 0.25);
  border-radius: inherit;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
}

/* 2. ถ้ากระจกถูกจับไปวาง "ซ้อนในกระจก" อีกที (ระบบจัดการเอง 100% ผู้ใช้ไม่ต้องแตะ) */
.glass-card .glass-card,
.glass .glass,
.glass-card .glass,
.glass .glass-card {
  background: rgba(255, 255, 255, 0.04);       /* ⚡ ดรอปเนื้อสีลงเองอัตโนมัติ แสงจึงทะลุได้เท่าเดิม ไม่ตัน! */
  backdrop-filter: none;                        /* ⚡ ไม่เบลอซ้ำสอง เพื่อให้มองทะลุเห็นพื้นหลังคมชัด และเครื่องไม่หน่วง */
  -webkit-backdrop-filter: none;
  border: 1px solid rgba(255, 255, 255, 0.28);  /* ⚡ สันขอบสะท้อนแสงคมขึ้นมาเอง เพื่อแยกชิ้นให้เด่นตา */
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.38);
}

/* Interactive States */
.glass-hover:hover,
.glass button:hover,
.glass.interactive:hover,
.glass-card:hover {
  background: rgba(255, 255, 255, 0.20);
  border-color: rgba(255, 255, 255, 0.36);
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.45);
}

.glass-card .glass-card:hover,
.glass .glass:hover,
.glass .glass-hover:hover,
.glass .glass.interactive:hover {
  background: rgba(255, 255, 255, 0.09);
  border-color: rgba(255, 255, 255, 0.42);
}

/* Fallback for legacy browsers without backdrop-filter support */
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass-card, .glass {
    background: rgba(15, 23, 42, 0.88);
  }
  .glass-card .glass-card, .glass .glass {
    background: rgba(30, 41, 59, 0.75);
  }
}
```

---

## 2. Fit-to-Screen Foundation (No Page Scroll)

Glassmorphism requires strict layout containment so blur buffers do not cause layout thrashing or unwanted page scrollbars:

```css
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  overflow: hidden;
  font-family: 'Sarabun', Inter, system-ui, sans-serif;
  color: #FFFFFF;
}

/* Ambient Background Layer: Essential for Glass to blur and shine through */
body {
  background-color: #0F172A; /* Deep Slate Base */
  background-image: 
    radial-gradient(at 10% 15%, rgba(0, 161, 228, 0.22) 0px, transparent 55%),
    radial-gradient(at 90% 85%, rgba(56, 189, 248, 0.18) 0px, transparent 55%),
    radial-gradient(at 50% 50%, rgba(30, 41, 59, 0.6) 0px, transparent 80%);
  background-attachment: fixed;
}

.app-shell {
  width: 100vw;
  height: 100dvh;
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  overflow: hidden;
}

/* All flex/grid children must use min-height: 0 to prevent overflow */
.workspace-grid {
  min-height: 0;
  display: grid;
  grid-template-columns: 28fr 44fr 28fr;
  gap: 14px;
  padding: 14px;
  overflow: hidden;
}

.panel-scrollable {
  min-height: 0;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
}
```

---

## 3. Style Presets Registry (From Standalone Factory)

The factory defines 25 presets categorized into 5 families. The primary preset is:

### Glassmorphism (Apple / Frosted Glass - Primary Standard)
- `surface`: `#ffffff`, `surfaceOpacity`: `0.18` (or `0.14` base)
- `blur`: `26px`, `saturate`: `170%`
- `border`: `#ffffff`, `borderOpacity`: `0.32`, `borderWidth`: `1px`
- `shadow`: blur `44px`, y `15px`, opacity `0.24`
- `highlight`: edgeOpacity `0.38` (inset rim light)
- `text`: `#f8fbff`, `textOpacity`: `0.96`
- `ambient`: `bgA`: `#7dd3fc`, `bgB`: `#c084fc`, `bgC`: `#0f172a`
- `nestedSurface`: `rgba(255, 255, 255, 0.04)` (Auto-Nested 0.04)

---

## 4. Gatekeeper Component Rules

1. **Card:** ต้องใช้ glass surface (`.glass` หรือ `.glass-card`)
2. **Modal:** ต้องใช้ glass surface ที่เด่นกว่า card
3. **Sidebar / Left Rail:** ต้องใช้ glass surface พร้อม blur
4. **Header / Stepper:** ต้องเป็น translucent sticky glass มองทะลุเห็นพื้นหลังได้
5. **Button:** ต้องมี variant ที่เข้ากับ glass surface พร้อม hover glow
6. **Input / Search:** ต้องมี background โปร่งแสง + focus ring ชัด
7. **Badge:** ต้องมี glass / soft glow variant
8. **Table / List:** ต้องอ่านง่ายบน glass background (ใช้ contrast สีขาว `#FFFFFF` หรือ `#F8FBFF`)
9. **Component หลักทุกตัว:** ต้องไม่หลุดเป็น flat SaaS card ธรรมดา
10. **Auto-Nested Context:** กระจกที่ซ้อนในกระจก (Nested Glass) ต้องดรอปความทึบลงเหลือ 0.04 และปิด backdrop-filter อัตโนมัติ เพื่อป้องกันการซ้อนทับจนทึบแสง

---

## 5. Verification Checklist

- [ ] Every component has `.glass` or `.glass-card` class applied.
- [ ] Nested components (`.glass-card .glass-card`, `.glass .glass`) automatically render lighter (`0.04`) and do not double-blur.
- [ ] Ambient background (mountain silhouette or color mesh gradient) is visibly translucent through all panels.
- [ ] Top rim light (`inset 0 1px 0 rgba(...)`) is visible as a crisp 1px highlight.
- [ ] No page-level vertical or horizontal scrollbars exist (`height: 100dvh; overflow: hidden;`).
