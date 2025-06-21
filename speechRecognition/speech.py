import speech_recognition as sr
import pyttsx3
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
import threading
import os
import logging

class Karen:
    def __init__(self):
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Karen")
        
        # Initialize text-to-speech engine with error handling
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
            self.engine.setProperty('rate', 150)
            self.logger.info("TTS engine initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing TTS engine: {e}")
            raise RuntimeError("Could not initialize text-to-speech engine")

        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            self.logger.info("Microphone initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing microphone: {e}")
            raise RuntimeError("Could not initialize microphone")

        # Initialize camera with Windows-specific backend
        self.cap = None
        self.initialize_camera()

        # Load mouth cascade with fallback
        self.mouth_cascade = None
        self.initialize_mouth_cascade()

        # Animal-image mapping
        self.animal_images = {
            'rabbit': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308',
            'lion': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d',
            'rainbow': 'https://images.unsplash.com/photo-1533984649377-c20fc524425b',
            'snake': 'https://plus.unsplash.com/premium_photo-1661897154120-5b27cd6a0bd5',
            'lemon': 'https://images.unsplash.com/photo-1582287104445-6754664dbdb2',
            'tiger': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5'
        }

        # State variables
        self.expected_word = ""
        self.lip_movement_detected = False
        self.feedback_text = ""
        self.show_feedback = False
        self.feedback_timeout = 0
        self.running = True
        self.interaction_active = True
        self.lock = threading.Lock()

        # Start camera thread if camera is available
        if self.cap is not None:
            self.camera_thread = threading.Thread(target=self.camera_loop)
            self.camera_thread.daemon = True
            self.camera_thread.start()
            self.logger.info("Camera thread started")

    def initialize_camera(self):
        """Initialize camera with Windows-specific backend and retries"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Try different backends
                backends = [cv2.CAP_DSHOW, cv2.CAP_ANY]
                for backend in backends:
                    try:
                        self.cap = cv2.VideoCapture(0, backend)
                        if self.cap.isOpened():
                            break
                    except:
                        continue
                
                if not self.cap or not self.cap.isOpened():
                    self.logger.warning("Could not open camera - running in audio-only mode")
                    self.cap = None
                    self.lip_movement_detected = True  # Bypass lip sync check
                    return
                
                # Configure camera settings
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                self.logger.info("Camera initialized successfully")
                return
                
            except Exception as e:
                self.logger.error(f"Camera initialization attempt {attempt + 1} failed: {e}")
                if attempt == max_attempts - 1:
                    self.logger.warning("Giving up on camera initialization")
                    self.cap = None
                    self.lip_movement_detected = True
                time.sleep(1)

    def initialize_mouth_cascade(self):
        """Initialize mouth cascade classifier with fallback"""
        try:
            cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_smile.xml')
            if os.path.exists(cascade_path):
                self.mouth_cascade = cv2.CascadeClassifier(cascade_path)
                if self.mouth_cascade.empty():
                    self.logger.warning("Could not load mouth cascade - lip sync detection disabled")
                    self.mouth_cascade = None
                else:
                    self.logger.info("Mouth cascade loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading mouth cascade: {e}")
            self.mouth_cascade = None

    def camera_loop(self):
        """Camera processing loop with robust error handling"""
        while self.running and self.cap is not None and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    self.logger.warning("Failed to capture frame - retrying...")
                    time.sleep(0.1)
                    continue

                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Mouth detection only if cascade is loaded
                if self.mouth_cascade is not None:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    mouths = self.mouth_cascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags=cv2.CASCADE_SCALE_IMAGE
                    )
                    
                    self.lip_movement_detected = len(mouths) > 0

                    # Draw rectangles around the mouths
                    for (x, y, w, h) in mouths:
                        if y > frame.shape[0] // 2:  # Lower half of face
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    self.lip_movement_detected = True  # Bypass if no cascade

                # Display feedback if needed
                if self.show_feedback:
                    cv2.putText(frame, self.feedback_text, (50, 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Check if feedback should timeout
                    if time.time() > self.feedback_timeout:
                        self.show_feedback = False

                # Display the frame
                cv2.imshow('Karen - Lip Sync Recognition', frame)
                
                # Exit on 'q' key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break

            except Exception as e:
                self.logger.error(f"Camera loop error: {e}")
                time.sleep(0.1)

        # Clean up
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        self.logger.info("Camera loop ended")

    def speak(self, text):
        """Convert text to speech with error handling"""
        try:
            self.logger.info(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.logger.error(f"Error in speech synthesis: {e}")

    def listen(self):
        """Listen for voice commands with improved recognition and error handling"""
        try:
            with self.microphone as source:
                self.logger.info("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    self.logger.info("Processing your speech...")
                    
                    result = self.recognizer.recognize_google(audio, show_all=True)
                    
                    if isinstance(result, dict) and 'alternative' in result:
                        alternatives = [alt['transcript'].lower() for alt in result['alternative']]
                        self.logger.info(f"Possible matches: {alternatives}")
                        
                        if self.expected_word:
                            for alt in alternatives:
                                if self.expected_word in alt:
                                    self.logger.info(f"Matched expected word: {self.expected_word}")
                                    return self.expected_word
                        
                        return alternatives[0] if alternatives else None
                    
                    elif isinstance(result, str):
                        return result.lower()
                    
                    return None
                    
                except sr.WaitTimeoutError:
                    self.logger.warning("Listening timed out")
                    return None
                except sr.UnknownValueError:
                    self.logger.warning("Could not understand audio")
                    self.speak("Sorry, I didn't catch that. Could you repeat?")
                    return None
                except sr.RequestError as e:
                    self.logger.error(f"Recognition error: {e}")
                    self.speak("Sorry, my speech service is down. Please try again later.")
                    return None
        except Exception as e:
            self.logger.error(f"Error in listen(): {e}")
            return None

    def show_image(self, animal):
        """Display image of the specified animal with error handling"""
        if animal in self.animal_images:
            try:
                self.logger.info(f"Fetching image for {animal}")
                response = requests.get(self.animal_images[animal], stream=True, timeout=5)
                response.raise_for_status()
                
                img = Image.open(BytesIO(response.content))
                
                plt.figure(figsize=(10, 8))
                plt.imshow(img)
                plt.axis('off')
                plt.title(animal.capitalize(), pad=20, fontsize=14)
                plt.tight_layout()
                plt.show(block=False)
                plt.pause(0.1)
                
                self.speak(f"Here is the image of {animal} you requested.")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Network error loading image: {e}")
                self.speak(f"Sorry, I couldn't load the image of {animal}. Please check your internet connection.")
            except Exception as e:
                self.logger.error(f"Error loading image: {e}")
                self.speak(f"Sorry, I couldn't display the image of {animal}.")
        else:
            self.logger.warning(f"No image available for {animal}")
            self.speak(f"I don't have an image for {animal}. Try another animal.")

    def stop_interaction(self):
        """Stop all running processes"""
        with self.lock:
            self.logger.info("Stopping interaction...")
            self.running = False
            self.interaction_active = False
            
            # Stop speech synthesis if it's running
            if hasattr(self, 'engine'):
                self.engine.stop()
            
            # Release camera resources
            if hasattr(self, 'cap') and self.cap is not None:
                self.cap.release()
            
            # Close all OpenCV windows
            cv2.destroyAllWindows()
            
            # Close matplotlib figures
            plt.close('all')
            self.logger.info("Interaction stopped")

    def cleanup(self):
        """Clean up resources"""
        self.stop_interaction()

    def check_pronunciation(self, command):
        """Check pronunciation with improved feedback"""
        if not command:
            self.feedback_text = "I didn't hear anything. Please try again."
            self.show_feedback = True
            self.feedback_timeout = time.time() + 3
            self.logger.info("No command received")
            return False

        if not self.lip_movement_detected and self.cap is not None:
            self.feedback_text = "I didn't see your lips moving. Please face the camera and speak clearly."
            self.show_feedback = True
            self.feedback_timeout = time.time() + 3
            self.logger.info("No lip movement detected")
            return False

        if command == self.expected_word:
            self.feedback_text = "Perfect! Your pronunciation was correct."
            self.show_feedback = True
            self.feedback_timeout = time.time() + 3
            self.logger.info(f"Correct pronunciation: {command}")
            return True
        else:
            self.feedback_text = (f"Almost there! You said '{command}' but expected '{self.expected_word}'. "
                                f"Try emphasizing the sounds in '{self.expected_word}'.")
            self.show_feedback = True
            self.feedback_timeout = time.time() + 4
            self.logger.info(f"Incorrect pronunciation. Expected: {self.expected_word}, Got: {command}")
            return False

    def run(self):
        try:
            self.speak("Hello! I'm Karen. Let's practice pronunciation together.")
            self.logger.info("Starting main interaction loop")
            
            while self.running and self.interaction_active:
                try:
                    # Animal selection prompt
                    self.speak("Which animal would you like to see? You can say rabbit, lion, rainbow, snake, lemon, or tiger.")
                    
                    # Listen for command with timeout
                    command = None
                    start_time = time.time()
                    while time.time() - start_time < 30:  # 30-second timeout
                        command = self.listen()
                        if command is not None:
                            break
                        time.sleep(0.1)
                    
                    if not command:
                        self.logger.warning("No command received within timeout")
                        continue
                        
                    if any(word in command for word in ['exit', 'quit', 'stop']):
                        self.speak("Goodbye! It was nice practicing with you.")
                        self.running = False
                        break

                    # Process animal command
                    for animal in self.animal_images.keys():
                        if animal in command:
                            self.expected_word = animal
                            self.speak(f"Great! Now please say the word '{animal}' clearly while facing the camera.")
                            
                            # Pronunciation check
                            pronunciation_check = None
                            start_time = time.time()
                            while time.time() - start_time < 30:  # 30-second timeout
                                pronunciation_check = self.listen()
                                if pronunciation_check is not None:
                                    break
                                time.sleep(0.1)
                            
                            if pronunciation_check:
                                correct = self.check_pronunciation(pronunciation_check)
                                if correct:
                                    self.show_image(animal)
                                    time.sleep(2)  # Show image for 2 seconds
                            break
                    else:
                        self.speak("I didn't recognize that animal. Please try again.")
                        
                except Exception as e:
                    self.logger.error(f"Error in interaction cycle: {e}")
                    continue
                    
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
        except Exception as e:
            self.logger.error(f"Fatal error in run(): {e}")
        finally:
            self.cleanup()
            self.logger.info("Main interaction loop ended")

if __name__ == "__main__":
    try:
        karen = Karen()
        karen.run()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")