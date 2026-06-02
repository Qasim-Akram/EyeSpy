import pyttsx3
import time

engine = pyttsx3.init()
engine.setProperty('rate', 145)
engine.setProperty('volume', 1.0)

last_spoken = 0
cooldown = 4.0

def speak(text):
    global last_spoken

    now = time.time()
    if now - last_spoken < cooldown:
        return

    last_spoken = now
    print(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def shutdown():
    pass