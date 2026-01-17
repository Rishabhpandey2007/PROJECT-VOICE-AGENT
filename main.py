import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import musicLibrary
import requests
import client
from groq import Groq

recognizer = sr.Recognizer()
newsapi="15b79b89b2e4fae99e92ad58a8cd95a"

def speak(text):
    engine = pyttsx3.init('sapi5')  # critical fix
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()



def processCommand(command):
    command = command.lower()
    print("Command:", command)

    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in command.lower():
         r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey=15b79b89b2e4fae99e92ad58a8cd95a")
         if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
    else:
        output = aiProcess(command)
        speak(output)  

def aiProcess(command):
    completion = client.client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a voice assistant named delta"},
            {"role": "user", "content": command}
        ]
    )
    response = completion.choices[0].message.content
    speak(response)  

if __name__ == "__main__":
    speak("Initializing delta")

    while True:
        try:
            # ---- WAKE WORD ----
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)

            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if word.lower() == "delta":
                time.sleep(0.3)
                speak("Give me command boss")

                # ---- COMMAND ----
                with sr.Microphone() as source:
                    print("Delta Active...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                processCommand(command)

        except sr.WaitTimeoutError:
            print("Timeout waiting for speech")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except Exception as e:
            print("Error:", str(e))