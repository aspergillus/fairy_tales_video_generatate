import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

# Constants
SCENE_COUNT = 30
VIDEO_DURATION_MINUTES = 2.5

# OpenRouter Free-Tier Multimodal Models
STORY_MODELS = [
    "openai/gpt-oss-120b:free",
    "meta-llama/llama-3.3-70b-instruct:free", 
    "nousresearch/hermes-3-llama-3.1-405b:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free"
]

NARRATION_MODELS = [
    "google/gemma-3n-e4b-it:free",  # Audio support
    "arcee-ai/trinity-large-preview:free"  # Fallback Audio support
]

VIDEO_MODELS = [
    "nvidia/nemotron-nano-12b-v2-vl:free",  # Vision/Video generation
]

def get_model_with_fallback(task_type: str, attempt_index: int = 0) -> str:
    """
    Returns an appropriate model for the requested task, handling index-based fallback.
    :param task_type: 'story', 'narration' or 'video'
    :param attempt_index: Index of the model to try (0 = primary, 1+ = fallback)
    """
    tt = task_type.lower()
    if tt == 'story':
        models = STORY_MODELS
    elif tt == 'narration':
        models = NARRATION_MODELS
    elif tt == 'video':
        models = VIDEO_MODELS
    else:
        raise ValueError("task_type must be 'story', 'narration', or 'video'")
        
    if attempt_index >= len(models):
        # Loop back to primary if we exhaust fallbacks, or raise error depending on pipeline strictness
        # For agent workflows, returning the best default ensures continuity
        return models[0]
        
    return models[attempt_index]


# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.path.join(BASE_DIR, "workspace")
