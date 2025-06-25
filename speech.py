import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings
import av
import numpy as np
import queue
import speech_recognition as sr

st.title("🎙️ Voice to Text (No Camera)")

# Queue to hold audio frames
audio_queue = queue.Queue()

# Audio Processor
class AudioProcessor(AudioProcessorBase):
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray().flatten().astype(np.int16).tobytes()
        audio_queue.put(audio)
        return frame

# Audio-only settings
client_settings = ClientSettings(
    media_stream_constraints={
        "video": False,
        "audio": True
    },
    rtc_configuration={}
)

# Stream from mic
webrtc_streamer(
    key="speech-to-text",
    client_settings=client_settings,
    audio_processor_factory=AudioProcessor
)

# Convert to text
if st.button("🎧 Convert Voice to Text"):
    recognizer = sr.Recognizer()
    try:
        audio_data = b''.join(list(audio_queue.queue))
        if audio_data:
            # Note: 16000 Hz sample rate, 2 bytes (16 bit) sample width
            audio = sr.AudioData(audio_data, sample_rate=16000, sample_width=2)
            text = recognizer.recognize_google(audio)
            st.success(f"📝 Transcribed Text: {text}")
        else:
            st.warning("⚠️ No audio captured. Please speak and try again.")
    except Exception as e:
        st.error(f"❌ Error: {e}")



