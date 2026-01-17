import os
from core.processing import process_video

def test_backend():
    print("Starting backend test...")
    video_path = "temp/sample_video.mp4"
    if not os.path.exists(video_path):
        print(f"Error: {video_path} not found.")
        return
        
    try:
        results = process_video(video_path, output_dir="temp")
        print("\nValues Returned:")
        for res in results:
            print(f"- {res['summary']} (Score: {res['score']}) -> {res['path']}")
            
        if results:
            print("SUCCESS: Backend processed video and generated clips.")
        else:
            print("FAILURE: No clips generated.")
            
    except Exception as e:
        print(f"EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_backend()
