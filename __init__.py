import os
import shutil
import urllib.request
import zipfile
import folder_paths

# --- CONFIGURATION ---
GITHUB_USER = "UmeAiRT"
REPO_NAME = "ComfyUI-Workflows"
BRANCH = "main"

# Automatic URLs
ZIP_URL = f"https://github.com/{GITHUB_USER}/{REPO_NAME}/archive/refs/heads/{BRANCH}.zip"
VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/version.txt"
ZIP_ROOT_NAME = f"{REPO_NAME}-{BRANCH}"
MENU_NAME = "UmeAiRT"

# --- COLORS FOR CONSOLE ---
CYAN = "\033[36m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def check_and_update():
    print(f"############################################################")
    print(f"##             {CYAN}UmeAiRT{RESET} {YELLOW}Workflows (Auto-Sync){RESET}              ##")
    print(f"############################################################")
    # 1. Define paths
    base_path = os.path.dirname(folder_paths.__file__)
    # Final destination: ComfyUI/user/default/workflows/UmeAiRT
    dest_path = os.path.join(base_path, "user", "default", "workflows", MENU_NAME)
    local_version_file = os.path.join(dest_path, "version.txt")
    
    # 2. Read local version (if exists)
    current_version = "0"
    if os.path.exists(local_version_file):
        try:
            with open(local_version_file, 'r', encoding='utf-8') as f:
                current_version = f.read().strip()
        except:
            pass

    # 3. Check remote version (GitHub)
    print(f"{CYAN}[UmeAiRT-Sync]{RESET} 🔍 Checking for updates...")
    try:
        with urllib.request.urlopen(VERSION_URL) as response:
            remote_version = response.read().decode('utf-8').strip()
    except Exception as e:
        print(f"{CYAN}[UmeAiRT-Sync]{RESET}{RED} ⚠️ Could not check for updates (No internet?). Keeping current version.{RESET}")
        return

    # 4. Compare: If versions match, do nothing (fast startup)
    if current_version == remote_version and os.path.exists(dest_path):
        print(f"{CYAN}[UmeAiRT-Sync]{RESET}{GREEN} ✅ Workflows are up to date (v{current_version}).{RESET}")
        return

    # 5. If different, start update process
    print(f"{CYAN}[UmeAiRT-Sync]{RESET}{YELLOW} 📥 New version detected (v{remote_version})! Downloading...{RESET}")
    
    try:
        # Define temp paths
        zip_path = os.path.join(base_path, "temp_umeairt.zip")
        
        # Download ZIP
        urllib.request.urlretrieve(ZIP_URL, zip_path)
        
        # Extract
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(base_path)
        
        extracted_folder = os.path.join(base_path, ZIP_ROOT_NAME)
        
        # Cleanup old folder
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
            
        # Move new folder to destination
        shutil.move(extracted_folder, dest_path)
        
        # Cleanup zip
        os.remove(zip_path)
        print(f"{CYAN}[UmeAiRT-Sync]{RESET}{GREEN} ✨ Successfully updated to v{remote_version}!{RESET}")

    except Exception as e:
        print(f"{CYAN}[UmeAiRT-Sync]{RESET}{RED} ❌ Update failed: {e}{RESET}")
    print(f"############################################################")

# Run check at startup
check_and_update()

# --- MANAGER NODE SIGNATURE ---
# Required to be recognized as a valid extension by ComfyUI Manager
class UmeAiRT_Sync_Node:
    def __init__(self): pass
    @classmethod
    def INPUT_TYPES(s): return {"required": {}}
    RETURN_TYPES = ("STRING",)
    FUNCTION = "noop"
    CATEGORY = "UmeAiRT"
    def noop(self): return ("Installed",)

NODE_CLASS_MAPPINGS = {"UmeAiRT_Sync_Node": UmeAiRT_Sync_Node}
NODE_DISPLAY_NAME_MAPPINGS = {"UmeAiRT_Sync_Node": "🔄 UmeAiRT Workflows (Auto-Sync)"}
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']