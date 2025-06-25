import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import os
import webbrowser
import openai
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc

# Set your OpenAI API key (optional, for smart answers)
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

engine = pyttsx3.init()
listener = sr.Recognizer()

# Add this at the top or just before the `run_siri()` function
app_paths = {
    "vscode": r"C:\Users\PAVAN\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad",
    "calculator": "calc",
    "explorer": "explorer",
    "command prompt": "cmd",
    "free fire": r"C:\Users\PAVAN\Desktop\Free Fire MAX.lnk",
    "whats app": r"C:\Users\PAVAN\AppData\Local\WhatsApp\WhatsApp.exe",
    "youtube"  :r"C:\Users\PAVAN\Desktop\YouTube.lnk",
    "files":r"C:\Windows\explorer.exe",
}


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



# --- Volume Control Function ---
def set_volume(level_percent):  # level_percent: 0–100
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Volume range is -96.0 to 0.0 dB
    min_volume, max_volume = volume.GetVolumeRange()[:2]
    target_volume = min_volume + (level_percent / 100.0) * (max_volume - min_volume)
    volume.SetMasterVolumeLevel(target_volume, None)

# --- Brightness Control Function ---
def set_brightness(level_percent):  # level_percent: 0–100
    sbc.set_brightness(level_percent)


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
         #os.system("code")  # VS Code (if added to PATH)
            os.system('"C:\\Users\\PAVAN\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"')
            speak("Opening Visual Studio Code")

        elif 'your name' in command:
            speak("My name is Jack, Iam  your AI assistant.")
            
        elif 'close code' in command or 'close visual studio' in command:
            os.system("taskkill /f /im Code.exe")
            speak("Closed Visual Studio Code")

        elif 'close chrome' in command or 'close browser' in command:
            os.system("taskkill /f /im chrome.exe")
            speak("Closed Chrome")

        elif 'close youtube' in command:
            os.system("taskkill /f /im chrome.exe")
            speak("Closed YouTube")

        elif 'close everything' in command or 'close all' in command:
            os.system("taskkill /f /im Code.exe")
            os.system("taskkill /f /im chrome.exe")
            speak("All applications have been closed")


        elif 'increase volume' in command:
            set_volume(100)
            speak("Volume increased to maximum")

        elif 'decrease volume' in command:
            set_volume(30)
            speak("Volume decreased")

        elif 'increase brightness' in command:
            set_brightness(100)
            speak("Brightness increased to maximum")

        elif 'decrease brightness' in command:
            set_brightness(30)
            speak("Brightness decreased")
        
        elif 'set volume to' in command:
                level = int(command.split("set volume to ")[-1].replace('%', ''))
                set_volume(level)
                speak(f"Volume set to {level} percent")
        elif 'set brightness to' in command:
            try:
                level = int(command.split("set brightness to ")[-1].replace('%', '').strip())
                if 0 <= level <= 100:
                    set_brightness(level)
                    speak(f"Brightness set to {level} percent")
                else:
                    speak("Please specify a brightness level between 0 and 100 percent.")
            except ValueError:
                    speak("I couldn't understand the brightness level. Please try again.")

        elif 'open' in command:
            try:
        # Extract app name after "open"
             app_name = command.replace('open', '').strip()
             if app_name in app_paths:
                 os.system(f'"{app_paths[app_name]}"')
                 speak(f"Opening {app_name}")
             else:
                 speak(f"Sorry, I don't know how to open {app_name}")
            except Exception as e:
                speak("Something went wrong while opening the application.")




        elif 'exit' in command or 'stop' in command:
            speak("Goodbye!")
            break

        elif command:
            speak("ASK agian")
            
       


run_siri()
