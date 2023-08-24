import os
import time
import pyaudio
import speech_recognition as sr
import playsound 
from gtts import gTTS
import openai
# from englisttohindi.englisttohindi import EngtoHindi

api_key = "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"

lang ='en'

openai.api_key = api_key


guy = ""

while True:
    def get_adio():
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            audio = r.listen(source)
            said = ""
            try:
                said = r.recognize_google(audio)
                print(said)
                global guy 
                guy = said
                

                if "Friday" in said:
                    words = said.split()
                    new_string = ' '.join(words[1:])
                    print(new_string) 
                    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content":said}])
                    respond = completion.choices[0].message.content
                    print(respond)
                    text = respond

                    # # message to be translated
                    # message = respond
                    # # creating a EngtoHindi() object
                    # res = EngtoHindi(message) 
                    # # displaying the translation
                    # print(res.convert)
                    # text = res.convert

                    speech = gTTS(text = text, lang=lang, slow=False, tld="com.au")
                    speech.save("welcome1.mp3")
                    playsound.playsound("welcome1.mp3")
                    print("Next command Master")
                    
            except Exception:
                print("Please say something")

        return said

    if "stop" in guy:
        break


    get_adio()
