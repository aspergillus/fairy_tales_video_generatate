import os
import json
import requests
import sys

# Ensure config can be imported from parent
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import config

def generate_story(project_dir, topic="A brave little fox named Finley on a magical starry adventure."):
    """Generates a 120-scene story using OpenRouter's API."""
    print(f"[Step 2] Generating story about '{topic}'...")
    
    if not config.OPEN_ROUTER_API_KEY:
        print("[Step 2 Error] OPEN_ROUTER_API_KEY is not set in the environment.")
        return False
        
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.OPEN_ROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = (
        "You are an expert children's storyteller and AI video prompt engineer. "
        "Objective: Write a highly engaging fairy tale script for kids, and format the output "
        "as a precise storyboard designed for an automated video generation pipeline. "
        "Constraints: "
        f"- The total story must be exactly {config.VIDEO_DURATION_MINUTES} minutes long when spoken at a moderate pace. "
        f"- You must break the story into exactly {config.SCENE_COUNT} sequential 5-second chunks. "
        "- Output strictly in valid JSON format without markdown wrapping. "
        "- Each chunk must contain two keys: narration (the words spoken in that 5-second window) and "
        "visual_prompt (a detailed, literal description of the scene for a Text-to-Video AI). "
        "JSON Schema: {\"title\": \"Story Name\", \"scenes\": [{\"scene_number\": 1, \"narration\": \"...\", \"visual_prompt\": \"...\"}, ... ]}"
    )
    
    # Try up to the number of available models
    max_attempts = len(config.STORY_MODELS) if hasattr(config, 'STORY_MODELS') else 1
    
    for attempt in range(max_attempts):
        model_id = config.get_model_with_fallback('story', attempt_index=attempt)
        print(f"[Step 2 Info] Attempt {attempt+1}/{max_attempts} using model: {model_id}")
        
        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Topic: {topic}"}
            ],
            "temperature": 0.7,
            "max_tokens": 8192
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            if not response.ok:
                print(f"[Step 2 Warning] API responded with {response.status_code}: {response.text}")
                if response.status_code in [429, 502, 503, 504]:
                    continue # Try next model
            response.raise_for_status()
            
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            # Clean up potential markdown wrapping if the LLM ignores instructions
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            # Parse and save JSON
            story_data = json.loads(content.strip())
            story_path = os.path.join(project_dir, "scripts", "story.json")
            
            with open(story_path, "w", encoding="utf-8") as f:
                json.dump(story_data, f, indent=2)
                
            print(f"[Step 2] Story generated and saved to {story_path}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"[Step 2 Warning] API Request failed on attempt {attempt+1}: {e}")
            if attempt == max_attempts - 1:
                print("[Step 2 Error] All models exhausted.")
                return False
        except json.JSONDecodeError as e:
            print(f"[Step 2 Warning] Failed to parse API output as JSON on attempt {attempt+1}: {e}")
            # Save raw output for debugging
            raw_path = os.path.join(project_dir, "scripts", f"story_raw_attempt_{attempt+1}.txt")
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(content if 'content' in locals() else str(response.text))
            print(f"[Step 2 Info] Raw output saved to {raw_path}")
            # Try the next model
            if attempt == max_attempts - 1:
                print("[Step 2 Error] All models exhausted and returned invalid JSON.")
                return False
            continue
        except Exception as e:
            print(f"[Step 2 Error] An unexpected error occurred: {e}")
            return False
            
    return False
