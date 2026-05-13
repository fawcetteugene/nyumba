# Nyumba Agents

## AgreementRecorder
Encrypts and stores a new agreement in local SQLite. Emits the agreement ID.

## ConflictIntelligence
Scans all agreements and witness votes, computes a risk score (0–10), and extracts recurring topics via keyword frequency.

## PeaceReceiptGenerator
For a verified agreement, generates a human‑readable receipt, a SMS‑truncated version, and a QR code image (PNG).

## SyncManager
Checks network connectivity; when online, marks unsynced agreements as synced (stub for future remote sync).

## WitnessValidator (standalone, not in main pipeline)
Accepts witness votes (yes/no + note) for an agreement. After 3 yes votes, marks the agreement as community verified.
