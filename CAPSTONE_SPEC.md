# Nyumba – Community Trust Ledger

## Problem statement
In conflict‑affected regions, disputes escalate because verbal agreements, mediation outcomes, and aid commitments are undocumented, easily manipulated, or lost. Nyumba provides an offline‑first, verifiable, and anonymous system for recording agreements, gathering community witness validation, and detecting conflict patterns.

## Acceptance criteria (achieved)
- [x] A. Multi‑agent orchestrator with AgreementRecorder, ConflictIntelligence, PeaceReceiptGenerator, SyncManager.
- [x] B. Each agent emits typed JSON events (agent, status, message, evidence, ts).
- [x] C. FastAPI server with /api/run (SSE), /api/witness, /api/receipt/{id}, /api/risk, serves web UI.
- [x] D. Single‑file web app (web/index.html) with offline support (Service Worker + IndexedDB) and live agent graph.
- [x] E. CLI commands: `nyumba add`, `nyumba witness`, `nyumba receipt`, `nyumba serve`.

## Architecture sketch
[Agent orchestrator] -> [SQLite (encrypted)] -> [Event bus] -> [SSE] -> [Web UI]

## Out of scope (MVP)
- Full peer‑to‑peer sync (stub implemented)
- Real LLM conflict analysis (keyword‑based)
- End‑to‑end encrypted multi‑user sync

## Reproducibility
Following the workshop prompts in Codex IDE produces an identical working prototype.

## Demo script
1. Start server: `python -m src.nyumba.server`
2. Open browser to localhost:8765
3. Create agreement → agent graph animates
4. Witness 3 times → verification
5. Generate QR receipt
6. Disable network → create agreement → queued
7. Re‑enable network → sync occurs
