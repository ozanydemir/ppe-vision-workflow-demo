from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.evaluator import evaluate_frame
from app.models import FrameRequest, FrameResult

app = FastAPI(title="PPE Vision Workflow Demo", version="0.1.0")
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "data": "synthetic", "identity": "disabled"}


@app.post("/evaluate", response_model=FrameResult)
def evaluate(frame: FrameRequest) -> FrameResult:
    return evaluate_frame(frame)
