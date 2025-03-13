import modal

from config import MODELS_DIR, OUTPUT_DIR
from util.download_helpers import git_install_custom_node


# base setup
image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git", "unzip", "wget")
    .run_commands("pip install --upgrade pip")
    .pip_install("uv")
    .run_commands("uv pip install --system --compile-bytecode huggingface_hub[hf_transfer]==0.28.1")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .run_commands("uv pip install --system --compile-bytecode comfy-cli==1.3.6")
    .run_commands("comfy --skip-prompt install --nvidia")
    .apt_install("libgl1-mesa-glx", "libglib2.0-0") # required for several custom nodes on Linux
)

# custom nodes
image = (
    image
    .run_commands("comfy node install rgthree-comfy")
    .run_commands("comfy node install comfyui-impact-pack")
    .run_commands("comfy node install comfyui-impact-subpack")
    .run_commands("comfy node install comfy-image-saver")
    .run_commands("comfy node install ComfyUI-YOLO")
    .run_commands("comfy node install comfyui-custom-scripts")
    .run_commands("comfy node install efficiency-nodes-comfyui")
    .run_commands("comfy node install comfyui-easy-use")
    .run_commands("comfy node install comfyui-inspire-pack")
    .run_commands("comfy node install comfyui_ipadapter_plus")
    .run_commands("comfy node install comfyui-advancedliveportrait")
    .run_commands("comfy node install wlsh_nodes")
    .run_commands("comfy node install ComfyUI_Comfyroll_CustomNodes")
    .run_commands("comfy node install comfyui_essentials")
    .run_commands("comfy node install ComfyUI-GGUF")
    .run_commands("comfy node install comfyui-detail-daemon")
    .run_commands("comfy node install ComfyUi_NNLatentUpscale")
    .run_commands(git_install_custom_node("ssitu/ComfyUI_UltimateSDUpscale", recursive=True))
    .run_commands(git_install_custom_node("welltop-cn/ComfyUI-TeaCache", install_reqs=True))
    .run_commands("comfy node install ComfyUI-TiledDiffusion")
    .run_commands("comfy node install comfyui_creaprompt")
    .run_commands(git_install_custom_node("nkchocoai/ComfyUI-SaveImageWithMetaData"))
    .run_commands(git_install_custom_node("receyuki/comfyui-prompt-reader-node", recursive=True, install_reqs=True))
)

# mounthed dirs need to be empty for Volume mount to work
image = (
    image
    .run_commands(f"rm -rf {OUTPUT_DIR}")
    .run_commands(f"rm -rf {MODELS_DIR}")
)

image = image.add_local_python_source("config", "enums", "container_setup", "models", "util")
