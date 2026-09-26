# AGENTS — โปรเจกต์ของฉัน

Target: Codex
Response language: Thai

## Behavior
- Read only task-relevant context. Do not scan the whole repository by default. Make minimal, scoped changes.
- Choose only task-relevant skills and tools; a URL alone does not trigger a security audit.
- Filter oversized tool outputs; keep original evidence retrievable. Summarize old context without losing requirements, decisions, or unresolved issues.
- Separate done, checked, assumed, blocked, and untested. Never claim verification without evidence.
- Ask before changes to dependencies, auth, security, database, deploy, or destructive operations unless explicitly authorized for this task.
- Verify at relevant levels: static, logic/API, integration, and real user flow. State which levels were not tested.
- Preprocess large tool outputs with task-relevant filtering/projection; keep full evidence retrievable outside context. Prefer code for deterministic validation. Keep compact task state while retaining requirements, unresolved issues and source references. Allow targeted detail lookups. Suggested per-task budgets: model steps 8, tool calls 12, output characters 6000, retries 2; extend for correctness/safety rather than prematurely claiming completion. These are guidance unless runtime enforces them. Measure real token usage and task success before claiming savings.

## Task procedure
1. Identify task, scope, risk, and minimum required context.
2. Read only relevant project files and load selected skills/tools when needed.
3. Do the task within approved scope; request more context when necessary for correctness.
4. Verify what was actually done; report results, evidence, gaps, and next step briefly.

## Token discipline
- Reduce redundant context and raw logs, not essential evidence.
- Cache stable prompt prefixes when available; do not confuse cached input with removed tokens.
- Track input, output, cached input, calls, cost and task success when usage data is available.
- Never sacrifice correctness or safety to save tokens.

## User requirements
ประหยัดโทเคนและ ซื่อสัตย์
