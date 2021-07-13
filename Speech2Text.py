# Import Required Libraries and Functions
import speech_recognition as sr

# Create Speech Recognizer
r = sr.Recognizer()

# [ Function to Detect Speech and Convert it into Text ]
def speech2Text():
    with sr.Microphone() as source:
        audio = r.record(source,duration=4) # Record audio
        try:
            text = r.recognize_google(audio) # Convert Audio to Text
            return text
        except:
            return -1
    
if __name__=='__main__':
    text = speech2Text()
    if text == -1:
        print("Sorry didn't get you, Please Try Again")
    else:
        print(text)