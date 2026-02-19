import sys
import time

# Import pipeline steps
from step1_init import initialize_project
from step2_story import generate_story
from step3_audio import generate_audio
from step4_video import generate_video
from step5_compose import compose_final_video

def main():
    print("=" * 50)
    print("🎬 Automated Video Generator Pipeline Started")
    print("=" * 50)
    start_time = time.time()
    
    # Step 1: Initialize
    print("\n--- Step 1: Project Initialization ---")
    project_dir = initialize_project()
    if not project_dir:
        print("Pipeline aborted at Step 1.")
        sys.exit(1)
        
    # Step 2: Story Generation
    print("\n--- Step 2: Story Generation ---")
    topic = "Finley the glowing fox who has to return a falling star back to the night sky before sunset."
    story_success = generate_story(project_dir, topic=topic)
    if not story_success:
        print("Pipeline aborted at Step 2.")
        sys.exit(1)
        
    # Step 3: Audio Generation
    print("\n--- Step 3: Audio Generation ---")
    audio_success = generate_audio(project_dir)
    if not audio_success:
        print("Pipeline aborted at Step 3.")
        sys.exit(1)
        
    # Step 4: Video Generation
    print("\n--- Step 4: Video Generation ---")
    video_success = generate_video(project_dir)
    if not video_success:
        print("Pipeline aborted at Step 4.")
        sys.exit(1)
        
    # Step 5: Final Composition
    print("\n--- Step 5: Final Composition ---")
    compose_success = compose_final_video(project_dir)
    if not compose_success:
        print("Pipeline aborted at Step 5.")
        sys.exit(1)
        
    # Finish
    end_time = time.time()
    elapsed = end_time - start_time
    print("\n" + "=" * 50)
    print(f"✅ Pipeline Completed Successfully in {elapsed:.2f} seconds.")
    print(f"📁 Project Data saved in: {project_dir}")
    print("=" * 50)

if __name__ == "__main__":
    main()
