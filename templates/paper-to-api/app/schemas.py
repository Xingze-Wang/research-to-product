"""
Request/Response schemas.
Modify these to match your model's input/output format.
"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    """
    Edit this to match your model's input.

    Examples:
      - Text model: add a `text: str` field
      - Image model: add an `image_url: str` or `image_base64: str` field
      - Multi-modal: add whatever you need
    """

    # --- Replace these example fields with your own ---
    input: Any = Field(..., description="Model input. Replace with your schema.")
    parameters: Optional[dict] = Field(
        default=None, description="Optional inference parameters (temperature, top_k, etc.)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "input": "Hello, world!",
                    "parameters": {"max_length": 128},
                }
            ]
        }
    }


class PredictResponse(BaseModel):
    """
    Edit this to match your model's output.
    """

    output: Any = Field(..., description="Model output. Replace with your schema.")
    latency_ms: Optional[float] = Field(
        default=None, description="Inference latency in milliseconds."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "output": {"text": "Generated response here."},
                    "latency_ms": 42.5,
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    status: str
    model_name: str
    model_version: str
    gpu_available: bool
    gpu_name: Optional[str] = None
