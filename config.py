import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

# Constants
SCENE_COUNT = 120
VIDEO_DURATION_MINUTES = 10
OPEN_ROUTER_MODEL = "openai/gpt-3.5-turbo" # Defaulting for fast structured JSON generation
