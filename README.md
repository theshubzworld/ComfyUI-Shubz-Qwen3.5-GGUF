## ComfyUI-Qwen3.5-Uncensored-GGUF

**GGUF-only** build of [ComfyUI-Qwen3.5-Uncensored](https://github.com/Deaquay/ComfyUI-Qwen3.5-Uncensored). Uses `llama-cpp-python` instead of `transformers` — no transformers dependency, so it won't conflict with older ComfyUI nodes that need transformers <5.

### Requirements

- **Python**: 3.10, 3.11, 3.12, 3.13, or 3.14
- **CUDA**: 12.4, 12.6, 12.8, or 13.0
- **llama-cpp-python**: Must be installed from [JamePeng's fork](https://github.com/JamePeng/llama-cpp-python/releases/) (not pip)

Tested with Python 3.13 + CUDA 13.0 + PyTorch 2.10/2.11.

If your Python or CUDA version isn't listed above, the required llama-cpp-python wheels are not available and this node pack won't work.

### Why this version?

`transformers>=5.2.0` is required by the full version for HuggingFace model support, but it breaks some older ComfyUI custom nodes. This GGUF-only build removes that dependency entirely while keeping all GGUF functionality.

### Nodes included

| Node | Description |
|------|-------------|
| **Qwen3.5-Uncensored (GGUF)** | Vision-language inference with GGUF models (image + video) |
| **Qwen3.5-Uncensored Advanced (GGUF)** | Same with full parameter control (ctx, batch, gpu layers, etc.) |
| **Qwen3.5-Uncensored Prompt Enhancer (GGUF)** | Text-only prompt enhancement/rewriting |
| **Story Split Node** | Splits WAN 2.2 Story output into 4 separate prompts |
| **VRAM Cleanup** | VRAM cleanup with multiple modes |

### Automatic Local Model Discovery

You don't need to edit JSON config files. The nodes automatically scan your local model directories:

- **GGUF models**: Any `.gguf` file found under `models/LLM/GGUF` (or any extra model path you've configured) shows up in the dropdown with a `[local]` prefix
- mmproj files in the same directory are automatically paired with the model
- Respects ComfyUI's `--base-directory`, `extra_model_paths.yaml`, and all registered LLM paths
- Model architecture (Qwen3.5 vs others) is detected from GGUF file metadata, not the model name
- Pre-configured models from `gguf_models.json` still work with auto-download

**REMEMBER: VL models need an mmproj file in the same folder to show up in the VL model list.**

---

### Installation

```bash
cd ComfyUI/custom_nodes/

git clone https://github.com/Deaquay/ComfyUI-Qwen3.5-Uncensored-GGUF.git

cd ComfyUI-Qwen3.5-Uncensored-GGUF

pip install -r requirements.txt
```

#### Install llama-cpp-python

You **must** install from [JamePeng's fork](https://github.com/JamePeng/llama-cpp-python/releases/), not pip.

Pick the wheel matching your CUDA + Python version. 

Example for Python 3.13 + CUDA 13.0 on Linux:

```bash
pip install https://github.com/JamePeng/llama-cpp-python/releases/download/v0.3.34-cu130-Basic-linux-20260331/llama_cpp_python-0.3.34+cu130.basic-cp313-cp313-linux_x86_64.whl
```

Available for CUDA 12.4, 12.6, 12.8, 13.0 and Python 3.10–3.14.

For Windows users with Python 3.13 + CUDA 13.0, use:

```
pip install https://github.com/JamePeng/llama-cpp-python/releases/download/v0.3.34-cu130-Basic-win-20260331/llama_cpp_python-0.3.34+cu130.basic-cp313-cp313-win_amd64.whl
```

But better look into the releases of the JamePeng repo for your version.

### Adding models

- Drop GGUF files into `models/LLM/GGUF/` — they'll be auto-detected
- **For VL models, put the mmproj file in the same directory as the model file**
- Or add entries to `gguf_models.json` for auto-download from HuggingFace

### What's NOT included (compared to the full version)

- No HuggingFace/transformers model support
- No Flash Attention 2 / SageAttention acceleration
- No BitsAndBytes quantization
- No HF Prompt Enhancer node

If you need those features, use the [full version](https://github.com/Deaquay/ComfyUI-Qwen3.5-Uncensored) instead.

### License

GPL-3.0 — see [LICENSE](LICENSE)
