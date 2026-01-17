import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import musicLibrary
import requests
from groq import Groq

recognizer = sr.Recognizer()
newsapi = "15b79b89b2e4fae99e92ad58a8cd95a"

client = Groq(api_key="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")

# ---------------- SPEAK (REINIT ENGINE EACH TIME) ----------------
def speak(text):
    print("Delta:", text)
    engine = pyttsx3.init('sapi5')   # 🔑 THIS IS THE FIX
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    time.sleep(0.3)

# ---------------- AI ----------------
def aiProcess(command):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a voice assistant named Delta"},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

# ---------------- COMMAND HANDLER ----------------
def processCommand(command):
    command = command.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif command.startswith("play"):
        song = command.replace("play", "").strip()
        link = musicLibrary.music.get(song)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Song not found")

    elif "news" in command:
        speak("Here are the top headlines")
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )
        if r.status_code == 200:
            for article in r.json().get("articles", [])[:5]:
                speak(article["title"])

    else:
        response = aiProcess(command)
        speak(response)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    speak("Initializing Delta")

    while True:
        try:
            # Wake word
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)

            word = recognizer.recognize_google(audio).lower()
            print("Heard:", word)

            if word == "delta":
                speak("I am active")

                while True:
                    try:
                        with sr.Microphone() as source:
                            print("Listening for command...")
                            recognizer.adjust_for_ambient_noise(source, duration=0.3)
                            audio = recognizer.listen(source, timeout=6)

                        command = recognizer.recognize_google(audio).lower()
                        print("Command:", command)

                        if "sleep" in command or "stop" in command:
                            speak("Going to sleep")
                            break

                        processCommand(command)

                    except sr.UnknownValueError:
                        speak("Say that again")
                    except sr.WaitTimeoutError:
                        speak("I am listening")

        except Exception as e:
            print("Error:", e)
