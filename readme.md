# 👁️ EyeSpy — Blind Assistance System

**Muhammad Qasim Akram (2152)  &  Asad Farooq (2138)**
BS Computer Science — 6th Semester | Islamia University of Bahawalpur | CS-1013 Computer Vision

A real-time object detection system that helps visually impaired individuals navigate their surroundings using audio feedback.
Built with **Python**, **YOLOv8**, and **OpenCV**.

---

## 📌 What It Does

EyeSpy uses your camera to detect objects in real time and speaks out what it sees — including what the object is, how close it is, and which direction it is coming from.

Example output:
```
person, very close, ahead
car, nearby, on your left. person, ahead, on your right
```

---

## 🧠 How It Works

```
Camera Feed → YOLOv8 Detection → Distance & Direction Estimation → Audio Announcement
```

1. **Camera** captures frames via OpenCV
2. **YOLOv8** scans each frame and identifies objects with bounding boxes
3. **Distance** is estimated by comparing bounding box size to frame size
4. **Direction** is determined by the horizontal position of the object in the frame
5. **Windows Speech API** announces the result out loud

### Distance Categories

| Label | Box Size (relative to frame) |
|-------|------------------------------|
| Very Close | > 25% |
| Nearby | 10% – 25% |
| Ahead | 3% – 10% |
| Far | < 3% |

### Direction Detection

- Left zone (0–35% of frame) → "on your left"
- Center zone (35–65%) → "ahead"
- Right zone (65–100%) → "on your right"

---

## 🗂️ Project Structure

```
EyeSpy/
├── main.py          # entry point, runs camera loop + speech
├── detector.py      # loads YOLOv8, runs inference, draws boxes
├── speaker.py       # text to speech handler
├── utils.py         # distance, direction, priority logic
├── requirements.txt # dependencies
└── .gitignore
```

---

## 🤖 Model & Dataset

| Detail | Info |
|--------|------|
| Model | YOLOv8n (Nano) |
| Dataset | COCO (Common Objects in Context) |
| Training Images | 118,000+ |
| Object Classes | 80 |
| Model Size | ~6 MB |
| Download | Automatic on first run |

The model is pre-trained — no custom training was done. It is downloaded automatically the first time you run the project.

---

## ⚙️ Setup

### Requirements

- Windows 10 or 11
- Python 3.10 or above
- Webcam or a video file

### Install Dependencies

```bash
pip install -r requirements.txt --no-cache-dir
```

---

## ▶️ Running the Project

**Using webcam:**
```bash
python main.py
```

**Using a video file (place it in the project folder):**
```bash
python main.py myvideo.mp4
```

**Using a video file from another location:**
```bash
python main.py "C:\Users\YourName\Videos\myvideo.mp4"
```

Press **Q** to quit.

---

## ⚠️ Known Limitations

- Distance is estimated, not measured (no depth sensor)
- Works best in good lighting
- Only detects the 80 COCO object classes
- May run slower on older hardware (use `yolov8n.pt` for best speed)

---

## 🚀 Possible Future Improvements

- Raspberry Pi deployment for portable use
- GPS integration for outdoor navigation
- Proximity beep sounds (faster beep = closer object)
- Custom model training for specific environments
- Android mobile app version

---

## 👨‍💻 Group Members

| Name | Roll No |
|------|---------|
| Muhammad Qasim Akram | 2152 |
| Asad Farooq | 2138 |

BS Computer Science — 6th Semester
Islamia University of Bahawalpur

---

## 📚 References

- [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com)
- [COCO Dataset](https://cocodataset.org)
- [OpenCV Docs](https://docs.opencv.org)
- [Windows Speech API](https://learn.microsoft.com/en-us/dotnet/api/system.speech.synthesis)