import speech_recognition as sr
import webbrowser
import pyttsx3
import pygame
import os
from openai import OpenAI
from gtts import gTTS
# import musiclibrary  # Uncomment only if you have a valid dictionary

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def aiprocess(command):
    client = OpenAI(api_key='sk-proj-your-key-here')  # Use a valid API key

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google. Give short responses please."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

def processcommand(c):
    c = c.lower()
    if 'open google' in c:
        webbrowser.open('https://google.com')
    elif 'open youtube' in c:
        webbrowser.open('https://youtube.com')
    elif 'open linkedin' in c:
        webbrowser.open('https://linkedin.com')
    elif c.startswith("play"):
        song = c.split(" ")[1]
        try:
            link = musiclibrary.music[song]  # Only if musiclibrary is defined
            webbrowser.open(link)
        except Exception as e:
            speak("Sorry, I couldn't find that song.")
    else:
        output = aiprocess(c)
        speak(output)

if __name__ == '__main__':
    speak('Initializing Jarvis....')

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)

            word = recognizer.recognize_google(audio)
            print("You said:", word)

            if word.lower() == 'jarvis':
                speak('Yes sir')

                with sr.Microphone() as source:
                    print('Jarvis active, listening for command...')
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                processcommand(command)

            elif "stop" in word.lower() or "ruk ja" in word.lower():
                speak("Okay, shutting down.")
                break

        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Sorry, I could not understand that.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except Exception as e:
            print("Error:", e)
