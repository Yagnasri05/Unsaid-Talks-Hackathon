import streamlit as st
import os
import gdown
from core.processing import process_video

st.set_page_config(page_title="PulsePoint AI", layout="wide")

st.title("PulsePoint AI ⚡")
st.markdown("### Turn long videos into viral reels automatically.")

# Sidebar
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Google API Key", type="password", help="Enter your Gemini API Key if not set in .env")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

# Main Area
tab1, tab2 = st.tabs(["Upload Video", "Use Drive Link"])

video_path = None

with tab1:
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
    if uploaded_file is not None:
        # Save to temp
        video_path = os.path.join("temp", uploaded_file.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded: {uploaded_file.name}")

with tab2:
    drive_url = st.text_input("Enter Google Drive Link")
    if drive_url:
        if st.button("Download from Drive"):
            try:
                output_path = os.path.join("temp", "downloaded_video.mp4")
                st.info("Downloading...")
                # gdown logic
                gdown.download(drive_url, output_path, quiet=False, fuzzy=True)
                if os.path.exists(output_path):
                    st.success("Download Complete")
                    video_path = output_path
                else:
                    st.error("Download failed.")
            except Exception as e:
                st.error(f"Error downloading: {e}")

if video_path and os.path.exists(video_path):
    st.video(video_path)
    
    if st.button("Generate Pulse Reels 🚀", type="primary"):
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("Please provide a Google API Key.")
        else:
            with st.status("Processing video...", expanded=True) as status:
                st.write("Analyzing content with Gemini AI...")
                # Create a placeholder for logs if needed
                
                try:
                    results = process_video(video_path, output_dir="temp")
                    
                    if not results:
                        status.update(label="Analysis failed.", state="error")
                        st.error("No clips generated. Check logs.")
                    else:
                        status.update(label="Processing complete!", state="complete")
                        
                        st.divider()
                        st.subheader("Generated Reels")
                        
                        cols = st.columns(len(results))
                        for i, result in enumerate(results):
                            with cols[i]:
                                st.markdown(f"**{result['summary']}**")
                                st.caption(f"Virality Score: {result['score']}/10")
                                st.video(result['path'])
                                
                                with open(result['path'], "rb") as file:
                                    st.download_button(
                                        label="Download Reel",
                                        data=file,
                                        file_name=os.path.basename(result['path']),
                                        mime="video/mp4"
                                    )
                                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    status.update(label="Error occurred", state="error")
