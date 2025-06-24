import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import os
import webbrowser
import openai

# Set your OpenAI API key (optional, for smart answers)
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

engine = pyttsx3.init()
listener = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("🎙️ Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"👂 You said: {command}")
            return command
    except:
        return ""

def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def run_siri():
    speak("Hi! I'm jack, your AI assistant. How can I help you today?")

    while True:
        command = take_command()

        if 'play' in command:
            song = command.replace('play', '')
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The time is {time}")

        elif 'open youtube' in command:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")

        elif 'open google' in command:
            webbrowser.open("https://google.com")
            speak("Opening Google")

        elif 'open code' in command:
            os.system("code")  # VS Code (if added to PATH)
            speak("Opening Visual Studio Code")

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye!")
            break

        elif command:
            speak("Let me think...")
            response = ask_openai(command)
            speak(response)

run_siri()
