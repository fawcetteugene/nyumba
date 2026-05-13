# nyumba

# Nyumba – PeaceTech Community Trust Ledger

Built during the Andela x OpenAI Codex Accelerator.  
**Offline-first | Anonymous witnesses | Conflict intelligence**

## Repository

GitHub Repository:

[github.com/fawcetteugene/nyumba.git](https://github.com/fawcetteugene/nyumba.git)

Clone the repository:

```bash
git clone https://github.com/fawcetteugene/nyumba.git
cd nyumba
```

---

## Problem

In many conflict-affected or low-connectivity regions, verbal agreements and mediation outcomes are easily lost, disputed, or manipulated. Nyumba creates a secure, community-backed trust ledger that continues working even without internet access.

The platform is designed for local peace committees, village elders, mediators, and humanitarian field teams operating in remote environments.

---

## Features

- ✅ **Offline-first architecture** – Works without internet using local storage and queued synchronization
- ✅ **Anonymous witnesses** – No names, emails, or IP tracking; random aliases preserve privacy
- ✅ **Encrypted local storage** – Agreements encrypted using Fernet before storage
- ✅ **Community verification** – Agreements become trusted after multiple witness confirmations
- ✅ **Live agent workflow** – Visual pipeline showing AgreementRecorder → ConflictIntelligence → PeaceReceiptGenerator → SyncManager
- ✅ **Conflict intelligence** – Automatic risk scoring and recurring topic detection
- ✅ **Peace receipts** – QR-code-based proof of verified agreements
- ✅ **CLI + Web UI** – Operates fully from terminal or browser
- ✅ **Progressive Web App (PWA)** – Cached locally for offline browser access

---

# Installation

## Create virtual environment

```bash
python -m venv .venv
```

## Activate environment

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

## Install dependencies

```bash
pip install -e .
```

---

# Running Nyumba

## Start the local server

```bash
python -m src.nyumba.server
```

Then open:

```text
http://localhost:8765
```

The web interface will continue functioning offline after the first load because the Service Worker caches the application locally.

---

# Offline Usage

Nyumba is designed for unstable or nonexistent internet environments.

## What works offline

- Creating agreements
- Viewing cached UI
- Witness verification
- Local encrypted storage
- Queueing unsynced agreements
- Generating local receipts

## What syncs later

When internet connectivity returns:

- Unsynced agreements upload automatically
- Verification records synchronize
- Conflict analytics update
- Shared ledgers merge

---

# CLI Usage

## Add agreement

```bash
nyumba add "Share the fishing net every Tuesday" "Lake Kivu" "Jean,Marie"
```

Example output:

```text
Agreement added successfully!
```

---

## Witness an agreement

Run this command three times using different aliases:

```bash
nyumba witness <agreement-id> --yes
```

After the third confirmation, the agreement becomes community verified.

---

## Generate peace receipt

```bash
nyumba receipt <agreement-id>
```

This generates:

- QR verification receipt
- SMS-ready confirmation text
- Verification metadata

---

## Alternative CLI execution

If the `nyumba` command is unavailable:

```bash
python -m src.nyumba.cli <command>
```

---

# Web UI Usage

## 1. Create Agreement

Fill in:

- Agreement text
- Location
- Participants

The live agent graph animates as the workflow executes.

---

## 2. Witness Agreement

1. Copy the Agreement ID from the event log
2. Paste it into the witness section
3. Vote "Yes"

After three successful witness confirmations, the agreement becomes verified.

---

## 3. Generate Receipt

Enter the verified Agreement ID and click:

```text
Generate QR
```

A QR peace receipt appears for printing, scanning, or SMS sharing.

---

## 4. Offline Test

To verify offline support:

1. Open the app once while online
2. Disable Wi-Fi or internet
3. Reload the browser
4. Create agreements normally
5. Re-enable internet
6. Click:

```text
Sync Queued Agreements
```

Queued records automatically synchronize.

---

# Example Real CLI Session

```bash
(.venv) fawcett@sv2320:~/Desktop/CodexProject/nyumba$ python -m src.nyumba.cli add "Share the fishing net every Tuesday" "Lake Kivu" "Jean,Marie"
```

Observed workflow:

- Agreement stored successfully
- Conflict analysis completed
- Risk score generated
- Receipt generation attempted
- SyncManager synchronized local agreements

Example agreement ID:

```text
3c851513-332e-43e2-84d0-27df9f10740a
```

---

# Project Structure

```text
nyumba/
├── src/nyumba/
│   ├── agents/
│   │   ├── agreement_recorder.py
│   │   ├── conflict_intelligence.py
│   │   ├── peace_receipt_generator.py
│   │   ├── sync_manager.py
│   │   └── witness_verifier.py
│   │
│   ├── orchestrator.py
│   ├── server.py
│   ├── cli.py
│   ├── db.py
│   ├── encryption.py
│   ├── models.py
│   └── utils.py
│
├── web/
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── sw.js
│
├── tests/
├── CAPSTONE_SPEC.md
├── AGENTS.md
├── README.md
└── pyproject.toml
```

---

# Built with Codex IDE

Codex generated:

- Multi-agent orchestration
- FastAPI backend
- SSE streaming events
- CLI workflow
- Offline-first web application
- Service Worker caching
- Agreement pipelines
- QR receipt workflows

Human-designed decisions included:

- Peace workflow structure
- Agent responsibilities
- Event architecture
- Encryption model
- Offline queue design
- UX language and verification flow

---

# Future Improvements

- Bluetooth peer-to-peer synchronization
- Local mesh networking
- Mobile app (React Native)
- GPT-4.1 conflict pattern analysis
- Swahili, French, and Arabic localization
- Community moderation dashboards
- Disaster-response deployment kits

---

# License

MIT License
