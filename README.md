# 🧘‍♂️ Real-Time Posture Coach

A computer vision application that monitors your sitting posture in real-time and alerts you when you begin to slouch. Built using **MediaPipe Pose Landmarker (v2)** and **OpenCV**, optimized for modern Python workflows with **uv**.

## 🚀 The Problem

"Desk Neck" and poor sitting posture are common issues in our community of students and remote workers. Long hours at a computer often lead to unconscious slouching, which causes long-term back and neck pain. This project provides a **real-time, privacy-focused** solution to build better habits.

## ✨ Key Features

- **Dynamic Calibration:** Don't settle for hardcoded angles. Calibrate the app to _your_ specific "good posture" with one keystroke.
- **High Performance:** Uses MediaPipe's Task API for smooth, real-time tracking (30+ FPS).
- **Visual Feedback:** On-screen alerts change from Green to Red immediately when slouching is detected.
- **Privacy-First:** All processing happens locally on your machine; no video data is sent to the cloud.

---

## 🛠️ Setup & Installation

This project uses `uv` for lightning-fast dependency management.

1.  **Clone the Repository:**

    ```bash
    git clone <your-repo-link>
    cd posture-coach
    ```

2.  **Install Dependencies:**

    ```bash
    uv sync
    ```

3.  **Download the Model:**
    The application requires the MediaPipe Pose Landmarker model.
    ```bash
    curl -o pose_landmarker.task https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task
    ```

---

## 🎮 How to Use

1.  **Run the Application:**
    ```bash
    uv run app.py
    ```
2.  **Calibrate:** Sit up straight in your ideal working position and face the camera (side view works best). Press the **'C'** key on your keyboard.
3.  **Monitor:** The app will now track the "Difference" from your baseline. If you lean forward or slouch, the status will flip to **SLOUCHING**.
4.  **Exit:** Press **'Q'** to close the application.

---

## 🧠 Technical Implementation

### Landmark Logic

The coach tracks three key points on the user's body: **Ear (7), Shoulder (11), and Hip (23)**.

### The Math

We calculate the angle $\theta$ between these three points. Rather than using a fixed threshold (e.g., 160°), we calculate the **Absolute Deviation** from your calibrated baseline:
$$\text{Difference} = | \theta_{current} - \theta_{calibrated} |$$
If the difference exceeds **15 degrees**, an alert is triggered.

---

## 📝 Reflection & Challenges

- **Challenge:** Standard fixed-angle detection failed depending on camera height and user orientation.
- **Solution:** Implemented a **Baseline Calibration** system that calculates the relative difference, making the tool robust for any setup.
- **Future Scope:** Adding an audio alert or a "Time-spent-slouching" counter to the final report.

## 📦 Requirements

- Python 3.9+
- `mediapipe`
- `opencv-python`
- `numpy`
