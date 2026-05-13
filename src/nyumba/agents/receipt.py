import time
import json
import qrcode
from pathlib import Path
from typing import Callable, Dict, Any
from ..models import Event, AgreementInput
from ..db import get_agreement, count_yes_votes
from ..crypto_utils import get_or_create_key, decrypt_text

def generate_receipt(agreement_id: str) -> Dict[str, Any]:
    agreement = get_agreement(agreement_id)
    if not agreement:
        return {"error": "agreement not found"}
    if not agreement["verified"]:
        return {"error": "agreement not verified"}

    fernet = get_or_create_key()
    blob = json.loads(agreement["encrypted_blob"])
    text = decrypt_text(blob["text"], fernet)
    participants = decrypt_text(blob["participants"], fernet)

    yes_votes = count_yes_votes(agreement_id)

    from ..db import get_db
    with get_db() as conn:
        row = conn.execute("SELECT risk_score FROM conflict_reports WHERE agreement_id = ? OR agreement_id IS NULL ORDER BY created_at DESC LIMIT 1", (agreement_id,)).fetchone()
        risk_score = row["risk_score"] if row else 0

    receipt_text = f"""NYUMBA PEACE RECEIPT
ID: {agreement_id}
Date: {time.ctime(agreement["created_at"])}
Location: {agreement["location"]}
Agreement: {text}
Witnesses: {yes_votes}/3 verified
Risk score: {risk_score}
"""
    sms_text = f"Nyumba: {text[:80]}... ID:{agreement_id[:8]}"
    qr_dir = Path.home() / ".nyumba" / "receipts"
    qr_dir.mkdir(parents=True, exist_ok=True)
    qr_path = qr_dir / f"{agreement_id}.png"
    qr = qrcode.make(receipt_text)
    qr.save(str(qr_path))

    return {
        "qr_path": str(qr_path),
        "sms_text": sms_text,
        "receipt_text": receipt_text
    }

def run(inp: AgreementInput, emit: Callable[[Event], None], prior: Dict) -> Dict[str, Any]:
    agreement_id = prior.get("agreement_id")
    if not agreement_id:
        emit(Event(agent="PeaceReceiptGenerator", status="failed", message="No agreement ID"))
        return {"error": "no agreement id"}
    result = generate_receipt(agreement_id)
    if "error" in result:
        emit(Event(agent="PeaceReceiptGenerator", status="failed", message=result["error"]))
    else:
        emit(Event(agent="PeaceReceiptGenerator", status="evidence", message="Receipt generated", evidence=[result["qr_path"]]))
    return result
