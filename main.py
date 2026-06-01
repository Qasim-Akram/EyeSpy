import cv2
import sys
from detector import ObjectDetector
from speaker import Speaker
from utils import build_announcement, get_priority


def main():
    # open default camera (0 = built in webcam)
    # change to 1 if you have external camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cant open camera. Check if its connected.")
        sys.exit(1)

    # set resolution, 640x480 is fine for yolo
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detector = ObjectDetector(model_path="yolov8n.pt", confidence=0.45)
    speaker = Speaker()

    # speak once at start so user knows system is on
    speaker.speak("Blind assistance system started. Camera is active.")

    print("Running. Press Q to quit.")

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Couldnt read frame from camera")
            break

        frame_count += 1

        # dont process every single frame, every 5th frame is enough
        # reduces cpu load without making it feel slow
        if frame_count % 5 != 0:
            cv2.imshow("Blind Assistance - Press Q to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        height, width = frame.shape[:2]

        # detect objects in current frame
        detections = detector.detect(frame)

        # sort by priority so dangerous things are mentioned first
        detections.sort(key=lambda d: get_priority(d['label']), reverse=True)

        # build speech message
        message = build_announcement(detections, width, height)

        if message:
            print(f"Detected: {message}")
            speaker.speak(message)

        # draw boxes on frame for visual display
        frame = detector.draw_boxes(frame, detections)

        # show frame count and detection count on screen
        cv2.putText(frame, f"Objects: {len(detections)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        cv2.imshow("Blind Assistance - Press Q to quit", frame)

        # q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # cleanup
    cap.release()
    cv2.destroyAllWindows()
    speaker.shutdown()
    print("System stopped.")


if __name__ == "__main__":
    main()