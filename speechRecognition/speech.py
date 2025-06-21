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

class Karen:
    def _init_(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 150)

        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")

        # Load mouth cascade (using a more reliable approach)
        cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_smile.xml')
        self.mouth_cascade = cv2.CascadeClassifier(cascade_path)
        if self.mouth_cascade.empty():
            raise RuntimeError("Could not load mouth cascade classifier")

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

        # Start camera thread
        self.camera_thread = threading.Thread(target=self.camera_loop)
        self.camera_thread.daemon = True
        self.camera_thread.start()

    def camera_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect mouths in the image
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
                # Only consider detections in the lower half of the face
                if y > frame.shape[0] // 2:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    self.lip_movement_detected = True

            # Display feedback if needed
            if self.show_feedback:
                cv2.putText(frame, self.feedback_text, (50, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Check if feedback should timeout
                if time.time() > self.feedback_timeout:
                    self.show_feedback = False

            # Display the resulting frame
            cv2.imshow('Karen - Lip Sync Recognition', frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

        # Release the capture when done
        self.cap.release()
        cv2.destroyAllWindows()

    def speak(self, text):
        """Convert text to speech"""
        print(f"Karen: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for voice commands with improved recognition"""
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                print("Processing your speech...")
                
                # Try Google Speech Recognition with show_all=True for alternatives
                result = self.recognizer.recognize_google(audio, show_all=True)
                
                if isinstance(result, dict) and 'alternative' in result:
                    # Get all possible transcriptions
                    alternatives = [alt['transcript'].lower() for alt in result['alternative']]
                    print(f"Possible matches: {alternatives}")
                    
                    # Check if any alternative matches our expected word
                    if self.expected_word:
                        for alt in alternatives:
                            if self.expected_word in alt:
                                print(f"Matched expected word: {self.expected_word}")
                                return self.expected_word
                    
                    # Return the most confident result
                    return alternatives[0]
                
                elif isinstance(result, str):
                    return result.lower()
                
                return None
                
            except sr.WaitTimeoutError:
                print("Listening timed out")
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                self.speak("Sorry, I didn't catch that. Could you repeat?")
                return None
            except sr.RequestError as e:
                print(f"Recognition error: {e}")
                self.speak("Sorry, my speech service is down. Please try again later.")
                return None
            except Exception as e:
                print(f"Unexpected error: {e}")
                return None
            
    def show_image(self, animal):
        """Display image of the specified animal"""
        if animal in self.animal_images:
            try:
                response = requests.get(self.animal_images[animal], stream=True)
                response.raise_for_status()
                
                img = Image.open(BytesIO(response.content))
                
                # Create a new figure with a specified size
                plt.figure(figsize=(10, 8))
                plt.imshow(img)
                plt.axis('off')
                plt.title(animal.capitalize(), pad=20, fontsize=14)
                
                # Adjust layout to prevent cutting off
                plt.tight_layout()
                
                # Use a non-blocking show
                plt.show(block=False)
                plt.pause(0.1)  # Small pause to allow the window to appear
                
                self.speak(f"Here is the image of {animal} you requested.")
            except Exception as e:
                print(f"Error loading image: {e}")
                self.speak(f"Sorry, I couldn't load the image of {animal}.")
        else:
            self.speak(f"I don't have an image for {animal}. Try another animal.")

    def check_pronunciation(self, command):
        """Check pronunciation with improved feedback"""
        if not command:
            self.feedback_text = "I didn't hear anything. Please try again."
            self.show_feedback = True
            self.feedback_timeout = time.time() + 3
            return False

        if not self.lip_movement_detected:
            self.feedback_text = "I didn't see your lips moving. Please face the camera and speak clearly."
            self.show_feedback = True
            self.feedback_timeout = time.time() + 3
            return False

        if command == self.expected_word:
            self.feedback_text = "Perfect! Your pronunciation was correct."
            self.show_feedback = True
            self.feedback_timeout = time.time() + 3
            return True
        else:
            # Give more specific feedback
            self.feedback_text = (f"Almost there! You said '{command}' but expected '{self.expected_word}'. "
                                f"Try emphasizing the sounds in '{self.expected_word}'.")
            self.show_feedback = True
            self.feedback_timeout = time.time() + 4
            return False

    def run(self):
        """Main interaction loop"""
        self.speak("Hello! I'm Karen. Let's practice pronunciation together.")
        
        try:
            while self.running:
                self.speak("Which animal would you like to see? You can say rabbit, lion, rainbow, snake, lemon, or tiger.")
                
                # Get initial command
                command = self.listen()
                
                if not command:
                    continue
                    
                if 'exit' in command or 'quit' in command or 'stop' in command:
                    self.speak("Goodbye! It was nice practicing with you.")
                    self.running = False
                    break

                # Check for animal names
                for animal in self.animal_images.keys():
                    if animal in command:
                        self.expected_word = animal
                        
                        # Give clear instructions
                        self.speak(f"Great! Now please say the word '{animal}' clearly while facing the camera. "
                                 "Make sure I can see your lips moving.")
                        
                        # Wait a moment before listening again
                        time.sleep(1)
                        
                        # Get pronunciation attempt
                        pronunciation_check = self.listen()
                        
                        if pronunciation_check:
                            correct = self.check_pronunciation(pronunciation_check)
                            if correct:
                                self.show_image(animal)
                                time.sleep(2)  # Give time to view the image
                        break
                else:
                    self.speak("I didn't recognize that animal. Please try again.")
                    
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.running = False
            self.cap.release()
            cv2.destroyAllWindows()
            plt.close('all')


if __name__ == "_main_":
    try:
        karen = Karen()
        karen.run()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")