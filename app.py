
import os
import tempfile
from pathlib import Path

import streamlit as st
from faster_whisper import WhisperModel

st.set_page_config(
    page_title="Audio to Text",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Audio-to-Text Converter")
st.write("Record speech with your microphone or upload an audio file.")

# Sidebar settings
with st.sidebar:
    st.header("Transcription settings")

    model_size = st.selectbox(
        "Model size",
        ["tiny", "base", "small", "medium"],
        index=1
    )

    language_choice = st.selectbox(
        "Audio language",
        [
            "Auto-detect", "English", "Hindi", "Kannada",
            "Tamil", "Telugu", "Spanish", "French", "German"
        ]
    )

    task = st.selectbox(
        "Output",
        ["Transcribe audio", "Translate to English"]
    )

# Microphone recording
st.subheader("1. Record with your microphone")
recorded_audio = st.audio_input("Record audio")

# Audio upload
st.subheader("2. Or upload an audio file")
uploaded_audio = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3", "m4a", "ogg", "flac", "mp4", "webm"]
)

audio_source = (
    recorded_audio
    if recorded_audio is not None
    else uploaded_audio
)

filename = (
    "microphone_recording.wav"
    if recorded_audio is not None
    else uploaded_audio.name if uploaded_audio is not None
    else None
)

LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Spanish": "es",
    "French": "fr",
    "German": "de"
}

if audio_source is not None:
    st.audio(audio_source)

    if recorded_audio is not None:
        st.caption("Source: microphone recording")
    else:
        st.caption(f"Source: {filename}")

    if st.button(
        "Convert to text",
        type="primary",
        use_container_width=True
    ):
        temp_path = None

        try:
            suffix = Path(filename).suffix or ".wav"

            # Save audio temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:
                temp_file.write(audio_source.getvalue())
                temp_path = temp_file.name

            # Load model and transcribe
            with st.spinner(
                f"Loading {model_size} model and transcribing audio..."
            ):
                model = WhisperModel(
                    model_size,
                    device="cpu",
                    compute_type="int8"
                )

                language = (
                    None
                    if language_choice == "Auto-detect"
                    else LANGUAGE_CODES[language_choice]
                )

                task_name = (
                    "translate"
                    if task == "Translate to English"
                    else "transcribe"
                )

                segments, info = model.transcribe(
                    temp_path,
                    language=language,
                    task=task_name,
                    vad_filter=True
                )

                segments = list(segments)

                transcript = " ".join(
                    segment.text.strip()
                    for segment in segments
                ).strip()

            # Display transcript
            if transcript:
                st.success("Transcription complete")
                st.subheader("Recognized text")

                edited_transcript = st.text_area(
                    "Edit or copy your transcript",
                    value=transcript,
                    height=240
                )

                st.download_button(
                    "Download transcript (.txt)",
                    data=edited_transcript,
                    file_name=(
                        f"{Path(filename).stem}_transcript.txt"
                    ),
                    mime="text/plain",
                    use_container_width=True
                )

                with st.expander("Transcription details"):
                    st.write(f"Detected language: {info.language}")
                    st.write(
                        f"Language probability: "
                        f"{info.language_probability:.1%}"
                    )
                    st.write(
                        f"Audio duration: {info.duration:.1f} seconds"
                    )
                    st.write(f"Model: {model_size}")

            else:
                st.warning(
                    "No speech was detected. "
                    "Try recording again in a quiet place."
                )

        except TypeError as exc:
            st.error("An audio-library version conflict was detected.")

            st.markdown("""
            Run these commands in your project terminal:

            ```bash
            python -m pip uninstall -y av faster-whisper
            python -m pip install --no-cache-dir "faster-whisper==1.1.1" "av==12.3.0"
            ```

            Then restart Streamlit.
            """)

            st.caption(f"Technical details: {exc}")

        except Exception as exc:
            st.error("The audio could not be transcribed.")
            st.write(
                "Check the audio format and installed dependencies."
            )
            st.caption(f"{type(exc).__name__}: {exc}")

        finally:
            # Remove temporary audio file
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

st.divider()

st.caption(
    "Transcription runs locally after the speech model is downloaded. "
    "The first run may take longer."
)
