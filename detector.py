from ultralytics import YOLO
import cv2

class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt", confidence=0.45):
        print("Loading model, please wait...")
        self.model = YOLO(model_path)
        self.confidence = confidence
        print("Model loaded ok")

    def detect(self, frame):
        results = self.model(frame, conf=self.confidence, verbose=False)

        detections = []

        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue

            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                conf = float(box.conf[0])
                class_id = int(box.cls[0])

                label = self.model.names[class_id]

                detections.append({
                    'box': (x1, y1, x2, y2),
                    'confidence': conf,
                    'label': label,
                    'class_id': class_id
                })

        return detections

    def draw_boxes(self, frame, detections):
        for det in detections:
            x1, y1, x2, y2 = det['box']
            label = det['label']
            conf = det['confidence']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            text = f"{label} {conf:.2f}"
            cv2.putText(
                frame, text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 255, 0), 2
            )

        return frame