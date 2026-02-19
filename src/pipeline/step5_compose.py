import os
import glob
import subprocess

def compose_final_video(project_dir):
    """Composes the final video by concatenating audio and video chunks using FFmpeg."""
    print("[Step 5] Starting video composition via FFmpeg...")
    
    audio_dir = os.path.join(project_dir, "audio_chunks")
    video_dir = os.path.join(project_dir, "video_chunks")
    final_output = os.path.join(project_dir, "final_render", "final_video.mp4")
    temp_dir = os.path.join(project_dir, "temp_muxed")
    
    os.makedirs(temp_dir, exist_ok=True)
    
    audio_files = sorted(glob.glob(os.path.join(audio_dir, "audio_*.mp3")))
    video_files = sorted(glob.glob(os.path.join(video_dir, "video_*.mp4")))
    
    if not audio_files or not video_files:
        print("[Step 5 Status] Audio or video chunks are missing. Cannot compose.")
        return False
        
    print(f"[Step 5] Found {len(audio_files)} audio chunks and {len(video_files)} video chunks. Muxing pairs...")
    
    muxed_files = []
    
    try:
        # Mux each video/audio pair individually
        count = min(len(audio_files), len(video_files))
        for i in range(count):
            v_path = video_files[i]
            a_path = audio_files[i]
            out_path = os.path.join(temp_dir, f"scene_{i:03d}.mp4")
            
            # Use ffmpeg to mux video and audio. 
            # -shortest ensures it stops when the shortest stream ends (usually audio since video is 5s)
            # -c:v copy avoids re-encoding video if possible, but since we want to align durations precisely, 
            # we'll re-encode or just copy and let the player handle it. Let's do a fast encode.
            cmd = [
                "ffmpeg", "-y", "-loglevel", "error",
                "-i", v_path,
                "-i", a_path,
                "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-shortest",
                out_path
            ]
            subprocess.run(cmd, check=True)
            muxed_files.append(out_path)
            
        print("[Step 5] Muxing complete. Concatenating all scenes into final video...")
        
        # Create a concat list
        list_file_path = os.path.join(project_dir, "ffmpeg_concat_list.txt")
        with open(list_file_path, "w") as f:
            for m in muxed_files:
                p = os.path.abspath(m).replace("\\", "/")
                f.write(f"file '{p}'\n")
                
        # Concat demuxer
        concat_cmd = [
            "ffmpeg", "-y", "-loglevel", "warning",
            "-f", "concat", "-safe", "0",
            "-i", list_file_path,
            "-c", "copy",
            final_output
        ]
        
        subprocess.run(concat_cmd, check=True)
        print(f"[Step 5] Final compilation successful! Output: {final_output}")
        
        # Clean up temp files
        for m in muxed_files:
            try:
                os.remove(m)
            except:
                pass
        try:
            os.remove(list_file_path)
            os.rmdir(temp_dir)
        except:
            pass
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[Step 5 Error] FFmpeg command failed: {e}")
        return False
    except Exception as e:
        print(f"[Step 5 Error] Failed during composition: {e}")
        return False
