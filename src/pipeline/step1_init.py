import os
from datetime import datetime
import sys

# Ensure config can be imported from parent
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import WORKSPACE_DIR

def initialize_project():
    """Creates the timestamped project directory and all necessary subfolders."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_dir = os.path.join(WORKSPACE_DIR, f"project_{timestamp}")
    
    directories = [
        "scripts",
        "audio_chunks",
        "video_chunks",
        "final_render"
    ]
    
    try:
        os.makedirs(project_dir, exist_ok=True)
        for d in directories:
            os.makedirs(os.path.join(project_dir, d), exist_ok=True)
        print(f"[Step 1] Initialized project directory: {project_dir}")
        return project_dir
    except Exception as e:
        print(f"[Step 1 Error] Failed to initialize directories: {e}")
        return None
