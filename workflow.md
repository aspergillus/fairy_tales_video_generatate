## It is automated video generation project and post on the youtube channel.

# 1. Initialization: 
Initializing directories for scripts, audio_chunks, video_chunks, and final_render.

# 2. Find the best LLM model.
- To generate the video for the script for free of cost from the Open Router. API key is already available in the .env file.

# 3. Master Scripting & Storyboarding (via OpenRouter): 
- An LLM generates a cohesive fairy tale. 
- Since a 10-minute video requires about 120 individual 5-second chunks, the LLM must generate a highly structured JSON file mapping out exactly 120 scenes, including the narrator's text and a specific visual prompt for each.

# 4. Audio Generation (via TTS API): 
- A Python script iterates through the JSON, sending the text of each scene to a free Text-to-Speech API, saving them sequentially (e.g., audio_001.wav).

# 5. Video Generation (via Video API): 
- The script sends the visual prompts to a Text-to-Video API capable of 5-second generations, saving them sequentially (video_001.mp4).

# 6. Composition: 
- Using a programmatic video editor like FFmpeg or MoviePy, the system concatenates the video chunks, overlays the sequential audio, and exports the final 10-minute file.