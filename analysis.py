import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def upload_to_gemini(path):
    """Uploads the given file to Gemini."""
    print(f"Uploading file: {path}")
    video_file = genai.upload_file(path=path)
    print(f"Completed upload: {video_file.uri}")
    
    # Check state and wait for it to be active
    while video_file.state.name == "PROCESSING":
        print("Processing video...")
        time.sleep(5)
        video_file = genai.get_file(video_file.name)
        
    if video_file.state.name == "FAILED":
        raise ValueError("Video processing failed.")
        
    print(f"Video is active: {video_file.name}")
    return video_file

def analyze_video_for_reels(video_path):
    """
    Analyzes the video using Gemini 1.5 Pro to identify 3 viral reels.
    Returns a list of dictionaries with 'start', 'end', 'summary', and 'virality_score'.
    """
    try:
        video_file = upload_to_gemini(video_path)
        
        # Create the prompt
        prompt = """
        Analyze this video and identify the 3 most viral, engaging, and "aha" moments suitable for TikTok/Instagram Reels.
        Focus on emotional peaks, funny moments, or profound wisdom ("golden nuggets").
        
        Return the response as a JSON list of objects. Each object must have:
        - "start_time": The start timestamp of the clip in "MM:SS" format.
        - "end_time": The end timestamp of the clip in "MM:SS" format.
        - "summary": A catchy title/summary for the clip.
        - "virality_score": A score from 1-10 on how viral this clip could be.
        
        Ensure the clips are between 30 and 60 seconds long.
        Example output format:
        [
            {"start_time": "00:10", "end_time": "00:50", "summary": "The secret to success", "virality_score": 9},
            ...
        ]
        """
        
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        
        print("Sending request to Gemini...")
        response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
        
        print("Raw response from Gemini:")
        print(response.text)
        
        # Clean up the markdown code blocks if present
        text = response.text.replace("```json", "").replace("```", "").strip()
        
        try:
            clips = json.loads(text)
            # Normalize timestamps to seconds
            for clip in clips:
                clip['start_seconds'] = parse_time(clip['start_time'])
                clip['end_seconds'] = parse_time(clip['end_time'])
                # Duration check/clamping if needed, but we trust the model mostly
            return clips
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return []
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def parse_time(time_str):
    """Converts MM:SS to seconds."""
    parts = time_str.split(':')
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0
