import os
from moviepy import VideoFileClip
from core.analysis import analyze_video_for_reels
from core.cropping import get_face_centers, smooth_centers

def process_video(video_path, output_dir="temp"):
    """
    Main pipeline:
    1. Analyze video for best clips.
    2. detailed smart cropping on those clips.
    3. Export.
    """
    # 1. Analyze
    print("Analyzing video content...")
    clips_metadata = analyze_video_for_reels(video_path)
    
    if not clips_metadata:
        print("No clips found or error in analysis.")
        return []
        
    generated_files = []
    
    # Load Main Video
    original_video = VideoFileClip(video_path)
    W, H = original_video.size
    
    # Target Aspect Ratio 9:16
    target_ratio = 9/16
    target_width = int(H * target_ratio)
    target_height = H
    
    if target_width > W:
        # If video is too narrow, we scale based on width
        target_width = W
        target_height = int(W / target_ratio)
        # Verify height doesn't exceed source
        if target_height > H:
             # This is a weird case, but let's stick to height constraint
             target_height = H
             target_width = int(H * target_ratio)
    
    # Pre-calculate face centers for the WHOLE video? 
    # Optimization: Only calculate for the clips we need.
    # However, for simplicity and context (smoothing), let's calculate per clip or assume we can do it fast enough.
    # Let's do it per clip to save time if video is 1 hour long.
    
    for i, clip_data in enumerate(clips_metadata):
        start = clip_data['start_seconds']
        end = clip_data['end_seconds']
        
        # Buffer
        start = max(0, start)
        end = min(original_video.duration, end)
        
        if end - start < 5: # Skip too short clips
            continue
            
        print(f"Processing Clip {i+1}: {clip_data['summary']} ({start}-{end})")
        
        # Subclip
        subclip = original_video.subclip(start, end)
        
        # Create a temp file for the subclip to process with opencv more easily (MoviePy sometimes slow with frame access on subclips of long files)
        # OR just iterate the subclip frames directly.
        
        # For Smart Cropping:
        # We need a function `crop(t)` that returns (x1, y1, x2, y2) or (x, y) center.
        # MoviePy's crop(x_center=..., width=..., height=...) accepts a function of t.
        
        # To make this efficient, we pre-calculate the centers for this subclip.
        # We can write the subclip to a temp file first to run MediaPipe on it reliably.
        temp_clip_path = os.path.join(output_dir, f"temp_clip_{i}.mp4")
        subclip.write_videofile(temp_clip_path, codec="libx264", audio_codec="aac")
        
        # Get Centers
        centers = get_face_centers(temp_clip_path)
        smoothed = smooth_centers(centers, window_size=15) # 0.5s smoothing (assuming 30fps)
        
        # Define crop function
        def get_center(t):
            frame_index = int(t * subclip.fps)
            frame_index = min(frame_index, len(smoothed) - 1)
            
            center_x = smoothed[frame_index]
            
            # Clamp center
            half_width = target_width / 2
            
            # Ensure crop box stays within bounds
            if center_x - half_width < 0:
                center_x = half_width
            if center_x + half_width > W:
                center_x = W - half_width
                
            return center_x

        # Reload the temp clip to apply crop
        clip_to_crop = VideoFileClip(temp_clip_path) 
        
        final_clip = clip_to_crop.crop(
            width=target_width, 
            height=target_height, 
            x_center=get_center
        )
        
        # Resize to standard 1080x1920 (TikTok/Reels HD)?
        # Or just keep the crop. Let's resize for consistency.
        final_clip = final_clip.resize(height=1920) # Width will automatically be 1080
        
        output_filename = os.path.join(output_dir, f"reel_{i+1}_{clip_data['summary'][:30].replace(' ', '_')}.mp4")
        final_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
        
        generated_files.append({
            "path": output_filename,
            "summary": clip_data['summary'],
            "score": clip_data['virality_score']
        })
        
        # Clean up temp
        clip_to_crop.close()
        os.remove(temp_clip_path)
        
    original_video.close()
    return generated_files
