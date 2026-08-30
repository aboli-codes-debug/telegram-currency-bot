# 🖱️ Hand Gesture Mouse Controller

Control your computer's mouse — move the cursor, left-click, right-click, and drag — using only hand gestures captured by a webcam. Built with real-time computer vision, no extra hardware required.

## How it works

The webcam feed is processed frame-by-frame with **MediaPipe Hands** to track 21 hand landmarks in real time. The position of the index fingertip is mapped from the camera frame to screen coordinates (with exponential smoothing to remove jitter), while the distance between the thumb and other fingertips is used to detect gestures:

| Gesture | Action |
|---|---|
| Move index finger | Move cursor |
| Pinch thumb + index (quick) | Left click |
| Pinch thumb + index (hold) | Drag |
| Pinch thumb + middle finger | Right click |

## Tech stack

- **Python 3**
- **OpenCV** — camera capture and frame rendering
- **MediaPipe** — hand landmark detection
- **PyAutoGUI** — controlling the OS-level mouse cursor
- **NumPy** — coordinate mapping

## Installation

```bash
git clone https://github.com/<your-username>/hand-gesture-mouse.git
cd hand-gesture-mouse
pip install -r requirements.txt
```

## Usage

```bash
python hand_mouse.py
```

Press **`q`** in the camera window to quit.

All behavior — camera index, click sensitivity, cursor smoothing, gesture distance thresholds — can be tuned in the `CONFIG` section at the top of `hand_mouse.py`, no need to touch the rest of the code.

## Demo

*(add a short GIF or video here showing the cursor being controlled by hand — this is the single most convincing thing you can show a potential client)*

## Possible improvements

- Multi-hand support for two-handed gestures
- Scroll gesture (e.g. two-finger swipe)
- On-screen calibration step for different hand sizes / camera distances

## License

MIT
