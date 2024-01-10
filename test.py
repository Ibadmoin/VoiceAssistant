import pyttsx3
import speech_recognition as sr

class VoiceAssistant:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)

    def speak(self, audio: str) -> None:
        self.engine.say(audio)
        self.engine.runAndWait()

    def take_command(self) -> str:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust settings for recognizing speech
            recognizer.pause_threshold = 1
            recognizer.energy_threshold = 494
            recognizer.adjust_for_ambient_noise(source, duration=1.5)

            audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"User said: {query}\n")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return ""
        return query

if __name__ == "__main__":
    assistant = VoiceAssistant()
    print(assistant.voices[1].id)
    if 'zira' in assistant.voices[1].id.lower():
        print("Friday")
    else:
        print("Jarvis")
