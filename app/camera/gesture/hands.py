import logging
from ..user_camera import UserCamera
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

logger = logging.getLogger("app")


class GestureDetector(UserCamera):
    def __init__(self, mode='mediapipe'):
        """
            Initialize the GestureDetector instance.

            mode (str): The mode of the camera is 'mediapipe'.
        """
        super().__init__(mode=mode)
        self.recognizer = None
        self.load_model()

    def load_model(self):
        """
            Load the gesture recognizer model.
        """
        model_file = open('resources/gesture_recognizer.task', "rb")
        model_data = model_file.read()
        model_file.close()
        base_options = python.BaseOptions(model_asset_buffer=model_data)
        options = vision.GestureRecognizerOptions(base_options=base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def process_frame(self, frame):
        """
            Processes a video frame to detect and display gestures.
        """
        if frame is None or frame.size == 0:
            logger.error("Frame is empty.")
            return None, frame

        gestures = self.detect_gesture(frame)
        gestures = self.display_gestures(frame, gestures)
        return gestures, frame

    def detect_gesture(self, frame):
        """
            Convert the frame from BGR to RGB and detect gestures using MediaPipe.
        """
        if self.recognizer is None:
            self.load_model()
        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
            gesture_result = self.recognizer.recognize(mp_image)
            return gesture_result
        except cv2.error as e:
            logger.error(f"Error during color conversion: {e}")
        except Exception as e:
            logger.error(f"Error during gesture recognition: {e}")

        return None

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
                return gesture_name
        else:
            cv2.putText(frame, "No gesture detected", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2, cv2.LINE_AA)
            return "None"
