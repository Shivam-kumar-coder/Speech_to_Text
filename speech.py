import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import numpy as np
import queue
import speech_recognition as sr

st.title("🎤 Hosted Speech to Text Converter")

audio_queue = queue.Queue()

class AudioProcessor(AudioProcessorBase):
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray().flatten().astype(np.int16).tobytes()
        audio_queue.put(audio)
        return frame

webrtc_streamer(key="speech", audio_processor_factory=AudioProcessor)

if st.button("Convert to Text"):
    recognizer = sr.Recognizer()
    try:
        audio_data = b''.join(list(audio_queue.queue))
        if audio_data:
            audio = sr.AudioData(audio_data, sample_rate=16000, sample_width=2)
            text = recognizer.recognize_google(audio)
            st.success(f"Recognized Text: {text}")
        else:
            st.warning("No audio data captured yet.")
    except Exception as e:
        st.error(f"Error: {e}")


