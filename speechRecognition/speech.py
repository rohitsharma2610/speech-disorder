import speech_recognition as sr
import pyttsx3
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import cv2
import time
import threading
import logging
import numpy as np

class Karen:
    def __init__(self):
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Karen")
        
        # Initialize TTS
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            if voices and len(voices) > 0:
                self.engine.setProperty('voice', voices[0].id)
            self.engine.setProperty('rate', 180)
            self.engine.setProperty('volume', 0.9)
            self.logger.info("TTS initialized")
        except Exception as e:
            self.logger.error(f"TTS error: {e}")
            self.engine = None

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                print("Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Microphone ready!")
        except Exception as e:
            print(f"Microphone error: {e}")
            self.microphone = None

        # Animal images
        self.animal_images = {
            'rabbit': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=800',
            'lion': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=800',
            'tiger': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=800',
            'snake': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=800',
            'lemon': 'https://images.unsplash.com/photo-1582287104445-6754664dbdb2?w=800',
            'rainbow': 'https://images.unsplash.com/photo-1533984649377-c20fc524425b?w=800'
        }

        # State variables
        self.running = True
        self.current_animal = None
        self.listening = False
        self.last_heard = ""
        self.last_response = ""
        self.status = "Ready"
        
        # Camera setup
        self.cap = None
        self.camera_active = False
        self.initialize_camera()
        
        # Start camera thread
        if self.cap:
            self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
            self.camera_thread.start()

    def initialize_camera(self):
        """Initialize camera"""
        try:
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                self.camera_active = True
                print("Camera initialized successfully!")
            else:
                print("Camera not available")
                self.cap = None
        except Exception as e:
            print(f"Camera error: {e}")
            self.cap = None

    def camera_loop(self):
        """Camera display loop with status"""
        while self.running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                # Flip frame for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Create overlay for text
                overlay = frame.copy()
                
                # Status box
                cv2.rectangle(overlay, (10, 10), (780, 150), (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
                
                # Status text
                cv2.putText(frame, "KAREN SPEECH RECOGNITION", (20, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                cv2.putText(frame, f"Status: {self.status}", (20, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                if self.listening:
                    cv2.putText(frame, "LISTENING...", (20, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                if self.last_heard:
                    cv2.putText(frame, f"You said: {self.last_heard}", (20, 130),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                
                # Current animal box
                if self.current_animal:
                    cv2.rectangle(overlay, (10, 160), (400, 220), (0, 100, 0), -1)
                    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
                    cv2.putText(frame, f"Current Animal: {self.current_animal.upper()}", (20, 190),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Instructions
                instructions = [
                    "Say: 'show me [animal]'",
                    "Animals: rabbit, lion, tiger, snake, lemon, rainbow",
                    "Press 'q' to quit"
                ]
                
                y_start = frame.shape[0] - 80
                for i, instruction in enumerate(instructions):
                    cv2.putText(frame, instruction, (20, y_start + i * 25),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                # Show frame
                cv2.imshow('Karen Camera', frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break
                    
            except Exception as e:
                print(f"Camera loop error: {e}")
                break
        
        # Cleanup
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Camera closed")

    def speak(self, text):
        """Text to speech"""
        try:
            print(f"[KAREN SAYS]: {text}")
            if self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

    def listen_once(self):
        """Listen for one command with visual feedback"""
        if not self.microphone:
            print("[KAREN]: No microphone available")
            return None
            
        try:
            self.listening = True
            self.status = "Listening..."
            print("[KAREN]: Listening for command...")
            
            with self.microphone as source:
                # Listen with shorter timeout for server mode
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
            self.status = "Processing..."
            print("[KAREN]: Processing speech...")
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language='en-US')  # type: ignore
            text = text.lower().strip()
            
            self.last_heard = text
            self.status = "Ready"
            self.listening = False
            
            print(f"[KAREN]: Heard: '{text}'")
            return text
            
        except sr.WaitTimeoutError:
            self.status = "Ready"
            self.listening = False
            # Don't print timeout in server mode - it's normal
            return None
        except sr.UnknownValueError:
            self.status = "Could not understand"
            self.listening = False
            print("[KAREN]: Could not understand speech")
            return None
        except sr.RequestError as e:
            self.status = f"Recognition error: {e}"
            self.listening = False
            print(f"[KAREN]: Recognition error: {e}")
            return None
        except Exception as e:
            self.status = f"Error: {e}"
            self.listening = False
            print(f"[KAREN]: Listen error: {e}")
            return None

    def show_image(self, animal):
        """Show animal image"""
        if animal not in self.animal_images:
            return False
            
        try:
            print(f"[KAREN]: Loading {animal} image...")
            self.status = f"Loading {animal} image..."
            
            response = requests.get(self.animal_images[animal], timeout=10)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            
            # Show image
            plt.figure(figsize=(10, 8))
            plt.imshow(img)
            plt.axis('off')
            plt.title(f"{animal.upper()}", fontsize=20, pad=20)
            plt.tight_layout()
            plt.show(block=False)
            plt.pause(0.1)
            
            self.status = f"Showing {animal}"
            print(f"[KAREN]: Showing {animal} image")
            return True
            
        except Exception as e:
            print(f"[KAREN]: Image error: {e}")
            self.status = f"Image error: {e}"
            return False

    def process_command(self, command):
        """Process voice command"""
        if not command:
            return "I didn't hear anything."
        
        command = command.lower().strip()
        print(f"[KAREN]: Processing command: '{command}'")
        self.status = "Processing command..."
        
        # Check for exit
        if any(word in command for word in ['exit', 'quit', 'stop', 'bye', 'goodbye']):
            self.speak("Goodbye!")
            self.running = False
            self.status = "Goodbye!"
            return "Goodbye!"
        
        # Check for animals
        found_animal = None
        for animal in self.animal_images.keys():
            if animal in command:
                found_animal = animal
                break
        
        if found_animal:
            self.current_animal = found_animal
            self.status = f"Selected: {found_animal}"
            
            response_text = f"Great! You want to see a {found_animal}. Let me show you."
            self.speak(response_text)
            
            if self.show_image(found_animal):
                self.speak(f"Here is a beautiful {found_animal}! Now say the word {found_animal} clearly for pronunciation practice.")
                return f"Showing {found_animal} image. Now practice saying '{found_animal}'"
            else:
                return f"Sorry, couldn't load {found_animal} image."
        
        # Check pronunciation
        if self.current_animal and self.current_animal in command:
            self.speak(f"Excellent! Perfect pronunciation of {self.current_animal}!")
            response = f"Perfect pronunciation of {self.current_animal}!"
            self.current_animal = None
            self.status = "Ready for next animal"
            return response
        
        # Help message
        animals = ", ".join(self.animal_images.keys())
        help_msg = f"Say 'show me' followed by: {animals}"
        self.speak("I can show you rabbit, lion, tiger, snake, lemon, or rainbow. Just say show me and the animal name.")
        self.status = "Waiting for command"
        return help_msg

    def run(self):
        """Main run loop for server mode"""
        try:
            self.status = "Starting..."
            self.speak("Hello! I am Karen. I can show you animal pictures.")
            self.speak("Say 'show me' followed by rabbit, lion, tiger, snake, lemon, or rainbow.")
            self.status = "Ready - listening for voice commands"
            
            while self.running:
                time.sleep(0.1)  # Keep alive for server mode
                
        except Exception as e:
            print(f"[KAREN]: Run error: {e}")

    def run_interactive(self):
        """Interactive mode with continuous listening"""
        try:
            self.status = "Starting..."
            self.speak("Hello! I am Karen. I can show you animal pictures.")
            self.speak("Say 'show me' followed by rabbit, lion, tiger, snake, lemon, or rainbow.")
            self.status = "Ready - say 'show me [animal]'"
            
            while self.running:
                command = self.listen_once()
                if command:
                    response = self.process_command(command)
                    print(f"[KAREN]: Response: {response}")
                else:
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\nShutting down...")
        except Exception as e:
            print(f"[KAREN]: Run error: {e}")
        finally:
            self.stop_interaction()

    def stop_interaction(self):
        """Stop Karen"""
        print("[KAREN]: Stopping...")
        self.running = False
        self.status = "Stopped"
        
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        plt.close('all')
        
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

if __name__ == "__main__":
    karen = Karen()
    karen.run_interactive()
