# Import Required Libraries and Functions
from gtts import gTTS
from playsound import playsound

# [ Function to Dictate Message ]
def dictate(text):
    output = gTTS(text = text) # Converting Text to Speech
    output.save('audio_files/message.mp3') # Saving Speech
    playsound('audio_files/message.mp3') # Playing the Saved Speech
