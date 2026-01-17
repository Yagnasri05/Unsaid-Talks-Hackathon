from core.analysis import analyze_video_for_reels

video_path = "temp/sample_video.mp4"
try:
    print("Testing Analysis...")
    clips = analyze_video_for_reels(video_path)
    print("Clips Found:", clips)
except Exception as e:
    print(f"Analysis Failed: {e}")
