import os
import json
import asyncio
import edge_tts

async def generate_single_audio(text, output_path, voice="en-US-AriaNeural"):
    """Valid Voices (examples): en-US-AriaNeural, en-GB-SoniaNeural, en-GB-RyanNeural"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_audio(project_dir):
    """Reads the story.json and generates an audio file for each scene."""
    print("[Step 3] Starting audio generation using Edge-TTS...")
    story_path = os.path.join(project_dir, "scripts", "story.json")
    
    if not os.path.exists(story_path):
        print(f"[Step 3 Error] Story file not found at {story_path}")
        return False
        
    try:
        with open(story_path, "r", encoding="utf-8") as f:
            story = json.load(f)
            
        scenes = story.get("scenes", [])
        if not scenes:
            print("[Step 3 Error] No scenes found in the story JSON.")
            return False
        
        for scene in scenes:
            scene_num = scene.get("scene_number")
            text = scene.get("narration")
            
            # Format filename (e.g., audio_001.wav or mp3). Edge-tts natively saves an mp3 even if labeled wav, 
            # so we'll just save as .mp3.
            filename = f"audio_{scene_num:03d}.mp3"
            output_path = os.path.join(project_dir, "audio_chunks", filename)
            
            print(f"[Step 3] Generation {scene_num}/{len(scenes)}: {filename}")
            
            # Run the async function synchronously inside the loop
            asyncio.run(generate_single_audio(text, output_path))
            
        print(f"[Step 3] Finished generating {len(scenes)} audio files.")
        return True
        
    except json.JSONDecodeError:
        print("[Step 3 Error] Invalid JSON in story file.")
        return False
    except Exception as e:
         print(f"[Step 3 Error] Unexpected error: {e}")
         return False
