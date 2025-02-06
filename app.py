import subprocess

import modal

from config import MODELS_DIR, OUTPUT_DIR
from container_setup import image
from enums.gpu import GPU
from models import (civitai_models_to_download, hf_models_to_download,
                    wget_models_to_download)
from util.download_helpers import civitai_dl, hf_dl, wget_dl

app = modal.App(name="comfyui", image=image)
output_vol = modal.Volume.from_name("comfyui-output", create_if_missing=True)
model_vol = modal.Volume.from_name("comfyui-models", create_if_missing=True)


# download models with `modal run app.py::download_models`
@app.local_entrypoint()
def download_models():
    list(hf_dl.starmap(hf_models_to_download))
    list(wget_dl.starmap(wget_models_to_download))

    for local_dir, filename, url in civitai_models_to_download:
        civitai_dl.remote(local_dir, filename, url)


# start ComfyUI with `modal serve app.py`
@app.function(
    allow_concurrent_inputs=10,
    concurrency_limit=1,
    container_idle_timeout=30,
    timeout=1800,
    gpu=[GPU.A10G, GPU.L4],
    volumes={
        OUTPUT_DIR: output_vol,
        MODELS_DIR: model_vol
    }
)
@modal.web_server(8000, startup_timeout=60)
def ui():
    subprocess.Popen("comfy launch -- --listen 0.0.0.0 --port 8000", shell=True)