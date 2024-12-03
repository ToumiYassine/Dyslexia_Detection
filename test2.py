import streamlit as st
from gtts import gTTS
import speech_recognition as sr
from difflib import SequenceMatcher
import os
import tempfile

# Function to Text-to-Speech (using gTTS)
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    # Save the audio file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
        tts.save(tmpfile.name)
        st.audio(tmpfile.name)

# Function to Split Word into Syllables (Simple Example)
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

# Function for Pronunciation Scoring
def calculate_similarity(word1, word2):
    return SequenceMatcher(None, word1.lower(), word2.lower()).ratio()

# Streamlit UI
st.title("Teaching Assistant for Dyslexic Students")
st.markdown("**Theme: Environment and Recycling**")

# Example Exercise
exercise = "Listen and pronounce the word: pollution."
word_to_pronounce = "pollution"
st.write(exercise)

# Text-to-Speech
if st.button("Listen to the Question"):
    text_to_speech(exercise)

# Speech Input
st.markdown("### Pronounce the word:")
if st.button("Start Recording"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            student_response = recognizer.recognize_google(audio)
            st.write(f"You said: {student_response}")
            similarity = calculate_similarity(word_to_pronounce, student_response)
            if similarity > 0.8:
                st.success("Great! You pronounced it correctly.")
            else:
                st.error("Almost there! Here's help:")
                syllables = split_word(word_to_pronounce)
                st.write(f"Word split into syllables: **{syllables}**")
                text_to_speech(f"The word is {word_to_pronounce}. Let me help you spell it: {syllables}.")
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand that. Please try again.")
        except sr.RequestError:
            st.error("Speech recognition service error.")

st.markdown("---")
st.write("Once you master pronunciation, you can move to the next exercise!")
