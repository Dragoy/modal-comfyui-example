import os
import shutil
import subprocess
from typing import Optional

import modal
from huggingface_hub import hf_hub_download, snapshot_download

from config import MODELS_DIR, OUTPUT_DIR
from container_setup import image
from enums.gpu import GPU
from models import (civitai_models_to_download, hf_models_to_download,
                    wget_models_to_download)

app = modal.App(name="comfyui", image=image)
output_vol = modal.Volume.from_name("comfyui-output", create_if_missing=True)
model_vol = modal.Volume.from_name("comfyui-models", create_if_missing=True)


@app.function(
    secrets=[modal.Secret.from_name("tokens", required_keys=["HF_TOKEN"])],
    volumes={MODELS_DIR: model_vol}
)
def hf_dl(local_dir: str, filename: str, repo_id: str, subfolder: Optional[str] = None):
    tmp_dir = "/tmp/download"

    tmp_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        subfolder=subfolder,
        local_dir=tmp_dir
    )

    target_dir = f"{MODELS_DIR}/{local_dir}"
    os.makedirs(target_dir, exist_ok=True)

    shutil.move(tmp_path, target_dir + "/" + filename)

    if subfolder:
        os.removedirs(tmp_dir + "/" + subfolder)

@app.function(
    secrets=[modal.Secret.from_name("tokens", required_keys=["HF_TOKEN"])],
    volumes={MODELS_DIR: model_vol}
)
def hf_clone_repo(repo_id: str, local_dir: str):
    target_dir = f"{MODELS_DIR}/{local_dir}"
    os.makedirs(target_dir, exist_ok=True)

    snapshot_download(
        repo_id=repo_id,
        local_dir=f"{MODELS_DIR}/{local_dir}"
    )

@app.function(
    secrets=[modal.Secret.from_name("tokens", required_keys=["CIVITAI_TOKEN"])],
    volumes={MODELS_DIR: model_vol}
)
def civitai_dl(local_dir: str, filename: str, url: str):
    token = os.environ["CIVITAI_TOKEN"]

    cmd = (
        f"comfy --skip-prompt model download --url '{url}' "
        f"--relative-path 'models/{local_dir}' "
        f"--filename '{filename}' "
        f"--set-civitai-api-token '{token}'"
    )

    subprocess.run(cmd, shell=True, check=True)

@app.function(volumes={MODELS_DIR: model_vol})
def wget_dl(local_dir: str, url: str):
    cmd = f"wget '{url}' -P {MODELS_DIR}/{local_dir}"

    subprocess.run(cmd, shell=True, check=True)


# download models with `modal run app.py::download_models`
@app.local_entrypoint()
def download_models():
    list(hf_dl.starmap(hf_models_to_download))
    list(wget_dl.starmap(wget_models_to_download))

    for local_dir, filename, url in civitai_models_to_download:
        civitai_dl.remote(local_dir, filename, url)


# start ComfyUI with `modal serve app.py`
@app.function(
    max_containers=1,
    scaledown_window=30,
    timeout=1800,
    region="eu-west",
    gpu=[GPU.A100_80GB],
    volumes={
        OUTPUT_DIR: output_vol,
        MODELS_DIR: model_vol
    }
)
@modal.concurrent(max_inputs=10)
@modal.web_server(8000, startup_timeout=60)
def ui():
    subprocess.Popen("comfy launch -- --listen 0.0.0.0 --port 8000", shell=True)
