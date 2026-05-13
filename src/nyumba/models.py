import time
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class Event:
    agent: str
    status: str   # started, thinking, evidence, completed, failed
    message: str
    evidence: Optional[List[str]] = None
    ts: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "agent": self.agent,
            "status": self.status,
            "message": self.message,
            "evidence": self.evidence or [],
            "ts": self.ts
        }

@dataclass
class AgreementInput:
    text: str
    location: str
    participants: List[str]
    timestamp: float = field(default_factory=time.time)
