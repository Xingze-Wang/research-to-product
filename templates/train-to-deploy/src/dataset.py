"""
=== YOUR DATA LOADING GOES HERE ===

Implement build_dataset() to return a PyTorch Dataset.
The training loop handles DataLoader, DistributedSampler, etc.
"""

from torch.utils.data import Dataset


class PlaceholderDataset(Dataset):
    """
    Replace this with your actual dataset.

    Requirements:
      - __getitem__ returns a dict that your model.forward() can accept
      - Keys should match your model's forward() signature

    Example for a text classifier:
        def __getitem__(self, idx):
            text = self.texts[idx]
            tokens = self.tokenizer(text, return_tensors="pt", padding="max_length")
            return {
                "input_ids": tokens["input_ids"].squeeze(),
                "labels": torch.tensor(self.labels[idx]),
            }
    """

    def __init__(self, data_path: str, split: str = "train"):
        import torch

        # --- REPLACE WITH YOUR DATA LOADING ---
        print(f"TODO: Load {split} data from {data_path}")
        self.size = 1000  # placeholder
        self.data = torch.randn(self.size, 768)
        self.labels = torch.randint(0, 10, (self.size,))

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        return {
            "x": self.data[idx],
            "labels": self.labels[idx],
        }


def build_dataset(data_config: dict, split: str = "train") -> Dataset:
    """
    Build dataset from config. Add your dataset classes here.
    """
    path_key = f"{split}_path"
    data_path = data_config.get(path_key, data_config.get("train_path"))
    return PlaceholderDataset(data_path, split)
