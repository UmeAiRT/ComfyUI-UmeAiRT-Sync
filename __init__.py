import os
import shutil
import urllib.request
import zipfile
import folder_paths

# --- REPOSITORY CONFIGURATION ---
GITHUB_USER = "UmeAiRT"
REPO_NAME = "ComfyUI-Workflows"
BRANCH = "main"

# Auto-generated URLs based on config
ZIP_URL = f"https://github.com/{GITHUB_USER}/{REPO_NAME}/archive/refs/heads/{BRANCH}.zip"
VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/version.txt"
ZIP_ROOT_NAME = f"{REPO_NAME}-{BRANCH}"
MENU_NAME = "UmeAiRT"

# --- CONSOLE COLORS SETUP ---
# Initializes colorama to ensure ANSI colors work correctly on Windows CMD/PowerShell
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(convert=True, autoreset=True)
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    RESET = Style.RESET_ALL
except ImportError:
    # Fallback if colorama is not present
    CYAN = GREEN = YELLOW = RED = RESET = ""

def check_and_update():
    """
    Checks the remote repository for updates at startup.
    Downloads and installs workflows if the remote version differs from the local one.
    """
    
    # 1. Setup paths
    base_path = os.path.dirname(folder_paths.__file__)
    # Target path: ComfyUI/user/default/workflows/UmeAiRT
    dest_path = os.path.join(base_path, "user", "default", "workflows", MENU_NAME)
    local_version_file = os.path.join(dest_path, "version.txt")
    
    # 2. Read local version
    current_version = "0"
    if os.path.exists(local_version_file):
        try:
            with open(local_version_file, 'r', encoding='utf-8') as f:
                current_version = f.read().strip()
        except Exception:
            pass

    # 3. Check remote version
    print(f"[{CYAN}UmeAiRT-Sync{RESET}] 🔍 Checking for workflows updates...")
    
    try:
        with urllib.request.urlopen(VERSION_URL) as response:
            remote_version = response.read().decode('utf-8').strip()
    except Exception as e:
        print(f"[{CYAN}UmeAiRT-Sync{RESET}]{RED} ⚠️ Check failed (No internet?). Keeping v{current_version}.{RESET}")
        return

    # 4. Compare versions
    if current_version == remote_version and os.path.exists(dest_path):
        print(f"[{CYAN}UmeAiRT-Sync{RESET}]{GREEN} ✅ Workflows are up to date (v{current_version}).{RESET}")
        return

    # 5. Perform Update
    print(f"[{CYAN}UmeAiRT-Sync{RESET}]{YELLOW} 📥 New version detected (v{remote_version})! Downloading...{RESET}")
    
    try:
        temp_zip_path = os.path.join(base_path, "temp_umeairt.zip")
        
        # Download repository zip
        urllib.request.urlretrieve(ZIP_URL, temp_zip_path)
        
        # Extract content
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(base_path)
        
        extracted_folder = os.path.join(base_path, ZIP_ROOT_NAME)
        
        # Remove old directory if it exists
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
            
        # Move extracted files to destination
        shutil.move(extracted_folder, dest_path)
        
        # Cleanup temporary zip
        os.remove(temp_zip_path)
        print(f"[{CYAN}UmeAiRT-Sync{RESET}]{GREEN} ✨ Successfully updated to v{remote_version}!{RESET}")

    except Exception as e:
        print(f"[{CYAN}UmeAiRT-Sync{RESET}]{RED} ❌ Update failed: {e}{RESET}")

# Execute synchronization logic on import
check_and_update()

# --- NODE DEFINITION ---
# Defines a dummy node to ensure the folder is recognized as a Custom Node by ComfyUI
class UmeAiRT_Sync_Node:
    def __init__(self): pass
    
    @classmethod
    def INPUT_TYPES(s): 
        return {"required": {}}
        
    RETURN_TYPES = ("STRING",)
    FUNCTION = "noop"
    CATEGORY = "UmeAiRT"
    
    def noop(self): 
        return ("Installed",)

NODE_CLASS_MAPPINGS = {
    "UmeAiRT_Sync_Node": UmeAiRT_Sync_Node
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UmeAiRT_Sync_Node": "🔄 UmeAiRT Workflows (Auto-Sync)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']