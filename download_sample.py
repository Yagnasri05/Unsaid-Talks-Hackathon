import gdown
import os

url = "https://drive.google.com/file/d/14B3mUgMdapF1b-FJzbswGgKymepGKkfA/view"
output = "temp/sample_video.mp4"

if not os.path.exists("temp"):
    os.makedirs("temp")

try:
    print(f"Downloading {url} to {output}...")
    gdown.download(url, output, quiet=False, fuzzy=True)
    if os.path.exists(output):
        print("Download successful!")
    else:
        print("Download failed (file not created).")
except Exception as e:
    print(f"Error: {e}")
