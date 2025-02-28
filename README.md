# 🐶 RoboPup – AI-Powered Gesture-Controlled Robotic Dog

RoboPup is a robotic dog built with the AI Lite Kit and Python. It responds to hand gestures using OpenCV and MediaPipe and moves based on HTTP-based commands.

## 🚀 Features

- **Hand Gesture Recognition** – Uses OpenCV and MediaPipe for detecting finger gestures.
- **Wi-Fi Control** – Sends movement commands over HTTP.
- **Predefined Tricks** – Performs an "Excited Hop" or "Twister" move based on thumb gestures.
- **Real-Time Video Processing** – Uses a webcam to analyze gestures.

## 🛠️ Setup

### Prerequisites

Ensure you have Python installed and the following dependencies:

```bash
pip install requests tensorflow opencv-python mediapipe numpy
```

### Hardware

- **Meritus AI Lite Kit**
- **Camera (for gesture recognition)**
- **Wi-Fi-enabled Microcontroller** (ESP-based recommended)

## 🔧 Configuration

Modify the `host` variable in `robopup.py` to match your RoboPup's IP address:

```python
host = '192.168.91.20'  # Change to your robot's IP
port = 80
```

## 🎮 Controls

| Gesture         | Action       |
|---------------|------------|
| Index Finger Up | Move Forward |
| Index Finger Down | Move Backward |
| Hand Left | Turn Left |
| Hand Right | Turn Right |
| Thumbs Up | Excited Hop |
| Thumbs Down | Twister |

<h2>🛠️ Installation Steps:</h2>

- Clone the repo

```
git clone https://github.com/adharvarun/RoboPup.git
```

- Open the directory

```
cd RoboPup
```

- Install the Dependencies

```
pip install -r requirements.txt
```

- Connect to the WiFi Network of your Meritus AI Lite Kit

- Run the script

```
python main.py
```

## 🖥️ Demonstration

1. Launch the script.
2. Show hand gestures in front of the camera.
3. Watch RoboPup respond in real-time!

## 📜 License

This project is Unlicensed
