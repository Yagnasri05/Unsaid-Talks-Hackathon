# PulsePoint AI

PulsePoint AI is a content repurposing tool that takes long-form video content and automatically generates 3-5 high-impact, vertical reels suitable for TikTok, Instagram Reels, and YouTube Shorts.

## Features

- **Automated Clip Selection**: Uses Google Gemini AI and audio analysis to find the most engaging moments (emotional peaks, interesting topics).
- **Smart Cropping**: Uses MediaPipe Face Detection to automatically crop horizontal video to vertical (9:16) while keeping the speaker centered.
- **Easy Interface**: Built with Streamlit for a simple drag-and-drop experience.

## Setup

1.  **Clone/Download** the repository.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables**:
    Create a `.env` file and add your Google Studio API Key:
    ```
    GOOGLE_API_KEY=YOUR_API_KEY_HERE
    ```
4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## Usage

1.  Upload a video file (MP4, MOV, etc.).
2.  Click "Generate Pulse Reels".
3.  Wait for the processing to complete.
4.  Preview and download the generated clips.

## Tech Stack

-   **Frontend**: Streamlit
-   **AI/LLM**: Google Gemini 2.5 Pro (via `google-generativeai`)
-   **Computer Vision**: MediaPipe (Face Detection)
-   **Audio Processing**: Librosa
-   **Video Editing**: MoviePy


