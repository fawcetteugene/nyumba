import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import Iterator

from .models import AgreementInput
from .orchestrator import orchestrate, Event
from .agents.witness import run as witness_run
from .agents.intelligence import compute_risk_and_topics
from .agents.receipt import generate_receipt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8765", "http://127.0.0.1:8765"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def healthz():
    return {"ok": True}

@app.get("/api/risk")
async def get_risk():
    result = compute_risk_and_topics()
    return {"risk_score": result["risk_score"], "top_topics": result["top_topics"]}

@app.post("/api/run")
async def run_agent(request: Request):
    body = await request.json()
    text = body.get("text")
    location = body.get("location")
    participants = body.get("participants", [])
    if not text or not location:
        raise HTTPException(400, "Missing text or location")

    inp = AgreementInput(text=text, location=location, participants=participants)

    async def event_generator():
        for event in orchestrate(inp):
            yield f"event: progress\ndata: {json.dumps(event.to_dict())}\n\n"
        yield f"event: done\ndata: {{\"status\": \"finished\"}}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/api/witness")
async def witness_vote(request: Request):
    body = await request.json()
    agreement_id = body.get("agreement_id")
    vote = body.get("vote")
    note = body.get("note", "")
    if not agreement_id or vote is None:
        raise HTTPException(400, "Missing agreement_id or vote")

    async def event_generator():
        events = []
        def emit(ev: Event):
            events.append(ev)
        result = witness_run(agreement_id, vote, note, emit)
        for ev in events:
            yield f"event: progress\ndata: {json.dumps(ev.to_dict())}\n\n"
        yield f"event: done\ndata: {json.dumps(result)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/receipt/{agreement_id}")
async def get_receipt(agreement_id: str):
    result = generate_receipt(agreement_id)
    if "error" in result:
        raise HTTPException(404, result["error"])
    if Path(result["qr_path"]).exists():
        return FileResponse(result["qr_path"])
    raise HTTPException(404, "QR file not found")

@app.get("/")
async def root():
    index_path = Path(__file__).parent.parent.parent / "web" / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text())
    return HTMLResponse(content="<h1>Nyumba</h1><p>Web UI not found.</p>")

# Add this block to allow direct execution
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
