import os
import shutil
import subprocess
from typing import Optional

import modal
from huggingface_hub import hf_hub_download, snapshot_download

from app import app, model_vol
from config import COMFY_DIR, MODELS_DIR


def git_install_custom_node(repo_id: str, recursive: bool = False, install_reqs: bool = False):
    custom_node = repo_id.split("/")[-1]
    
    command = f"git clone https://github.com/{repo_id}"

    if recursive:
        command += " --recursive"

    command += f" {COMFY_DIR}/custom_nodes/{custom_node}"

    if install_reqs:
        command += f" && uv pip install --system --compile-bytecode -r {COMFY_DIR}/custom_nodes/{custom_node}/requirements.txt"

    return command

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