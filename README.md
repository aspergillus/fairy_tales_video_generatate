# Fairy Tales Video Generator

An automated pipeline designed to generate enchanting 10-minute fairy tale videos for kids. This project streamlines the process of creating engaging children's stories by converting scripts into detailed storyboards, breaking them down into 5-second chunks for a seamless video generation workflow.

## Detailed Description

Creating captivating and high-quality video content for children requires careful planning of visuals and narration. The **Fairy Tales Video Generator** simplifies this process by producing a structured storyboard from a fairy tale script. 

The core of the system takes a whimsical story and divides it into precise 5-second intervals. For each interval, it generates two crucial components:
1. **Narration:** The spoken dialogue or storytelling meant to be heard during that chunk.
2. **Visual Prompt:** A highly specific, vivid description of the scene that visual generation models (like Midjourney, DALL-E, or Stable Diffusion/video models) can use to create the accompanying animations or images.

The output from this pipeline is formatted in a strict, valid JSON schema, making it perfectly suited for automated ingestion by text-to-image/video and text-to-speech tools, thus enabling an end-to-end automated video production line.

## Automated Workflow

The video generation process follows a systematic workflow to ensure consistency and quality:

1. **Script Ingestion & Parsing:**
   - The system receives a base fairy tale script.
   - It analyzes the pacing and content to optimally divide the story into 10-minute appropriate segments.

2. **Chunking & Storyboarding (The 5-Second Rule):**
   - The script is segmented into 5-second blocks, which is the ideal duration for maintaining visual interest for kids' content.
   - For each block, the system pairs the corresponding script lines (Narration) with detailed art directions (Visual Prompts).

3. **Prompt Engineering:**
   - The visual prompts are carefully engineered to include consistent character descriptions, art styles (e.g., 3D Pixar style, watercolor, vibrant), lighting, and camera angles.

4. **JSON Structuring:**
   - All extracted data is compiled into a predefined JSON schema.
   - Example schema structure:
     ```json
     {
       "story_title": "...",
       "chunks": [
         {
           "timestamp": "00:00-00:05",
           "narration": "Once upon a time in a magic forest...",
           "visual_prompt": "A lush, glowing magic forest with giant colorful mushrooms, soft sunlight filtering through the canopy, vivid colors, 3D animation style, cinematic lighting."
         }
       ]
     }
     ```

5. **Downstream Integration (Execution):**
   - The JSON output is sent to a Text-to-Speech (TTS) engine to generate the voiceover for the `narration`.
   - The `visual_prompt` is sent to an AI Image/Video generator to create the scene.
   - Finally, the audio and visual assets are stitched together chronologically to form the final 10-minute fairy tale video.
