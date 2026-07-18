"""
{
  "name": "ComfyUI-Shubz-Qwen3.5-GGUF",
  "description": "ComfyUI-Shubz-Qwen3.5-GGUF for ComfyUI. Uses llama-cpp-python — no transformers dependency.",
  "author": "Shubz",
  "version": "1.0.0",
  "url": "https://github.com/theshubzworld/ComfyUI-Shubz-Qwen3.5-GGUF",
  "category": "image"
}
"""

import importlib.util
import os
import sys
import ctypes

# Get the directory of the current script
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)

# Workaround for Windows DLL load entry point conflict between PyTorch and llama-cpp-python OpenMP runtimes
if sys.platform == "win32":
    try:
        import site
        libomp_loaded = False
        # Search in site-packages and python directories
        search_dirs = []
        try:
            search_dirs.extend(site.getsitepackages())
        except AttributeError:
            pass
        search_dirs.append(os.path.dirname(sys.executable))
        
        for site_dir in search_dirs:
            potential_paths = [
                os.path.join(site_dir, "Lib", "site-packages", "llama_cpp", "lib", "libomp140.x86_64.dll"),
                os.path.join(site_dir, "llama_cpp", "lib", "libomp140.x86_64.dll")
            ]
            for potential_path in potential_paths:
                if os.path.exists(potential_path):
                    ctypes.CDLL(potential_path)
                    libomp_loaded = True
                    print(f"[Shubz Qwen3.5 GGUF Workaround] Pre-loaded libomp DLL from: {potential_path}")
                    break
            if libomp_loaded:
                break
        
        # Fallback to sys.path search if not loaded
        if not libomp_loaded:
            for path_entry in sys.path:
                potential_path = os.path.join(path_entry, "llama_cpp", "lib", "libomp140.x86_64.dll")
                if os.path.exists(potential_path):
                    ctypes.CDLL(potential_path)
                    print(f"[Shubz Qwen3.5 GGUF Workaround] Pre-loaded libomp DLL from sys.path: {potential_path}")
                    break
    except Exception as e:
        print(f"[Shubz Qwen3.5 GGUF Workaround] Warning: Failed to pre-load libomp DLL: {e}")

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "./web"

def load_modules_from_directory(directory):
    for file in os.listdir(directory):
        if file.endswith(".py"):
            file_path = os.path.join(directory, file)
            module_name = os.path.basename(file)[:-3]
            if module_name == os.path.basename(__file__)[:-3]:
                continue

            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                if hasattr(module, "NODE_CLASS_MAPPINGS"):
                    NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
                if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
                    NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
            except Exception as e:
                print(f"Error loading module {module_name}: {e}")

load_modules_from_directory(current_dir)

# Also load from nodes subdirectory
nodes_dir = os.path.join(current_dir, "nodes")
if os.path.exists(nodes_dir):
    load_modules_from_directory(nodes_dir)
NODE_CLASS_MAPPINGS = dict(sorted(NODE_CLASS_MAPPINGS.items(), key=lambda x: NODE_DISPLAY_NAME_MAPPINGS.get(x[0], x[0])))
NODE_DISPLAY_NAME_MAPPINGS = dict(sorted(NODE_DISPLAY_NAME_MAPPINGS.items(), key=lambda x: x[1]))

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS"
]
