import os
from datetime import datetime

def initialize_project():
    """Creates the timestamped project directory and all necessary subfolders."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_dir = f"project_{timestamp}"
    
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
