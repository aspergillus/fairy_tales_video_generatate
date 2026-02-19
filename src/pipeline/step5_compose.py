import os
import glob
from moviepy import AudioFileClip, VideoFileClip, concatenate_videoclips

def compose_final_video(project_dir):
    """Composes the final 10-minute video by concatenating audio and video chunks."""
    print("[Step 5] Starting video composition...")
    
    audio_dir = os.path.join(project_dir, "audio_chunks")
    video_dir = os.path.join(project_dir, "video_chunks")
    final_output = os.path.join(project_dir, "final_render", "final_video.mp4")
    
    # Notice we look for .mp3 since edge_tts outputs mp3 format
    audio_files = sorted(glob.glob(os.path.join(audio_dir, "audio_*.mp3")))
    video_files = sorted(glob.glob(os.path.join(video_dir, "video_*.mp4")))
    
    if not audio_files or not video_files:
        print("[Step 5 Status] Audio or video chunks are missing. Cannot compose until Step 3 and Step 4 are complete.")
        return False
        
    if len(audio_files) != len(video_files):
        print(f"[Step 5 Warning] Mismatch between number of audio files ({len(audio_files)}) and video files ({len(video_files)}).")
        
    print(f"[Step 5] Found {len(audio_files)} audio chunks and {len(video_files)} video chunks.")
    
    final_clips = []
    
    try:
        # Pair up audio and video sequentially
        for i in range(min(len(audio_files), len(video_files))):
            v_path = video_files[i]
            a_path = audio_files[i]
            
            # Load clips
            video_clip = VideoFileClip(v_path)
            audio_clip = AudioFileClip(a_path)
            
            # Sub-clips might have slightly different durations. 
            # E.g. Ken burns video is strictly 5.0 seconds. The spoken TTS might be 3 to 6 seconds.
            # We align the video generation exactly to the spoken audio's duration.
            final_audio_duration = audio_clip.duration
            
            # Ensure the video matches the exact duration of the spoken audio.
            # Usually Ken Burns videos generated are fixed duration, so we loop or trim the video.
            # For fairy tales, freezing the final frame or repeating is fine.
            # Fortunately MoviePy handles this nicely. We just lock the audio track.
            
            # Note: Ken burns videos are exactly 5.0 in our step 4 logic. If audio is 6.2s, 
            # moviepy will freeze the last frame for 1.2s.
            video_clip = video_clip.with_duration(final_audio_duration)
            
            # Set audio
            scene_clip = video_clip.with_audio(audio_clip)
            final_clips.append(scene_clip)
            
        print("[Step 5] Concatenating all scenes. This may take a while depending on total duration...")
        # Concatenate into one massive timeline
        final_video = concatenate_videoclips(final_clips, method="compose")
        
        # Write final result
        print(f"[Step 5] Writing final render to {final_output}")
        # Audio codec 'aac' provides broad compatibility with typical mp4 containers
        final_video.write_videofile(
            final_output, 
            fps=24, 
            codec="libx264", 
            audio_codec="aac"
        )
        
        # Free resources
        final_video.close()
        for clip in final_clips:
            clip.close()
            
        print(f"[Step 5] Final compilation successful! Output available at: {final_output}")
        return True
        
    except Exception as e:
        print(f"[Step 5 Error] An error occurred during composition: {e}")
        return False
