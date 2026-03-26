# paper-to-api

Turn your research model into a production API in 3 minutes.

## Usage

```bash
cp -r templates/paper-to-api my-project
cd my-project

# 1. Drop your model code into model/
# 2. Edit model/predict.py — implement the `predict()` function
# 3. Run:
make serve        # local dev server at http://localhost:8000
make docker       # build container
make deploy       # deploy with docker-compose (GPU support)
make bench        # load test your endpoint
```

## What's Inside

```
paper-to-api/
├── Makefile              # One command for everything
├── Dockerfile            # Multi-stage, optimized for ML
├── docker-compose.yml    # GPU-enabled deployment
├── requirements.txt      # Pin your deps
├── config.yaml           # All knobs in one place
├── app/
│   ├── main.py           # FastAPI server (don't touch unless you need to)
│   ├── middleware.py      # CORS, logging, error handling
│   └── schemas.py        # Request/response models
├── model/
│   ├── __init__.py
│   ├── predict.py        # ← YOUR CODE GOES HERE
│   └── download.py       # Model weight management
├── scripts/
│   ├── bench.py          # Load testing with locust
│   └── health_check.py   # Liveness + readiness probes
└── tests/
    └── test_api.py       # Smoke tests
```

## The Only File You Need to Edit

`model/predict.py` — implement two functions:

```python
def load_model(config: dict) -> Any:
    """Called once at startup. Return your model."""
    pass

def predict(model: Any, request: PredictRequest) -> PredictResponse:
    """Called per request. Run inference and return results."""
    pass
```

Everything else is handled.
