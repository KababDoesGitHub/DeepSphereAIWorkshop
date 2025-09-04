import datetime
import random
import pyttsx3
import requests
import speech_recognition as sr

class voiceAssistant:
    def __init__(self):
        self._setup_core_components()
        self._setup_apis()
        self._setup_responses()
        self._initialize_assistant()
    def _setup_core_components(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.assistant_name = "Alt Cunningham"
        self._configure_voice()
    def setup_apis(self):
        self.gemini_api_key = "AIzaSyBs6PtzdSOxvu7n5DofqdqEqbRj2wOV3tQ"
        self.gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    def _setup_responses(self):
        self.responses = {
            "hello": ["Hello! How can I help you today?", "Hi there!", "Hello! Nice to meet you!"],
            "how are you": ["I'm doing great, thank you for asking!", "I'm fine, how about you?"],
            "what is your name": [f"I'm {self.assistant_name}, your personal voice assistant!", f"You can call me {self.assistant_name}.", f"I'm {self.assistant_name}."],
            "goodbye": ["Goodbye! Have a great day!", "See you later!", "Bye! Take care!"],
            "thank you": ["You're welcome!", "Happy to help!", "No problem!"],
        }
    def _initialize_assistant(self):
        print(f"{self.assistant_name} is now online.")
        self.speak(f"Hello! I am {self.assistant_name}, your personal voice assistant. How can I assist you today?")
        self._test_gemini_connection
    def _configure_voice(self):
        voices = self.engine.getProperty('voices')
        print(f"Found {len(voices)} voices available.")
        if voices:
            print(f"Using default voice: {voices[0].name}")
            self.tts_engine.setProperty('rate',150)
            self.tts_engine.setProperty('volume',1.0)
    def _test_gemini_connection(self):
        print('Testing Gemini API connection...')
        if self.ask_gemini("Say hello in one sentence"):
            print("Gemini API connected successfully!.")
        else:
            print("Failed to connect to Gemini API.- Check your API Key and network connection.")
    def speak(self, text):
        print(f"Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    def listen(self):
        timeout = 30
        phrase_limit = 60
        threshold = 200 
        pause_threshold = 1.5
        try:
            with self.microphone as source:
                print("Listening for input...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                self.recognizer.energy_threshold = threshold
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = pause_threshold
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            error_msg = "I couldn't understand that clearly. Please try again with clearer speech."
            print("Speech was unclear - please try again")
            self.speak(error_msg)
            return None
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            self.speak("Sorry, I'm having trouble with the speech recognition service.")
            return None
        except Exception as e:
            print(f"Error during listening: {e}")
            self.speak("Sorry, something went wrong while listening. Please try again.")
            return None