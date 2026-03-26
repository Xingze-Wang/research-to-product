# train-to-deploy

From single-GPU training script to production deployment pipeline.

## Usage

```bash
cp -r templates/train-to-deploy my-project
cd my-project

# 1. Edit config/train.yaml — point to your data and model
# 2. Edit src/model.py — define your model architecture
# 3. Run:
make train          # single or multi-GPU training
make export         # export to ONNX / TensorRT
make deploy         # deploy as K8s service
make cost           # estimate your inference cost per 1M calls
```

## What's Inside

```
train-to-deploy/
├── Makefile
├── config/
│   ├── train.yaml          # Training hyperparameters
│   ├── export.yaml         # Model export settings
│   └── deploy.yaml         # Deployment config
├── src/
│   ├── model.py            # ← YOUR MODEL HERE
│   ├── dataset.py          # ← YOUR DATA LOADING HERE
│   ├── train.py            # Training loop (DDP/FSDP ready)
│   ├── export.py           # ONNX + TensorRT export
│   └── evaluate.py         # Eval + benchmarking
├── deploy/
│   ├── Dockerfile.inference
│   ├── k8s/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── hpa.yaml        # Autoscaling
│   └── triton/              # Optional: Triton Inference Server
│       └── config.pbtxt
├── scripts/
│   └── cost_calculator.py  # $/1M requests estimator
└── tests/
    └── test_train.py
```
