import gradio as gr
import speech_recognition as sr
from gtts import gTTS
from transformers import pipeline
# Modèle de NLP pour générer des réponses
import google.generativeai as genai

genai.configure(api_key="AIzaSyCwIh3QHFIiTdpgi2QAkmD_dfrQcJ0A13w")
model = genai.GenerativeModel("gemini-1.5-flash")
#print(response.text)
#chatbot = pipeline("text-generation", model="gpt-2" , use_auth_token="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")

# Fonction pour reconnaître la parole
def recognize_speech(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data)

# Fonction principale
def assistant(audio):
    text = recognize_speech(audio)
    response = model.generate_content(text)
    tts = gTTS(response.text, lang="fr")
    tts.save("response.mp3")
    return response, "response.mp3"

# Interface Gradio
interface = gr.Interface(
    fn=assistant,
    inputs = gr.Audio(type="filepath"),
    outputs=["text", "audio"],
    live=True,
    title="Assistant IA pour les élèves dyslexiques",
    description="Pose une question, l'assistant répond avec une voix adaptée."
)

interface.launch()
