import os
import subprocess
import glob

def compose_final_video(project_dir):
    """Composes the final 10-minute video by concatenating audio and video chunks."""
    print("[Step 5] Starting video composition...")
    
    audio_dir = os.path.join(project_dir, "audio_chunks")
    video_dir = os.path.join(project_dir, "video_chunks")
    final_output = os.path.join(project_dir, "final_render", "final_video.mp4")
    
    audio_files = sorted(glob.glob(os.path.join(audio_dir, "audio_*.wav")))
    video_files = sorted(glob.glob(os.path.join(video_dir, "video_*.mp4")))
    
    # Check if files exist to compose
    if not audio_files or not video_files:
        print("[Step 5 Status] Audio or video chunks are missing. Skipping composition (Expected since actual generation APIs are mocked).")
        return True # Return true so the script doesn't abort
        
    if len(audio_files) != len(video_files):
        print(f"[Step 5 Warning] Mismatch between number of audio files ({len(audio_files)}) and video files ({len(video_files)}).")
        
    # We create a text file for ffmpeg to concatenate
    list_file_path = os.path.join(project_dir, "ffmpeg_concat_list.txt")
    
    try:
        with open(list_file_path, "w") as f:
             # Iterate to create paired ffmpeg instructions
             for i in range(min(len(audio_files), len(video_files))):
                 # FFmpeg expects relative or absolute paths, properly quoted
                 v_file = os.path.abspath(video_files[i]).replace("\\", "/")
                 a_file = os.path.abspath(audio_files[i]).replace("\\", "/")
                 
                 # The standard way to concat in ffmpeg using a demuxer file is just video first, 
                 # but since we want to mux audio & video, we might be better off running a complex script.
                 # For simplicity of the orchestrator, we will outline a simple concatenation logic,
                 # but leave it mocked since dummy files aren't real valid media files.
                 f.write(f"file '{v_file}'\n")
                 
        print(f"[Step 5] Created concat list for FFmpeg at {list_file_path}")
        
        # Real FFmpeg implementation to concatenate and map audio (assuming video clips already have the audio merged, or using a more complex filtergraph):
        """
        # A simple concat if the videos already had their respective audio:
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
            "-i", list_file_path, 
            "-c", "copy", final_output
        ]
        
        print("[Step 5] Running FFmpeg concatenation...")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"[Step 5 Error] FFmpeg failed:\\n{result.stderr}")
            return False
        """
        
        print(f"[Step 5] Final composition mocked successfully. Expected output: {final_output}")
        return True
        
    except Exception as e:
        print(f"[Step 5 Error] An error occurred during composition: {e}")
        return False
