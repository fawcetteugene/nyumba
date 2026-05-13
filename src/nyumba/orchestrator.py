import time
from typing import Iterator, Callable, List, Optional, Dict, Any
from .models import Event, AgreementInput
from .agents import agreement, witness, intelligence, receipt, sync


def orchestrate(inp: AgreementInput) -> Iterator[Event]:
    """Run the agent pipeline and yield events."""
    # Helper to emit events
    events_queue = []
    def emit(ev: Event):
        events_queue.append(ev)

    # Start pipeline
    yield Event(agent="Pipeline", status="started", message="Starting Nyumba workflow")

    # 1. AgreementRecorder
    agent_name = "AgreementRecorder"
    emit(Event(agent=agent_name, status="started", message="Recording agreement"))
    result = agreement.run(inp, emit, {})
    for ev in events_queue:
        yield ev
    events_queue.clear()
    emit(Event(agent=agent_name, status="completed", message="Agreement stored", evidence=[result.get("agreement_id", "")]))
    for ev in events_queue:
        yield ev
    events_queue.clear()

    # 2. ConflictIntelligence
    agent_name = "ConflictIntelligence"
    emit(Event(agent=agent_name, status="started", message="Analyzing conflict patterns"))
    conflict_result = intelligence.run(inp, emit, result)
    for ev in events_queue:
        yield ev
    events_queue.clear()
    emit(Event(agent=agent_name, status="completed", message=f"Risk score: {conflict_result.get('risk_score', 0)}", evidence=conflict_result.get("top_topics", [])))
    for ev in events_queue:
        yield ev
    events_queue.clear()

    # 3. PeaceReceiptGenerator
    agent_name = "PeaceReceiptGenerator"
    if result.get("agreement_id"):
        emit(Event(agent=agent_name, status="started", message="Generating peace receipt"))
        receipt_result = receipt.run(inp, emit, result)
        for ev in events_queue:
            yield ev
        events_queue.clear()
        emit(Event(agent=agent_name, status="completed", message="Receipt ready", evidence=[receipt_result.get("qr_path", "")]))
        for ev in events_queue:
            yield ev
        events_queue.clear()
    else:
        emit(Event(agent=agent_name, status="failed", message="No agreement ID to generate receipt"))
        for ev in events_queue:
            yield ev
        events_queue.clear()

    # 4. SyncManager
    agent_name = "SyncManager"
    emit(Event(agent=agent_name, status="started", message="Syncing if online"))
    sync.run(inp, emit, result)
    for ev in events_queue:
        yield ev
    events_queue.clear()
    emit(Event(agent=agent_name, status="completed", message="Sync check done"))
    for ev in events_queue:
        yield ev
    events_queue.clear()

    # Final pipeline event
    yield Event(agent="Pipeline", status="completed", message="Nyumba workflow finished", evidence=[])
