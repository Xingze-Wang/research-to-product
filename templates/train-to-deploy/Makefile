.PHONY: train export deploy cost test clean

# ============================================================
# train-to-deploy — Makefile
# ============================================================

CONFIG_DIR ?= config
NUM_GPUS ?= $(shell python -c "import torch; print(torch.cuda.device_count())" 2>/dev/null || echo 1)

# --- Training ---
train:
	@echo "Training with $(NUM_GPUS) GPU(s)"
ifeq ($(shell test $(NUM_GPUS) -gt 1 && echo yes),yes)
	torchrun --nproc_per_node=$(NUM_GPUS) src/train.py --config $(CONFIG_DIR)/train.yaml
else
	python src/train.py --config $(CONFIG_DIR)/train.yaml
endif

train-resume:
	python src/train.py --config $(CONFIG_DIR)/train.yaml --resume

# --- Export ---
export:
	python src/export.py --config $(CONFIG_DIR)/export.yaml
	@echo "Exported models in outputs/exported/"

# --- Evaluation ---
eval:
	python src/evaluate.py --config $(CONFIG_DIR)/train.yaml

# --- Deployment ---
deploy-build:
	docker build -f deploy/Dockerfile.inference -t model-inference:latest .

deploy:
	kubectl apply -f deploy/k8s/

# --- Cost Analysis ---
cost:
	python scripts/cost_calculator.py

# --- Testing ---
test:
	pytest tests/ -v

clean:
	rm -rf outputs/ __pycache__ .pytest_cache
