from flask import Flask, jsonify
from flask_cors import CORS
from speechRecognition.speech import Karen
import threading
import logging
import time

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class KarenSystem:
    def __init__(self):
        self.karen = None
        self.is_active = False
        self.status_message = "System ready"
        self.lock = threading.Lock()
        self.interaction_thread = None
        self.camera_thread = None

    def get_status(self):
        with self.lock:
            return {
                "active": self.is_active,
                "message": self.status_message
            }

    def toggle_system(self):
        with self.lock:
            if self.is_active:
                return self._stop_karen()
            return self._start_karen()

    def _start_karen(self):
        try:
            logger.info("Starting Karen system...")
            self.status_message = "Starting system..."
            
            # Initialize Karen instance
            self.karen = Karen()
            self.karen.running = True
            
            # Start camera thread if available
            if self.karen.cap is not None:
                self.camera_thread = threading.Thread(target=self.karen.camera_loop)
                self.camera_thread.daemon = True
                self.camera_thread.start()
                time.sleep(2)  # Give camera more time to initialize
            
            # Start main interaction in a separate thread
            self.interaction_thread = threading.Thread(target=self._run_interaction, daemon=True)
            self.interaction_thread.start()
            
            self.is_active = True
            self.status_message = "System active - listening for commands"
            logger.info("Karen system started successfully")
            
            return {
                "status": "success",
                "active": True,
                "message": self.status_message
            }
            
        except Exception as e:
            error_msg = f"Start error: {str(e)}"
            logger.error(error_msg)
            self.status_message = error_msg
            return {
                "status": "error",
                "active": False,
                "message": self.status_message
            }

    def _run_interaction(self):
        """Wrapper to maintain interaction state"""
        try:
            self.karen.run()
        except Exception as e:
            logger.error(f"Interaction error: {e}")
            with self.lock:
                self.status_message = f"Interaction error: {str(e)}"
                self.is_active = False

    def _stop_karen(self):
        try:
            logger.info("Stopping Karen system...")
            self.status_message = "Stopping system..."
            
            if self.karen:
                self.karen.stop_interaction()
                
                if self.interaction_thread and self.interaction_thread.is_alive():
                    self.interaction_thread.join(timeout=3)
                
                if self.camera_thread and self.camera_thread.is_alive():
                    self.camera_thread.join(timeout=2)
            
            self.is_active = False
            self.status_message = "System ready"
            logger.info("Karen system stopped successfully")
            
            return {
                "status": "success",
                "active": False,
                "message": self.status_message
            }
        except Exception as e:
            error_msg = f"Stop error: {str(e)}"
            logger.error(error_msg)
            self.status_message = error_msg
            return {
                "status": "error",
                "active": False,
                "message": self.status_message
            }

# Initialize system
karen_system = KarenSystem()

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify(karen_system.get_status())

@app.route('/api/toggle', methods=['POST'])
def toggle():
    try:
        return jsonify(karen_system.toggle_system())
    except Exception as e:
        logger.error(f"Toggle error: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "active": False
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)