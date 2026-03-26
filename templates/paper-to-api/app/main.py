"""
FastAPI server for model inference.
You shouldn't need to edit this file. Edit model/predict.py instead.
"""

import time
import asyncio
from contextlib import asynccontextmanager
from typing import Any

import yaml
import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import PredictRequest, PredictResponse, HealthResponse
from app.middleware import add_logging_middleware
from model.predict import load_model, predict


# --- Global state ---
_model: Any = None
_config: dict = {}
_semaphore: asyncio.Semaphore = None


def _load_config() -> dict:
    with open("config.yaml") as f:
        return yaml.safe_load(f)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup, cleanup on shutdown."""
    global _model, _config, _semaphore

    _config = _load_config()
    max_concurrent = _config.get("server", {}).get("max_concurrent", 16)
    _semaphore = asyncio.Semaphore(max_concurrent)

    print(f"Loading model: {_config['model']['name']} v{_config['model']['version']}")
    start = time.time()
    _model = load_model(_config["model"])
    print(f"Model loaded in {time.time() - start:.2f}s")

    yield

    # Cleanup
    del _model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


# --- App ---
app = FastAPI(
    title="Research Model API",
    description="Auto-generated API for model inference. Edit model/predict.py to customize.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
cors_origins = _load_config().get("server", {}).get("cors_origins", ["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_logging_middleware(app)


# --- Routes ---
@app.get("/health", response_model=HealthResponse)
async def health():
    """Liveness check."""
    gpu_available = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if gpu_available else None
    return HealthResponse(
        status="ok",
        model_name=_config["model"]["name"],
        model_version=_config["model"]["version"],
        gpu_available=gpu_available,
        gpu_name=gpu_name,
    )


@app.post("/predict", response_model=PredictResponse)
async def predict_endpoint(request: PredictRequest):
    """Run inference. This is your money endpoint."""
    async with _semaphore:
        try:
            start = time.time()
            result = await asyncio.wait_for(
                asyncio.to_thread(predict, _model, request),
                timeout=_config["model"].get("timeout", 30),
            )
            result.latency_ms = (time.time() - start) * 1000
            return result
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504,
                detail=f"Inference timed out after {_config['model']['timeout']}s",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
