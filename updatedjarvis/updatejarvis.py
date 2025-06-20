import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random
import time
from dotenv import load_dotenv

load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Customize your paths 
MUSIC_DIR = 'C:\\Users\\HP\\Downloads\\One Love-(PagalWorld).mp3' # Give the path of your music directory
CODE_PATH = "C:\\Users\\HP\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe" # Give the path of your app

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Sir. Please tell me how may I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source)
    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"User said: {command}\n")
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that.")
        return "None"
    except sr.RequestError:
        speak("Speech service error.")
        return "None"
    return command

def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to, content)
        server.quit()
        speak("Email has been sent successfully!")
    except Exception as e:
        print(e)
        speak("Unable to send the email.")

def play_music():
    try:
        songs = [file for file in os.listdir(MUSIC_DIR) if file.endswith(('.mp3', '.wav'))]
        if songs:
            song_path = os.path.join(MUSIC_DIR, random.choice(songs))
            os.startfile(song_path)
            speak("Playing music.")
        else:
            speak("No music files found.")
    except Exception as e:
        print(e)
        speak("Unable to play music.")


# Main Program
if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                try:
                    print(results)
                except UnicodeEncodeError:
                    print(results.encode('ascii', 'ignore').decode())
                speak(results)

            except:
                speak("Sorry, I couldn't find anything.")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'open stack overflow' in query:
            speak("Opening Stack Overflow")
            webbrowser.open("https://stackoverflow.com")

        elif 'play music' in query:
            play_music()

        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")

        elif 'open code' in query:
            speak("Opening Visual Studio Code")
            os.startfile(CODE_PATH)

        elif 'send email' in query or 'email to vaibhav' in query:
            speak("What should I say?")
            content = take_command()
            if content and content != "None":
                send_email(RECIPIENT_EMAIL, content)


        elif any(word in query for word in ['exit', 'quit', 'stop', 'terminate', 'shutdown']):
            speak("Goodbye Sir!")
            break

        time.sleep(1)
