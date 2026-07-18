# Shared utilities for GGUF nodes
# Cache functions, hash helpers, and common constants extracted from Shubz_QwenVL.py
# so that GGUF-only builds don't need the transformers dependency.

import hashlib
import json
from pathlib import Path

# Global cache for generated prompts
PROMPT_CACHE = {}
CACHE_FILE = Path(__file__).parent / "prompt_cache.json"


def load_prompt_cache():
    """Load prompt cache from file"""
    global PROMPT_CACHE
    try:
        if CACHE_FILE.exists():
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                PROMPT_CACHE = json.load(f)
                print(f"[Shubz QwenVL] Loaded {len(PROMPT_CACHE)} cached prompts")
    except Exception as e:
        print(f"[Shubz QwenVL] Failed to load prompt cache: {e}")
        PROMPT_CACHE = {}


def save_prompt_cache():
    """Save prompt cache to file"""
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(PROMPT_CACHE, f, indent=2)
    except Exception as e:
        print(f"[Shubz QwenVL] Failed to save prompt cache: {e}")


def get_cache_key(model_name, preset_prompt, custom_prompt, image_hash=None, video_hash=None, seed=None):
    """Generate cache key from inputs"""
    key_data = {
        "model": model_name,
        "preset": preset_prompt,
        "custom": custom_prompt.strip() if custom_prompt else "",
        "image": image_hash,
        "video": video_hash,
        "seed": seed,
    }
    key_str = json.dumps(key_data, sort_keys=True)
    return hashlib.md5(key_str.encode()).hexdigest()


def get_alternative_cache_key(model_name, preset_prompt, custom_prompt, image_hash=None, video_hash=None, seed=None, module_name="Shubz QwenVL"):
    """Generate alternative cache key for fixed seed mode to find random prompts"""
    print(f"[{module_name} DEBUG] Searching through cache for model={model_name}, preset={preset_prompt}")

    for cached_key, cached_data in PROMPT_CACHE.items():
        cached_model = cached_data.get("model")
        cached_preset = cached_data.get("preset")
        cached_seed = cached_data.get("seed")

        print(f"[{module_name} DEBUG] Checking entry: model={cached_model}, preset={cached_preset}, seed={cached_seed}")

        if (cached_model == model_name and
            cached_preset == preset_prompt and
            cached_seed != seed):

            cached_image_hash = cached_data.get("image_hash")
            cached_video_hash = cached_data.get("video_hash")

            print(f"[{module_name} DEBUG] Found potential match with hashes: image={cached_image_hash}, video={cached_video_hash}")

            if cached_image_hash is None and cached_video_hash is None:
                if image_hash is None and video_hash is None:
                    print(f"[{module_name} DEBUG] Match found (no images/videos)!")
                    return cached_key
            else:
                if cached_image_hash == image_hash and cached_video_hash == video_hash:
                    print(f"[{module_name} DEBUG] Match found (hashes match)!")
                    return cached_key
    print(f"[{module_name} DEBUG] No alternative cache found")
    return None


def get_image_hash(image):
    """Generate hash for image tensor"""
    if image is None:
        return None
    try:
        shape = str(image.shape)
        dtype = str(image.dtype)
        if len(image.shape) >= 3:
            sample_pixels = image.flatten()[:100].tolist() if image.numel() > 0 else []
        else:
            sample_pixels = image.flatten().tolist() if image.numel() > 0 else []

        content = f"{shape}_{dtype}_{sample_pixels[:10]}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    except Exception:
        return None


def get_video_hash(video):
    """Generate hash for video tensor (same as image)"""
    return get_image_hash(video)


# Load cache on module import
load_prompt_cache()
