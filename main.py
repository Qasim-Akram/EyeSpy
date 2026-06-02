import cv2
import sys
import time
import subprocess
from detector import ObjectDetector
from utils import build_announcement, get_priority

last_spoken = 0
cooldown = 5.0

def speak(text):
    global last_spoken
    now = time.time()
    if now - last_spoken < cooldown:
        return
    last_spoken = now
    print(f"Speaking: {text}")
    # use windows built in speech instead of pyttsx3
    # this never gets stuck because each call is a fresh process
    cmd = f'Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Rate = 1; $s.Speak("{text}")'
    subprocess.Popen(["powershell", "-Command", cmd])

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cant open camera.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detector = ObjectDetector(model_path="yolov8n.pt", confidence=0.45)

    print("Running. Press Q to quit.")
    speak("EyeSpy started")

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cant read frame")
            break

        frame_count += 1

        if frame_count % 20 != 0:
            cv2.imshow("EyeSpy - Press Q to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        height, width = frame.shape[:2]

        detections = detector.detect(frame)
        detections.sort(key=lambda d: get_priority(d['label']), reverse=True)

        message = build_announcement(detections, width, height)
        print(f"Detected: {message}")

        if message:
            speak(message)

        frame = detector.draw_boxes(frame, detections)
        cv2.putText(frame, f"Objects: {len(detections)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.imshow("EyeSpy - Press Q to quit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()