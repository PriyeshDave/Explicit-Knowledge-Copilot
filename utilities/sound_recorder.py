import streamlit as st
import sounddevice as sd
import wavio
import tempfile
import speech_recognition as sr
import os
from gtts import gTTS

# Function to record audio
def record_audio(duration=10, fs=44100):
    st.write(f"Recording for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    return audio, fs

# Save audio to a temporary file
def save_audio(audio, fs):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wavio.write(temp_file.name, audio, fs, sampwidth=2)
    return temp_file.name

# Function to transcribe audio
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file
        try:
            text = recognizer.recognize_google(audio_data)  # Use Google Web Speech API
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"


def input_audio():
    # Input for duration of recording
    # duration = st.slider("Recording duration (seconds)", 1, 10, 5)
    transcript = ''
    start_btn = st.button("Record")
    #play_btn = st.button("Play")

    # Record button
    if start_btn:
        audio, fs = record_audio(duration=10)
        audio_file = save_audio(audio, fs)

        # Play the audio in the Streamlit app
        #st.audio(audio_file, format='audio/wav')
        #st.success("Recording complete!")

        # Transcribe the audio
        transcript = transcribe_audio(audio_file)
        st.subheader("Transcript:")
        st.success(transcript)  # Display the transcription
    
    if transcript != '':
        return transcript.lower()

    # Option to download the file
    # if play_btn and 'audio_file' in locals():
    #     with open(audio_file, "rb") as file:
    #         st.download_button(label="Download audio", data=file, file_name=os.path.basename(audio_file), mime="audio/wav")


def text_to_speech(transcript, output_path="speech_output.mp3"):
    tts = gTTS(text=transcript, lang='en')
    tts.save(output_path)  # Save the speech to an mp3 file
    return output_path