import cv2
import sys
from detector import ObjectDetector
from speaker import Speaker
from utils import build_announcement, get_priority


def main():
    
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cant open camera. Check if its connected.")
        sys.exit(1)

    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detector = ObjectDetector(model_path="yolov8n.pt", confidence=0.45)
    speaker = Speaker()

   
    speaker.speak("Blind assistance system started. Camera is active.")


    print("Running. Press Q to quit.")

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Couldnt read frame from camera")
            break

        frame_count += 1

       
        if frame_count % 5 != 0:
            cv2.imshow("Blind Assistance - Press Q to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        height, width = frame.shape[:2]

        detections = detector.detect(frame)

        detections.sort(key=lambda d: get_priority(d['label']), reverse=True)

       
        message = build_announcement(detections, width, height)

        if message:
            print(f"Detected: {message}")
            speaker.speak(message)

        frame = detector.draw_boxes(frame, detections)

        
        cv2.putText(frame, f"Objects: {len(detections)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        cv2.imshow("Blind Assistance - Press Q to quit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    speaker.shutdown()
    print("System stopped.")


if __name__ == "__main__":
    main()