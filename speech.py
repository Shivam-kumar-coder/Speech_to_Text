import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr
import av
import numpy as np
import queue

st.title("🎤 Hosted Speech to Text Converter")

# Global queue to collect audio
audio_queue = queue.Queue()

# AudioProcessor class
class AudioProcessor(AudioProcessorBase):
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray().flatten().astype(np.int16).tobytes()
        audio_queue.put(audio)
        return frame

# Start mic recording
webrtc_streamer(key="speech", audio_processor_factory=AudioProcessor)

# Convert voice to text
if st.button("Convert to Text"):
    recognizer = sr.Recognizer()
    try:
        audio_data = b''.join(list(audio_queue.queue))
        with sr.AudioFile(sr.AudioData(audio_data, 16000, 2)) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            st.success(f"Recognized Text: {text}")
    except Exception as e:
        st.error(f"Error: {e}")



