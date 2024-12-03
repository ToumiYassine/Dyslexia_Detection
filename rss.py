import requests

# Clé API
api_key = 'd0c358b22c654be0b25b14b9066210cf'

def recognize_speech(audio_file_path, api_key):
    url = "https://api.voicerss.org/"
    with open(audio_file_path, 'rb') as audio_file:
        audio_content = audio_file.read()
    
    params = {
        'key': api_key,
        'hl': 'en-us',
        'src': audio_content,  # Contenu brut du fichier audio
        'c': 'mp3',  # Format attendu
        'f': '48khz_16bit_stereo',
        'r': '0'
    }
    
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        return response.text  # Le texte transcrit par Voice RSS
    else:
        return f"Error: {response.text}"

# Test
audio_path = r"C:\Users\ASUS-MSi\Desktop\Dyslexia_Detection-main\aaa.mp3"  # Chemin du fichier MP3
print(recognize_speech(audio_path, api_key))
