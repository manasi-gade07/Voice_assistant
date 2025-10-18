import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import threading
import time
import musiclibrary 
from jokes import tell_joke





# Initialize recognizer
r = sr.Recognizer()


# Speak function (non-blocking + always works)
def speak(text):
    def _speak():
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # female voice (use voices[0] for male)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    print(f"Alexa: {text}")
    threading.Thread(target=_speak).start()

# Process user commands
def processCommand(c):
    c = c.lower()

    if "open google" in c:
        speak("Opening Google...")
        webbrowser.open("https://google.com")

    elif "open youtube" in c:
        speak("Opening YouTube...")
        webbrowser.open("https://youtube.com")

    elif "open facebook" in c:
        speak("Opening Facebook...")
        webbrowser.open("https://facebook.com")

    elif "open linkedin" in c:
        speak("Opening LinkedIn...")
        webbrowser.open("https://linkedin.com")

    elif "time" in c:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    
        
    elif "calculate" in command:
        expr = command.replace("calculate", "").strip()
        try:
            result = eval(expr)
            speak(f"The result is {result}")
        except:
            speak("Invalid calculation.")
    elif "joke" in c or "tell me a joke" in c:
        joke = tell_joke()  # Get joke from jokes.py
        print(f"Joke: {joke}")
        speak(joke)


    elif "date" in c:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")

    elif "search" in c:
        query = c.replace("search", "").strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("Please say what to search for.")

    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song in your library.")

    elif "open notepad" in c:
        speak("Opening Notepad...")
        os.system("notepad")

    elif "stop" in c or "exit" in c or "goodbye" in c:
        speak("Goodbye Manasi! Have a great day.")
        exit()

    else:
        speak("Sorry, I didn't understand that command.")

# Listen for speech
def listen_command(timeout=5, phrase_time_limit=4):
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        try:
            command = r.recognize_google(audio)
            print("Heard:", command)
            return command.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Network error.")
            return ""
        except Exception as e:
            print("Error:", e)
            return ""

# Main Loop
if __name__ == "__main__":
    speak("Hi Manasi! I am Alexa, your personal assistant.")
    time.sleep(1)
    while True:
        print("Say 'Alexa' to activate...")
        word = listen_command(timeout=5, phrase_time_limit=2)

        if "alexa" in word:
            speak("Yes, how can I help?")
            command = listen_command(timeout=6, phrase_time_limit=5)
            if command:
                processCommand(command)
            else:
                speak("I didn't catch that. Could you repeat?")
