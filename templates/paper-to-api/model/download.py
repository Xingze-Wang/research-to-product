"""
Model weight management.
Download once, cache locally, never think about it again.
"""

import os
from pathlib import Path


def ensure_weights(source: str, cache_dir: str = "./weights") -> str:
    """
    Ensure model weights are available locally.

    Args:
        source: HuggingFace model ID, URL, or local path
        cache_dir: Where to store downloaded weights

    Returns:
        Local path to the weights
    """
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)

    # Already local
    if os.path.exists(source):
        return source

    # HuggingFace Hub
    if "/" in source and not source.startswith("http"):
        try:
            from huggingface_hub import snapshot_download

            local_dir = snapshot_download(
                repo_id=source,
                local_dir=str(cache_path / source.replace("/", "--")),
            )
            print(f"Downloaded {source} → {local_dir}")
            return local_dir
        except ImportError:
            raise RuntimeError(
                "Install huggingface_hub: pip install huggingface_hub"
            )

    # URL download
    if source.startswith("http"):
        import urllib.request

        filename = source.split("/")[-1]
        dest = str(cache_path / filename)
        if not os.path.exists(dest):
            print(f"Downloading {source} → {dest}")
            urllib.request.urlretrieve(source, dest)
        return dest

    raise ValueError(f"Cannot resolve model source: {source}")
