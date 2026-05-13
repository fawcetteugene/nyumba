import time
import random
from typing import Callable, Dict, Any, Optional
from ..models import Event
from ..db import save_witness_vote, count_yes_votes, mark_verified, get_agreement

def run(agreement_id: str, vote: bool, note: str = "", emit: Optional[Callable[[Event], None]] = None) -> Dict[str, Any]:
    if emit is None:
        def emit(e): pass

    emit(Event(agent="WitnessValidator", status="started", message=f"Processing vote for {agreement_id}"))

    agreement = get_agreement(agreement_id)
    if not agreement:
        emit(Event(agent="WitnessValidator", status="failed", message="Agreement not found"))
        return {"error": "agreement not found"}

    alias = f"Witness_{random.randint(100000, 999999)}"
    vote_int = 1 if vote else 0

    save_witness_vote(agreement_id, vote_int, note, alias, time.time())
    emit(Event(agent="WitnessValidator", status="evidence", message=f"Vote recorded from {alias}", evidence=[agreement_id, str(vote)]))

    total_yes = count_yes_votes(agreement_id)
    verified_now = False
    if total_yes >= 3 and not agreement["verified"]:
        mark_verified(agreement_id)
        verified_now = True
        emit(Event(agent="WitnessValidator", status="completed", message=f"Agreement verified! Total yes votes: {total_yes}", evidence=[agreement_id]))

    emit(Event(agent="WitnessValidator", status="completed", message=f"Vote accepted. Total yes: {total_yes}"))

    return {"total_yes_votes": total_yes, "verified_now": verified_now}
