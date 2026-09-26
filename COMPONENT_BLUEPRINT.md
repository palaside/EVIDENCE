# 📐 COMPONENT BLUEPRINT (3-TIER HIERARCHY)
## Digital Evidence Master Blueprint

---

## 1. 3-Tier Layering Rules (ห้ามข้ามชั้นเรียก)

```
[ Layer 3: Page Section ]
  ├── HeaderSection (Mode Tabs & Brand)
  ├── InputQueueSection (Left 25%)
  ├── EvidenceStageSection (Middle 50%)
  └── CommandSecuritySection (Right 25%)
       │
       ▼
[ Layer 2: Composite Components ]
  ├── UploadDropzone
  ├── FileQueueList
  ├── MathematicalCanvas (645x890)
  ├── LiquidGlassModal (11-Col Table)
  ├── PasswordLockSwitch
  └── SaveModalDialog
       │
       ▼
[ Layer 1: Primitive Components ]
  ├── BaseButton (.btn-primary, .btn-action, .btn-trash)
  ├── BaseInput (.form-control)
  ├── StatusBadge (.brand-badge, .court-status)
  └── TypographyHeading (.title, .sub)
```

---

## 2. Component Specifications

### C-001: `MathematicalCanvas`
- **Props:** `imageSrc`, `paperW = 645`, `paperH = 890`, `mode = 'SLIP' | 'CHAT'`, `timestamp`
- **Logic:** $Scale = \min(645/W_{orig}, 890/H_{orig})$, $x_{start} = (645 - W_{new})/2$, $y_{start} = (890 - H_{new})/2$
- **Verification:** Center $(X, Y) == (322.5, 445.0)$

### C-002: `LedgerTable11Col`
- **Props:** `records[]`, `totalSum`, `averageSum`
- **Variants:** Standard Row vs Failed Highlight Row (`#fde8e8` + `#C53030`)
- **Footer:** Double Underline on totals
