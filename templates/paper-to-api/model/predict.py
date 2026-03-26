"""
=== YOUR CODE GOES HERE ===

Implement two functions:
  1. load_model()  — called once at startup
  2. predict()     — called per request

That's it. The server, Docker, batching, error handling — all handled.
"""

from typing import Any

from app.schemas import PredictRequest, PredictResponse


def load_model(config: dict) -> Any:
    """
    Load your model. Called once when the server starts.

    Args:
        config: The 'model' section from config.yaml

    Returns:
        Your model object (anything — PyTorch model, pipeline, tokenizer, etc.)

    Example:
        model = torch.load(config["weights"], map_location=config["device"])
        model.eval()
        return model
    """
    # --- REPLACE THIS WITH YOUR MODEL LOADING CODE ---
    print(f"TODO: Load your model from {config.get('weights', 'N/A')}")
    print(f"      Device: {config.get('device', 'auto')}")

    # Example for HuggingFace:
    # from transformers import AutoModelForCausalLM, AutoTokenizer
    # tokenizer = AutoTokenizer.from_pretrained(config["weights"])
    # model = AutoModelForCausalLM.from_pretrained(config["weights"])
    # return {"model": model, "tokenizer": tokenizer}

    return None  # ← Replace with your model


def predict(model: Any, request: PredictRequest) -> PredictResponse:
    """
    Run inference. Called for every API request.

    Args:
        model: Whatever you returned from load_model()
        request: The parsed request body (edit schemas.py to change this)

    Returns:
        PredictResponse with your results

    Example:
        tokens = model["tokenizer"](request.input, return_tensors="pt")
        output = model["model"].generate(**tokens, max_length=128)
        text = model["tokenizer"].decode(output[0])
        return PredictResponse(output={"text": text})
    """
    # --- REPLACE THIS WITH YOUR INFERENCE CODE ---
    return PredictResponse(
        output={"message": f"TODO: Run inference on input: {request.input}"}
    )
