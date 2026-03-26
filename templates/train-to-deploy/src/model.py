"""
=== YOUR MODEL GOES HERE ===

Define your model architecture. The training loop handles the rest.
"""

import torch
import torch.nn as nn


class MyModel(nn.Module):
    """
    Replace this with your actual model.

    Requirements:
      - forward() should return a loss tensor (scalar) during training
      - Or return a dict with a "loss" key

    Example for a simple classifier:
        def forward(self, input_ids, labels=None):
            logits = self.classifier(self.backbone(input_ids))
            if labels is not None:
                return F.cross_entropy(logits, labels)
            return logits
    """

    def __init__(self, config: dict = None):
        super().__init__()
        # --- REPLACE WITH YOUR ARCHITECTURE ---
        self.net = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Linear(256, 10),
        )
        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, x, labels=None, **kwargs):
        logits = self.net(x)
        if labels is not None:
            return self.loss_fn(logits, labels)
        return logits


def build_model(config: dict) -> nn.Module:
    """
    Build model from config. Add your model classes here.
    """
    models = {
        "MyModel": MyModel,
        # Add your models here:
        # "TransformerLM": TransformerLM,
    }

    model_class = config.get("class", "MyModel")
    if model_class not in models:
        raise ValueError(f"Unknown model: {model_class}. Available: {list(models.keys())}")

    model = models[model_class](config)

    # Load pretrained weights if specified
    pretrained = config.get("pretrained")
    if pretrained:
        state_dict = torch.load(pretrained, map_location="cpu")
        if "model_state_dict" in state_dict:
            state_dict = state_dict["model_state_dict"]
        model.load_state_dict(state_dict, strict=False)
        print(f"Loaded pretrained weights from {pretrained}")

    return model
