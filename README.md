# Audio-to-Text Converter

A Python web app using Streamlit and Faster-Whisper. It supports recording directly from a microphone and uploading existing audio files.

## Features
- Record audio on the page using the browser microphone
- Upload WAV, MP3, M4A, OGG, FLAC, MP4, or WebM
- Automatic language detection or select English, Hindi, Kannada, Tamil, Telugu, Spanish, French, or German
- Transcribe speech or translate speech to English
- Edit and download the transcript as `.txt`

## Requirements
- Python 3.10–3.12 recommended
- FFmpeg installed and available on PATH
- Internet for the initial model download
- A recent Streamlit version with `st.audio_input`

## Setup

Create and activate a virtual environment:

**Windows PowerShell**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Install FFmpeg:
- Windows: install FFmpeg and add its `bin` folder to PATH.
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`

Run:
```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`. Click the microphone recorder and grant browser permission. Record and stop, then click **Convert to text**.

## How it works
Streamlit captures a browser microphone recording or accepts an uploaded file. Faster-Whisper transcribes the audio locally on the computer running the app. The recognized text is shown in an editable field and can be downloaded.

## Notes
- First use downloads the chosen model.
- `tiny` and `base` are faster; `small` and `medium` can be more accurate but need more resources.
- Browser microphone access generally requires localhost or HTTPS.
- The app does not continuously transcribe while recording; it transcribes after the recording is stopped and you click Convert to text.
