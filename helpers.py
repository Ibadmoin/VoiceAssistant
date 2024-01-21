import pyttsx3
import pyautogui
import psutil
import pyjokes
import speech_recognition as sr
import json
import requests
import geocoder
from difflib import get_close_matches
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
g = geocoder.ip('me')
data = json.load(open('data.json'))

def speak(audio)->None:
    engine.say(audio)
    engine.runAndWait()

def screenshot()->None:
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    img = pyautogui.screenshot()
    img.save(f"./screenshots/{filename}")

def cpu()->None:
    usage = str(psutil.cpu_percent())
    speak("CPU is at"+usage+"percent.")
    

def joke()->None:
    for i in range(5):
        speak(pyjokes.get_jokes()[i])


def takeCommand() -> str:
    # Create a recognizer object
    r = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust settings for recognizing speech
        r.pause_threshold =1
        r.energy_threshold = 494
        r.adjust_for_ambient_noise(source, duration=1.5)

        # Listen to the audio input
        audio = r.listen(source)

    try:
        print("Recognizing...")
        
        # Use Google's speech recognition to convert audio to text
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
    
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return "None"
    
    except sr.RequestError as err:
        print(f"Could not request results from Google's speech recognition service; {err}")
        return "None"
    
    return query

def weather():
      apiKey = os.getenv("WEATHER_API")
      api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={str(g.latlng[0])}&lon={str(g.latlng[1])}&appid={apiKey}"
    
      
      data = requests.get(api_url)
      data_json = data.json()
   
      if data_json['cod'] == 200:
        main = data_json['main']
        wind = data_json['wind']
        weather_desc = data_json['weather'][0]
        speak(str(data_json['coord']['lat']) + 'latitude' + str(data_json['coord']['lon']) + 'longitude')
        speak('Current location is ' + data_json['name'] + data_json['sys']['country'] + 'dia')
        speak('weather type ' + weather_desc['main'])
        speak('Wind speed is ' + str(wind['speed']) + ' metre per second')
        speak('Temperature: ' + str(main['temp']) + 'degree celcius')
        speak('Humidity is ' + str(main['humidity']))



def translate(word):
    word = word.lower()
    if word in data:
        speak(data[word])
    elif len(get_close_matches(word, data.keys()))> 0:
        x = get_close_matches(word, data.keys())[0]
        speak(f"Did you mean {x} instead, respond with Yes or No.")
        ans = takeCommand().lower()
        if 'yes' in ans:
            speak(data[x])
        elif 'no' in ans:
            speak("Word doesn't exist. Please make sure you spelled it correctly.")
        else:
            speak("Sorry Sir! i could'nt understand your query.")
    else:
          speak("Word doesn't exist. Please double check it.")


