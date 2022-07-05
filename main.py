import speech_recognition as sr
from models import Text

try:
    r = sr.Recognizer()
    with sr.Microphone() as input:
        print("recording is progress...")
        audio = r.listen(input)
        text = r.recognize_google(audio, language='en-EN')
        print(text)
        text_correct = Text("this is what I need to do")
        if text == text_correct.text:
            print("correct")
        else:
            print("falied")

except Exception as e:
    print(e)