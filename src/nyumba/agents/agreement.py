import uuid
import time
from typing import Callable, Dict, Any
from ..orchestrator import Event, AgreementInput
from ..db import save_agreement, get_agreement
from ..crypto_utils import get_or_create_key, encrypt_text

def run(inp: AgreementInput, emit: Callable[[Event], None], prior: Dict) -> Dict[str, Any]:
    agreement_id = str(uuid.uuid4())
    fernet = get_or_create_key()

    # Encrypt the agreement text and participants
    text_encrypted = encrypt_text(inp.text, fernet)
    participants_encrypted = encrypt_text(",".join(inp.participants), fernet)

    # Store in DB (we store the encrypted blob as a JSON-like string)
    # For simplicity, store as JSON: {text: encrypted, participants: encrypted}
    import json
    encrypted_blob = json.dumps({
        "text": text_encrypted,
        "participants": participants_encrypted
    })

    save_agreement(
        id=agreement_id,
        encrypted_blob=encrypted_blob,
        location=inp.location,
        participants=",".join(inp.participants),  # plain for display? Actually we store plain only for indexing, we'll keep plain but in production maybe encrypt. For MVP, we store location and participants in plain for search.
        created_at=inp.timestamp,
        verified=0,
        synced=0
    )

    emit(Event(
        agent="AgreementRecorder",
        status="evidence",
        message=f"Stored agreement {agreement_id}",
        evidence=[agreement_id, inp.text[:50] + "..."]
    ))

    # Also we could store the actual encrypted blob in a separate field? The above is fine.
    return {"agreement_id": agreement_id, "location": inp.location, "status": "stored"}
