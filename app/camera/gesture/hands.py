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
        gestures = self.detect_gesture(frame)
        gestures = self.display_gestures(frame, gestures)
        return gestures, frame

    def detect_gesture(self, frame):
        """
            Detect gestures in the given frame using MediaPipe.

            Returns:
                GestureRecognizerResult: An object with the following attributes:
                    - gestures (list): A list of recognized gestures, where each gesture contains the category name and
                    confidence score.
                    - handedness (list): A list indicating the handedness (e.g., left or right hand) detected in
                    the frame.
                    - hand_landmarks (list): A list of 3D landmarks of the hand in the image.
                    - hand_world_landmarks (list): A list of 3D landmarks of the hand in world coordinates.
                If no gestures are detected, these attributes will be empty lists.
        """
        if self.recognizer is None:
            self.load_model()

        if frame is None or frame.size == 0:
            logger.error("Frame is empty.")
            return None
        # Convert frame BGR to RGB for MediaPipe
        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except cv2.error as e:
            logger.error(f"OpenCV error during color conversion: {e}")
            return None
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        try:
            gesture_result = self.recognizer.recognize(mp_image)
        except Exception as e:
            logger.error(f"Error during gesture recognition: {e}")
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
                return gesture_name
        else:
            cv2.putText(frame, "No gesture detected", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2, cv2.LINE_AA)
            return "None"
