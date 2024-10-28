import time
from ipaddress import ip_address

import pyttsx3
import keyboard
import os
import subprocess as sp
import imdb
import wolframalpha
import pyautogui
import webbrowser

import speech_recognition as sr
from decouple import config
from datetime import datetime
from conv import random_text
from random import choice
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 225)
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

USER = config('USER')
HOSTNAME = config('BOT')


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Reconizing...")
        queri = r.recognize_google(audio, language='en-i')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 23 and hour < 6:
                speak("Good night sir,take care!")
            else:
                speak("Have a good day sir!")
            exit()

    except Exception:
        speak("Sorry I could not understood. Can you please repeat that?")
        queri = 'None'
    return queri


def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_me():
    hour = datetime.now().hour
    if(hour >= 6) and (hour <12):
        speak(f"Good morning {USER}")
    elif(hour >= 12) and (hour <= 17):
        speak(f"Good afternoon {USER}")
    elif(hour >= 17) and (hour <23):
        speak(f"Good evening {USER}")
    speak(f"I am {HOSTNAME}. How may i assist you?")

listening = False

def start_listening():
    global listening
    listening = True
    print("started listening")

def pause_listening():
    global listening
    listening = False
    print("stopped listening")

keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I am absolutely fine sir. What about you")

            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening camera sir")
                sp.run('start microsoft.windows.camera:', shell=True)

            elif "open notepad" in query:
                speak("Opening Notepad for you sir")
                notepad_path = "C:\\Users\\Gelso\\AppData\\Local\\Microsoft\\WindowsApps\\notepad.exe"
                os.startfile(notepad_path)

            elif "open discord" in query:
                speak("Opening Discord for you sir")
                discord_path = "C:\\Users\\Gelso\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc"
                os.startfile(discord_path)

            elif "open android studio" in query:
                speak("Opening Android Studio for you sir")
                androidStudio_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Android Studio"
                os.startfile(androidStudio_path)

            elif "open vscode" in query:
                speak("Opening Visual Studio Code for you sir")
                vscode_path = "C:\\Users\\Gelso\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code"
                os.startfile(vscode_path)

            elif "open photoshop" in query:
                speak("Opening Adobe Photoshop for you sir")
                photoshop_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Adobe Photoshop 2023"
                os.startfile(photoshop_path)

            elif "open after effects" in query:
                speak("Opening Adobe After Effects for you sir")
                afterEffects_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Adobe After Effects 2022"
                os.startfile(afterEffects_path)

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(f"Your ip address is {ip_address}")
                print(f"Your address is {ip_address}")

            elif "open youtube" in query:
                speak("What do you want to play on youtube sir?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"What do you what to search on google {USER}?")
                query = take_command().lower()
                search_on_google(query)

            elif "open wikipedia" in query:
                speak("What do you want to search on wikipedia sir?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia, {results}")
                speak("I am printing in on terminal")
                print(results)

            elif "send email" in query:
                speak("On what email address do you want to send sir? Please enter in the terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject sir?")
                subject = take_command().capitalize()
                speak("What is the message?")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong! Please check the error log sir.")

            elif "give me news" in query:
                speak(f"I am reading out the latest headline of today, sir")
                speak(get_news())
                speak("I am printing in the screen sir")
                print(*get_news(), sep='\n')

            elif "weather" in query:
                ip_address = find_my_ip()
                speak("tell me the name of your city")
                city = input("Enter the name of your city")
                speak(f"Getting weather report for your city {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                speak(f"Also, the weather report talsk about {weather}")
                speak("For your convenience, I am printing it on the screen sir!")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels like:{feels_like}")

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name:")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("searching for" + text)
                speak("I found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title} - {year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline', 'plot summary not available')
                    speak(f"{title} was released in {year} has imdb ratings of {rating}. It has a cast of {actor}."
                          f" The plot summary of movie is {plot}")

                    print(f"{title} was released in {year} has imdb ratings of {rating}. It has a cast of {actor}."
                          f" The plot summary of movie is {plot}")


            elif "calculate" in query:
                app_id = "TA64T7-AEU7YPU4VY"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is "+ans)
                    print("The answer is " + ans)
                except StopIteration:
                    speak("I could not find that! Please try again.")

            elif "what is" in query or "who is" in query or "which is" in query:
                app_id = "TA64T7-AEU7YPU4VY"
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                        query.lower().index("who is") if 'who is' in query.lower() else \
                        query.lower().index("which is") if 'which is' in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind+2:]
                        result = client.query(" ".join(text))
                        ans = next(result.results).text
                        speak("The answer is "+ ans)
                        print("The answer is "+ ans)
                    else:
                        speak("I could not find that")

                except StopIteration:
                    speak("I could not find that. Please try again!")

            elif "subscribe" in query:
                speak("Everyone who are listining to me, please subscribe"
                      f"to Gelson Matavela youtube channel! I will teach you how to do.")

                speak("Firstly go to youtube")
                webbrowser.open("https://youtube.com/")
                speak("click on search bar")
                pyautogui.moveTo(806, 120, 1)
                pyautogui.click(x=806, y=125, clicks =1, interval = 0, button = 'left')
                speak("Gelson Matavela")
                pyautogui.typewrite("Gelson Matavela", 0.1)
                time.sleep(1)
                speak("press enter")
                pyautogui.press('enter')
                pyautogui.moveTo(971, 314, 1)
                speak("Here you will se our channel")
                pyautogui.moveTo(1638, 314, 1)
                speak("Click here to subscribe our channel")
                pyautogui.click(x = 1688, y = 314, clicks = 1, interval = 0, button = 'left')
                speak("And also do not forget to press the bell icon")
                pyautogui.moveTo(1750, 314, 1)
                pyautogui.click(x = 1750, y = 314, clicks = 1, interval = 0, button = 'left')
                speak("turn on all notifications")
                pyautogui.click(x = 1750, y = 320, clicks = 1, interval = 0, button = 'left')


















