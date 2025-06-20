import speech_recognition as sr
import pyttsx3
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import time

class Karen:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Change index for different voices
        self.engine.setProperty('rate', 150)  # Speed of speech
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Animal-image mapping (using placeholder images from Unsplash)
        self.animal_images = {
            'rabbit': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'lion': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d',
            'rainbow': 'https://images.unsplash.com/photo-1533984649377-c20fc524425b?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'snake': 'https://plus.unsplash.com/premium_photo-1661897154120-5b27cd6a0bd5?q=80&w=388&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'lemon': 'https://images.unsplash.com/photo-1582287104445-6754664dbdb2?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'tiger': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5'
        }
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"Karen: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for voice commands"""
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
        try:
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you repeat?")
            return None
        except sr.RequestError:
            self.speak("Sorry, my speech service is down. Please try again later.")
            return None
            
    def show_image(self, animal):
        """Display image of the specified animal"""
        if animal in self.animal_images:
            try:
                response = requests.get(self.animal_images[animal])
                img = Image.open(BytesIO(response.content))
                
                plt.figure(figsize=(8, 6))
                plt.imshow(img)
                plt.axis('off')
                plt.title(animal.capitalize(), pad=20)
                plt.show()
                
                self.speak(f"Here is the image of {animal} you requested.")
            except Exception as e:
                print(f"Error loading image: {e}")
                self.speak(f"Sorry, I couldn't load the image of {animal}.")
        else:
            self.speak(f"I don't have an image for {animal}. Try another animal.")
            
    def run(self):
        """Main loop for Karen"""
        self.speak("Initializing Karen. How may I assist you today?")
        
        while True:
            command = self.listen()
            
            if command:
                if 'exit' in command or 'quit' in command or 'stop' in command:
                    self.speak("Goodbye! Have a great day.")
                    break
                    
                for animal in self.animal_images.keys():
                    if animal in command:
                        self.show_image(animal)
                        break
                else:
                    self.speak("I didn't recognize that animal. Try saying rabbit, lion, dog, cat, elephant, or tiger.")

if __name__ == "__main__":
    karen=Karen()
    karen.run()