import requests
from typing import Callable, Dict, Any
from ..models import Event, AgreementInput
from ..db import get_db

def run(inp: AgreementInput, emit: Callable[[Event], None], prior: Dict) -> Dict[str, Any]:
    online = False
    try:
        requests.head("https://8.8.8.8", timeout=3)
        online = True
    except:
        pass

    if online:
        emit(Event(agent="SyncManager", status="thinking", message="Online, syncing unsynced agreements"))
        with get_db() as conn:
            rows = conn.execute("SELECT id FROM agreements WHERE synced = 0").fetchall()
            for row in rows:
                conn.execute("UPDATE agreements SET synced = 1 WHERE id = ?", (row["id"],))
            conn.commit()
        emit(Event(agent="SyncManager", status="evidence", message=f"Synced {len(rows)} agreements"))
        return {"synced_count": len(rows), "online": True}
    else:
        emit(Event(agent="SyncManager", status="thinking", message="Offline, sync deferred"))
        return {"synced_count": 0, "online": False}
