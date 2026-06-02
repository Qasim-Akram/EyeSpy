import cv2
import sys
import time
import subprocess
from detector import ObjectDetector
from utils import build_announcement, get_priority

last_spoken = 0
cooldown = 3.0

ps_process = subprocess.Popen(
    ["powershell", "-NoExit", "-Command", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    text=True
)

def speak(text):
    global last_spoken
    now = time.time()
    if now - last_spoken < cooldown:
        return
    last_spoken = now
    print(f"Speaking: {text}")
    cmd = f'Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Rate = 3; $s.Speak("{text}")\n'
    ps_process.stdin.write(cmd)
    ps_process.stdin.flush()

def main():
    # check if user passed a video file as argument
    if len(sys.argv) > 1:
        source = sys.argv[1]
        print(f"Using video file: {source}")
    else:
        source = 0
        print("Using webcam")

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Cant open: {source}")
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
            # if video file ended, just stop
            if source != 0:
                print("Video finished.")
            else:
                print("Cant read frame")
            break

        frame_count += 1

        if frame_count % 10 != 0:
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
    ps_process.stdin.close()
    ps_process.terminate()

if __name__ == "__main__":
    main()