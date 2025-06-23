import streamlit as st  
import speech_recognition as sr 
st.title("speech to text convertor ")

#if st.button('speech to text convertor')
recog=sr.Recognizer()
mic=sr.Microphone()
ut=st.button("Start Now")
if ut:
    with mic as source:
        st.info("Please Speak")
        audio=recog.listen(source)
        try:
            text=recog.recognize_google(audio)
            st.success(f'Text is:{text}')
        except:
            st.error(" Error Plesase Try again")
        finally:
            st.write("processing complete")
