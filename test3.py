import streamlit as st
import requests
from gtts import gTTS
from difflib import SequenceMatcher
import tempfile
from transformers import pipeline
import os

# Set FFmpeg path for audio processing (if necessary)
os.environ["FFMPEG_BINARY"] = r"C:\ffmpeg\bin\ffmpeg.exe"  # Path to your ffmpeg executable

# Initialize Whisper pipeline for speech recognition
whisper = pipeline('automatic-speech-recognition', model='openai/whisper-medium', device=-1)

# Function to convert text to speech using gTTS
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
        tts.save(tmpfile.name)
        st.audio(tmpfile.name)  # Play the generated speech

# Function to split a word into syllables (simplified approach)
def split_word(word):
    vowels = "aeiou"
    syllables = []
    current = ""
    for char in word:
        current += char
        if char in vowels:
            syllables.append(current)
            current = ""
    if current:
        syllables.append(current)
    return " - ".join(syllables)

# Function to calculate pronunciation similarity between two words
def calculate_similarity(word1, word2):
    return SequenceMatcher(None, word1.lower(), word2.lower()).ratio()

# Function to recognize speech using Whisper (from uploaded audio)
def recognize_speech_with_whisper(audio_file_path):
    # Use Whisper to transcribe the speech in the audio file
    transcription = whisper(audio_file_path)
    return transcription['text']

# Streamlit UI setup
st.title("Teaching Assistant for Dyslexic Students")
st.markdown("**Theme: Environment and Recycling**")

# Example exercise for the user
exercise = "Listen and pronounce the word: pollution."
word_to_pronounce = "pollution"
st.write(exercise)

# Button to listen to the question (text-to-speech)
if st.button("Listen to the Question"):
    text_to_speech(exercise)

# Prompt user to upload their pronunciation of the word
st.markdown("### Pronounce the word:")
audio_file = st.file_uploader("Upload your audio", type=["wav"])

if audio_file:
    st.write("Analyzing your pronunciation...")
    
    # Save the uploaded audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name  # Path of temporary audio file
        
        # Recognize the speech using Whisper model
        transcribed_text = recognize_speech_with_whisper(temp_audio_path)
        st.write(f"You said: {transcribed_text}")

        # Compare the transcribed text with the correct word
        similarity = calculate_similarity(word_to_pronounce, transcribed_text)
        
        # Provide feedback based on pronunciation similarity
        if similarity > 0.8:
            st.success("Great! You pronounced it correctly.")
        else:
            st.error("Almost there! Here's help:")
            syllables = split_word(word_to_pronounce)  # Split the word into syllables
            st.write(f"Word split into syllables: **{syllables}**")
            text_to_speech(f"The word is {word_to_pronounce}. Let me help you spell it: {syllables}.")

# Footer
st.markdown("---")
st.write("Once you master pronunciation, you can move to the next exercise!")
