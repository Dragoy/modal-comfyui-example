# local_dir, filename, repo_id, subfolder
hf_models_to_download = [
    ("unet/FLUX",           "flux1-dev-Q8_0.gguf",                      "city96/FLUX.1-dev-gguf"),
]

hf_models_downloaded = [
]

# local_dir, filename, url
civitai_models_to_download = [
    ("checkpoints/SDXL",            "animagineXL40_v40.safetensors",                    "https://civitai.com/api/download/models/1337429?type=Model&format=SafeTensor&size=full&fp=fp16"),     # https://civitai.com/models/1188071
]

civitai_models_downloaded = [
]

# local_dir, url
wget_models_to_download = [
    ("upscale_models", "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"),
]

wget_models_downloaded = [
]