from config import COMFY_DIR


def git_install_custom_node(repo_id: str, recursive: bool = False, install_reqs: bool = False):
    custom_node = repo_id.split("/")[-1]
    
    command = f"git clone https://github.com/{repo_id}"

    if recursive:
        command += " --recursive"

    command += f" {COMFY_DIR}/custom_nodes/{custom_node}"

    if install_reqs:
        command += f" && uv pip install --system --compile-bytecode -r {COMFY_DIR}/custom_nodes/{custom_node}/requirements.txt"

    return command

