import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class PostureCoach:
    def __init__(self, model_path="pose_landmarker.task"):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)

    def calculate_angle(self, a, b, c):
        """Calculates the angle between three points (normalized coordinates)."""
        a, b, c = np.array(a), np.array(b), np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
            a[1] - b[1], a[0] - b[0]
        )
        angle = np.abs(radians * 180.0 / np.pi)
        return 360 - angle if angle > 180.0 else angle

    def run(self):
        cap = cv2.VideoCapture(0)
        baseline_angle = None

        print("Standardizing... Sit straight and press 'c' to calibrate.")

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
            )
            timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            result = self.detector.detect_for_video(mp_image, timestamp_ms)

            if result.pose_landmarks:
                landmarks = result.pose_landmarks[0]

                # We use the Left side (Ear: 7, Shoulder: 11, Hip: 23)
                # If you sit facing the other way, use 8, 12, 24
                ear = [landmarks[7].x, landmarks[7].y]
                shoulder = [landmarks[11].x, landmarks[11].y]
                hip = [landmarks[23].x, landmarks[23].y]

                current_angle = self.calculate_angle(ear, shoulder, hip)

                # --- CALIBRATION LOGIC ---
                key = cv2.waitKey(5) & 0xFF
                if key == ord("c"):
                    baseline_angle = current_angle
                    print(f"Calibrated! Baseline angle set to: {int(baseline_angle)}")

                if baseline_angle is not None:
                    # If the current angle deviates significantly from baseline, it's a slouch
                    # We use 'abs' to handle both directions of facing the camera
                    diff = abs(current_angle - baseline_angle)

                    status = "GOOD" if diff < 15 else "SLOUCHING"
                    color = (0, 255, 0) if status == "GOOD" else (0, 0, 255)

                    cv2.putText(frame, f"Status: {status}", (50, 50), 2, 1, color, 2)
                    cv2.putText(
                        frame,
                        f"Diff from Baseline: {int(diff)}",
                        (50, 90),
                        2,
                        0.6,
                        (255, 255, 255),
                        1,
                    )
                else:
                    cv2.putText(
                        frame,
                        "Press 'C' to Calibrate",
                        (50, 50),
                        2,
                        1,
                        (0, 255, 255),
                        2,
                    )

                cv2.imshow("Posture Coach", frame)
                if key == ord("q"):
                    break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    coach = PostureCoach()
    coach.run()
