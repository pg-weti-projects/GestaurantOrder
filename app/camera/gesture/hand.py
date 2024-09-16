from ..custom import Camera
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class GestureDetector(Camera):
    def __init__(self, mode='mediapipe'):
        """
            Initialize the GestureDetector instance.

            mode (str): The mode of the camera is 'mediapipe'.
        """
        super().__init__(mode=mode)
        base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
        options = vision.GestureRecognizerOptions(base_options=base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def detect_gesture(self, frame):
        if frame is None or frame.size == 0:
            print("Error: Frame is empty.")
            return None
        # Convert frame BGR to RGB for MediaPipe
        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except cv2.error as e:
            print(f"OpenCV error during color conversion: {e}")
            return None
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        try:
            gesture_result = self.recognizer.recognize(mp_image)
        except Exception as e:
            print(f"Error during gesture recognition: {e}")
            return None

        return gesture_result

    def display_gestures(self, frame, gestures):
        """
            Display the recognized gesture and its confidence score.
        """
        if gestures.gestures:
            for gesture in gestures.gestures:
                gesture_name = gesture[0].category_name
                score = gesture[0].score
                cv2.putText(frame, f"Gesture: {gesture_name} ({score:.2f})",
                            (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "No gesture detected", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2, cv2.LINE_AA)