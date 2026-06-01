import pyttsx3
import threading
import time


# this class handles all the voice stuff
# we run speech in a seperate thread so it doesnt block the camera feed
class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()

        # set speed, 150 is comfortable not too fast not too slow
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

        self.is_speaking = False
        self.last_spoken_time = 0

        # how many seconds to wait before speaking again
        # we dont want it to keep repeating every single frame
        self.cooldown = 3.0

        self.lock = threading.Lock()

    def speak(self, text):
        # check if enough time has passed since last announcement
        current_time = time.time()
        if current_time - self.last_spoken_time < self.cooldown:
            return

        if self.is_speaking:
            return

        # run in background thread so camera doesnt freeze
        def _speak():
            with self.lock:
                self.is_speaking = True
                self.engine.say(text)
                self.engine.runAndWait()
                self.is_speaking = False

        self.last_spoken_time = current_time
        t = threading.Thread(target=_speak, daemon=True)
        t.start()

    def set_cooldown(self, seconds):
        # lets you change how often it speaks
        self.cooldown = seconds

    def shutdown(self):
        # cleanup when program exits
        self.engine.stop()