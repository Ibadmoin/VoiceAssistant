import pyttsx3
import wikipedia
import speech_recognition as sr 
import webbrowser
import datetime
import os
import sys
import smtplib
from diction import translate
from sys import platform
from helpers import *
from youtube import youtube
import getpass

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)


class Jarvis:
    def __init__(self) -> None:
        self.currentAssistant = "jarvis"
        if platform == "linux" or platform == "linux2":
            self.chrome_path = '/usr/bin/google-chrome'
        elif platform == "darwin":
            self.chrome_path = 'open -a /Applications/Google/Chrome.app'
        elif platform == "win32":
            self.chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        else:
            print('Unsupported OS')
            exit(1)
        webbrowser.register(
            'chrome', None, webbrowser.BackgroundBrowser(self.chrome_path))
        
    def wishMe(self)->None:
        hour = int(datetime.now().hour)
        if hour >= 0 and hour <12:
            print("Good Morning SIR")
            speak("Good Morning SIR")
        elif hour >= 12 and hour < 18:
            print("Good Afternoon SIR")
            speak("Good Afternoon SIR")

        else:
            print('Good Evening SIR')
            speak('Good Evening SIR')
        
        print("I am JARVIS. Please tell me how can I help you SIR?")
        speak("I am JARVIS. Please tell me how can I help you SIR?")


    

    def sendEmail(self,to,content)->None:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login()
        server.sendmail('email',to,content)
        server.close()
    
    def execute_query(self, query):

        if 'current weather' in query:
            weather()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query =query.replace('wikipedia','')
            results = wikipedia.summary(query, sentences=2)
            speak('According to Wikipedia')
            print(results)
            speak(results)
        elif 'youtube downloader' in query:
            exec(open('youtube_downloader.py').read())

        if 'are you there' in query:
            speak("Yes Sir, I am here! How may I help you?")

        elif 'voice' in query:
            if self.currentAssistant == "jarvis":
                engine.setProperty('voice', voices[1].id)
                self.currentAssistant = "friday"
                speak("Hello Sir, I have switched to Friday's voice. How is it?")
            else:
                engine.setProperty('voice', voices[0].id)
                speak("Hello Sir, I have switched back to my original voice. How is it?")
                self.currentAssistant = "jarvis"

        
        if 'Jarvis who made you' in query:
            speak("I am an open source project which then upgraded by Ibad moin")
        
        elif 'open youtube' in query:
            webbrowser.get().open_new_tab('http://www.youtube.com')
        
        elif 'cpu' in query:
            cpu()
        
        elif 'joke' in query:
            joke()
        
        elif 'screenshot' in query:
            speak("Taking screenshot")
            screenshot()
        
        elif 'open google' in query:
            webbrowser.get().open_new_tab('https://www.google.com')
        
        elif 'open chat gpt' in query:
            webbrowser.get().open_new_tab('https://chat.openai.com')
        
        elif 'search youtube' in query:
            speak("What do you want to search on youtube?")
            youtube(takeCommand())
        
        elif "the time" in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            speak(f'Sir, the time is {strTime}')

        elif 'search' in query:
            speak("What do you want to search for?")
            search = takeCommand()
            url = 'https://google.com/search?q=' + search
            webbrowser.get('chrome').open_new_tab(url)
            speak("Here is what I found for, "+ search)

        elif 'location' in query:
            speak("what is the location")
            location = takeCommand()
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get('chrome').open_new_tab(url)
            speak('Here is the location ' + location)
        
        elif 'your master' in query:
            if platform == "win32" or "darwin":
                speak('Muhammad Ibad is my master. He created me couple of days ago')
            elif platform == "linux" or platform == "linux2":
                name = getpass.getuser()
                speak(name, 'is my master. He is running me right now')

        elif 'your name' in query:
            if hasattr(self, 'currentAssistant'):
                if self.currentAssistant == "friday":
                    speak("I am FRIDAY, the voice assistant created by Muhammad Ibad.")
                elif self.currentAssistant == "jarvis":
                    speak("I am JARVIS, the voice assistant created by Muhammad Ibad.")
                else:
                    speak("I am an open-source voice assistant, but I cannot determine my name in this context.")
            else:
                 speak("I am an open-source voice assistant, and my name has not been determined yet.")
            
        elif 'stands for' in query:
            speak('J.A.R.V.I.S stands for JUST A RATHER VERY INTELLIGENT SYSTEM')
            
        elif 'shutdown' in query:
            if platform == "win32":
                os.system('shutdown /p /f')
            elif platform == "linux" or platform == "linux2" or "darwin":
                os.system('poweroff')

        elif 'your friend' in query:
            speak('My friends are Google assisstant alexa and siri')
            
        elif "remember that" in query:
            speak("What should i remember sir!")
            rememberMsg = takeCommand()
            speak("You said me to remember ,\""+rememberMsg+"\". Will remind")
            remember = open('data.txt','w')
            remember.write(rememberMsg)
            remember.close()
            
        elif 'do you remember anything' in query:
            remember = open('data.txt', 'r')
            speak("You said me to remember that " + remember.read())
            remember.close()


        elif 'sleep' in query:
            speak("Going Offline, Sir Call me if you needed.")
            sys.exit()
            
        elif 'dictionary' in query:
            speak("What you want to search in your intelligent dictionary?")
            translate(takeCommand())
            

            # add news, github, music, etc
def wakeUpJARVIS():
    bot_ = Jarvis()
    bot_.wishMe()
    while True:
        query = takeCommand().lower()
        bot_.execute_query(query)

if __name__ == '__main__':
    wakeUpJARVIS()
        



