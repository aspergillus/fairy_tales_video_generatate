import os
import json
import requests
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import textwrap
from moviepy import ImageClip, vfx

def create_fallback_image(text, output_path):
    """Creates a localized fallback placeholder image containing the text prompt."""
    img = Image.new('RGB', (1920, 1080), color=(40, 44, 52))
    d = ImageDraw.Draw(img)
    
    # Try using default font, scale by wrapping
    margin = 100
    offset = 100
    for line in textwrap.wrap(text, width=40):
        # Default PIL font is small, but it works as a fallback guarantee
        d.text((margin, offset), line, fill=(200, 220, 240))
        offset += 50
        
    img.save(output_path, "JPEG")
    return True

def create_ken_burns_video(image_path, output_path, duration=5.0):
    """
    Takes an image, applies a gentle zoom-in (Ken Burns), and creates a video clip.
    In moviepy v2.x, vfx.resize takes either a scalar factor or a function.
    We will zoom in by 10% over the duration.
    """
    try:
        # Load the image
        clip = ImageClip(image_path).with_duration(duration)
        
        # A zoom effect function: t is time in seconds
        # Zoom starts at 1.0 and goes up to 1.1 at the end
        def zoom(t):
            return 1.0 + (0.1 * (t / duration))

        # Apply resize and crop to center
        zoomed_clip = clip.with_effects([vfx.Resize(zoom)])
        
        # Ensure it maintains 1920x1080 bounds 
        # (resizing an image upwards makes it larger than 1920x1080, so we crop center)
        # Using a fixed crop center for simplicity
        w, h = clip.size
        cropped_clip = zoomed_clip.with_effects([
            vfx.Crop(x_center=w/2, y_center=h/2, width=w, height=h)
        ]).with_fps(24)

        # Write out
        cropped_clip.write_videofile(output_path, codec="libx264", audio=False, logger=None)
        
        # Cleanup the clip resources
        cropped_clip.close()
        zoomed_clip.close()
        clip.close()
        return True
    except Exception as e:
        print(f"Error creating Ken Burns video: {e}")
        return False

def generate_video(project_dir):
    """Reads the story.json, fetches images from Pollinations API, and generates Ken Burns videos."""
    print("[Step 4] Starting Image-to-Video generation...")
    story_path = os.path.join(project_dir, "scripts", "story.json")
    
    if not os.path.exists(story_path):
        print(f"[Step 4 Error] Story file not found at {story_path}")
        return False
        
    try:
        with open(story_path, "r", encoding="utf-8") as f:
            story = json.load(f)
            
        scenes = story.get("scenes", [])
        if not scenes:
            print("[Step 4 Error] No scenes found in the story format JSON.")
            return False
            
        for scene in scenes:
            scene_num = scene.get("scene_number")
            visual_prompt = scene.get("visual_prompt")
            
            print(f"\n[Step 4] Generating image for scene {scene_num}/{len(scenes)}...")
            
            # 1. Fetch Image
            safe_prompt = urllib.parse.quote(visual_prompt)
            # Seed forces some consistency. nologo removes watermark.
            image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1920&height=1080&nologo=true&seed=42"
            
            image_filename = f"image_{scene_num:03d}.jpg"
            image_path = os.path.join(project_dir, "video_chunks", image_filename)
            
            # Switch to API fallback logic
            fallback_needed = False
            try:
                response = requests.get(image_url, stream=True, timeout=15)
                if response.status_code == 200:
                    with open(image_path, "wb") as img_file:
                        for chunk in response.iter_content(1024):
                            img_file.write(chunk)
                            
                    # Sanitize the image using Pillow to prevent MoviePy/PyAV avcodec decode errors
                    with Image.open(image_path) as img:
                        img = img.convert("RGB")
                        img.save(image_path, "JPEG")
                else:
                    print(f"[Step 4 Warning] Failed to fetch image (HTTP {response.status_code}). Engaging fallback.")
                    fallback_needed = True
            except Exception as req_e:
                print(f"[Step 4 Warning] Network/Decode Exception: {req_e}. Engaging fallback.")
                fallback_needed = True
                
            if fallback_needed:
                create_fallback_image(f"Scene {scene_num}: {visual_prompt}", image_path)
                
            # 2. Convert to Video
            print(f"[Step 4] Applying Ken Burns effect for scene {scene_num}...")
            video_filename = f"video_{scene_num:03d}.mp4"
            video_path = os.path.join(project_dir, "video_chunks", video_filename)
            
            success = create_ken_burns_video(image_path, video_path, duration=5.0)
            if not success:
                print(f"[Step 4 Warning] Failed to animate video for scene {scene_num}")
                
        print(f"\n[Step 4] Finished processing {len(scenes)} video files.")
        return True
        
    except json.JSONDecodeError:
        print("[Step 4 Error] Invalid format JSON in story file.")
        return False
    except Exception as e:
         print(f"[Step 4 Error] Unexpected error: {e}")
         return False
