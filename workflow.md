## It is automated video generation project and post on the youtube channel.

# 1. Initialization: 
- Creating video project directory with 4 sub-directories for scripts, audio_chunks, video_chunks, and final_render.

# 2. Find the best LLM model.
- To generate the video for the script for free of cost from the Open Router. API key is already available in the .env file.

# 3. Master Scripting & Storyboarding (via OpenRouter): 
- An LLM generates a cohesive fairy tale. 
- Since a 10-minute video requires about 120 individual 5-second chunks, the LLM must generate a highly structured JSON file mapping out exactly 120 scenes, including the narrator's text and a specific visual prompt for each.

# 4. Audio Generation (via TTS API): 
- A Python script iterates through the JSON, sending the text of each scene to a free Text-to-Speech API, saving them sequentially (e.g., audio_001.wav).

# 5. Video Generation (via Image Generation + Ken Burns Animation): 
- The script sends the visual prompts to a free, high-quality Image Generation API (e.g., Pollinations AI) to generate a static scene image.
- Using MoviePy, the static image is animated with a subtle 5-second zoom/pan (Ken Burns effect) to create a video clip, saving them sequentially (video_001.mp4).

# 6. Composition: 
- Using a programmatic video editor (MoviePy), the system iterates through the generated audio and video chunks in the workspace directories.
- It overlays each audio scene (MP3) onto its corresponding video scene (MP4).
- Finally, it concatenates all the individual audio-video chunks into a seamless, finalized complete video file and exports it to the `final_render` directory.