import os
import json
import requests
import config

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
        "Objective: Write a highly engaging, 10-minute long fairy tale script for kids, and format the output "
        "as a precise storyboard designed for an automated video generation pipeline. "
        "Constraints: "
        "- The total story must be exactly 10 minutes long when spoken at a moderate pace. "
        "- You must break the story into exactly 120 sequential 5-second chunks. "
        "- Output strictly in valid JSON format without markdown wrapping. "
        "- Each chunk must contain two keys: narration (the words spoken in that 5-second window) and "
        "visual_prompt (a detailed, literal description of the scene for a Text-to-Video AI). "
        "JSON Schema: {\"title\": \"Story Name\", \"scenes\": [{\"scene_number\": 1, \"narration\": \"...\", \"visual_prompt\": \"...\"}, ... ]}"
    )
    
    payload = {
        "model": config.OPEN_ROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Topic: {topic}"}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
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
        print(f"[Step 2 Error] API Request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"[Step 2 Error] Failed to parse API output as JSON: {e}")
        # Save raw output for debugging
        raw_path = os.path.join(project_dir, "scripts", "story_raw.txt")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(content if 'content' in locals() else str(response.text))
        print(f"[Step 2 Info] Raw output saved to {raw_path}")
        return False
    except Exception as e:
        print(f"[Step 2 Error] An unexpected error occurred: {e}")
        return False
