import time
import json
from typing import Callable, Dict, Any, Optional
from ..models import Event, AgreementInput
from ..db import get_all_agreements, save_conflict_report
from ..crypto_utils import get_or_create_key, decrypt_text

def count_no_votes(agreement_id: str) -> int:
    from ..db import get_db
    with get_db() as conn:
        row = conn.execute("SELECT COUNT(*) as cnt FROM witness_votes WHERE agreement_id = ? AND vote = 0", (agreement_id,)).fetchone()
        return row["cnt"]

def compute_risk_and_topics(agreement_id: Optional[str] = None) -> Dict[str, Any]:
    agreements = get_all_agreements()
    if agreement_id:
        agreements = [a for a in agreements if a["id"] == agreement_id]

    if not agreements:
        return {"risk_score": 0.0, "top_topics": []}

    total_no_votes = 0
    unverified_count = 0
    all_texts = []
    fernet = get_or_create_key()

    for ag in agreements:
        blob = json.loads(ag["encrypted_blob"])
        text = decrypt_text(blob["text"], fernet)
        all_texts.append(text)
        if not ag["verified"]:
            unverified_count += 1
        no_votes = count_no_votes(ag["id"])
        total_no_votes += no_votes

    total_ag = len(agreements)
    risk_score = (unverified_count * 2 + total_no_votes) / (total_ag + 1) * 10
    risk_score = min(10.0, max(0.0, risk_score))

    stopwords = {"the","and","to","of","a","in","for","on","with","by","at","from","is","it","an","we","will","share","water","land","money"}
    word_counts = {}
    for text in all_texts:
        for word in text.lower().split():
            word = word.strip(".,!?")
            if word not in stopwords and len(word) > 2:
                word_counts[word] = word_counts.get(word, 0) + 1
    top_topics = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_topics_list = [word for word, _ in top_topics]

    save_conflict_report(agreement_id, risk_score, json.dumps(top_topics_list), time.time())

    return {"risk_score": round(risk_score, 1), "top_topics": top_topics_list}

def run(inp: Optional[AgreementInput], emit: Callable[[Event], None], prior: Dict) -> Dict[str, Any]:
    agreement_id = prior.get("agreement_id")
    result = compute_risk_and_topics(agreement_id)
    emit(Event(agent="ConflictIntelligence", status="evidence", message=f"Risk score: {result['risk_score']}", evidence=result['top_topics']))
    return result
