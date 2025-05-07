# local_dir, filename, repo_id, subfolder
hf_models_to_download = [
    # ("unet/FLUX", "flux1-dev-Q8_0.gguf", "city96/FLUX.1-dev-gguf"),
    # ("diffusion_models", "hidream_i1_dev_bf16.safetensors", "Comfy-Org/HiDream-I1_ComfyUI", "split_files/diffusion_models"),
    # ("diffusion_models", "hidream_i1_full_fp16.safetensors", "Comfy-Org/HiDream-I1_ComfyUI", "split_files/diffusion_models"),
    # ("clip", "clip_g_hidream.safetensors", "Comfy-Org/HiDream-I1_ComfyUI", "split_files/text_encoders"),
    # ("clip", "clip_l_hidream.safetensors", "Comfy-Org/HiDream-I1_ComfyUI", "split_files/text_encoders"),
    # ("clip", "t5xxl_fp8_e4m3fn_scaled.safetensors", "Comfy-Org/HiDream-I1_ComfyUI", "split_files/text_encoders"),
    # ("clip", "llama_3.1_8b_instruct_fp8_scaled.safetensors", "Comfy-Org/HiDream-I1_ComfyUI", "split_files/text_encoders"),
    # ("vae", "ae.safetensors", "Comfy-Org/HiDream-I1_ComfyUI", "split_files/vae"),

    ("diffusion_models", "wan2.1_i2v_720p_14B_bf16.safetensors", "Comfy-Org/Wan_2.1_ComfyUI_repackaged", "split_files/diffusion_models"),
    ("text_encoders", "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "Comfy-Org/Wan_2.1_ComfyUI_repackaged", "split_files/text_encoders"),
    ("vae", "wan_2.1_vae.safetensors", "Comfy-Org/Wan_2.1_ComfyUI_repackaged", "split_files/vae"),
    ("clip_vision", "clip_vision_h.safetensors", "Comfy-Org/Wan_2.1_ComfyUI_repackaged", "split_files/clip_vision"),
]

# local_dir, filename, url
civitai_models_to_download = [
    ("checkpoints/SDXL", "animagineXL40_v40.safetensors", "https://civitai.com/api/download/models/1337429?type=Model&format=SafeTensor&size=full&fp=fp16"),     # https://civitai.com/models/1188071
]

# local_dir, url
wget_models_to_download = [
    ("upscale_models", "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"),
]

# Списки уже загруженных моделей мы будем определять динамически
