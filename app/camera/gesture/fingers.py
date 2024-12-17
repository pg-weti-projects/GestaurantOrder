from ..user_camera import UserCamera
import cv2
from cvzone import HandTrackingModule


class FingersDetector(UserCamera):
    def __init__(self, mode='fingers'):
        """
            Initialize the FingersDetector instance.
            mode (str): The mode of the camera is 'fingers'.
        """
        super().__init__(mode=mode)
        self.hand = HandTrackingModule.HandDetector()

    def process_frame(self, frame):
        """
        Processes a video frame to detect and display gestures.
        """
        hands, frame = self.hand.findHands(frame)
        gestures = self.detect_gesture(hands)
        gestures = self.display_gestures(frame, gestures)
        return gestures, frame

    def detect_gesture(self, hands):
        gestures = {}

        # Handle case where two hands are detected
        if hands and len(hands) == 2:
            left = hands[0]
            right = hands[1]
            right_fingers = self.hand.fingersUp(right)
            left_fingers = self.hand.fingersUp(left)

            gestures['left_num_fingers'] = sum(left_fingers)
            gestures['left_is_open'] = all(left_fingers)

            gestures['right_num_fingers'] = sum(right_fingers)
            gestures['right_is_open'] = all(right_fingers)

            gestures['all_fingers'] = sum(left_fingers) + sum(right_fingers)

        # Handle case where only one hand is detected
        elif hands and len(hands) == 1:
            left = hands[0]
            left_fingers = self.hand.fingersUp(left)

            gestures['left_num_fingers'] = sum(left_fingers)
            gestures['left_is_open'] = all(left_fingers)

            gestures['right_num_fingers'] = 0
            gestures['right_is_open'] = False

            gestures['all_fingers'] = sum(left_fingers)

        # Handle case where no hands are detected
        else:
            gestures['left_num_fingers'] = 0
            gestures['left_is_open'] = False
            gestures['right_num_fingers'] = 0
            gestures['right_is_open'] = False
            gestures['all_fingers'] = 0
            gestures['none_gestures'] = "None"

        return gestures

    def display_gestures(self, frame, gestures) -> str:

        # Display and return None gesture
        if 'none_gestures' in gestures:
            cv2.putText(frame, "None gestures", (10, 70),  # Y = 70
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            return gestures['none_gestures']

        # Display Left Hand Info
        left_num_fingers = gestures.get('left_num_fingers', 0)
        left_is_open = gestures.get('left_is_open', False)
        left_status_text = "Hand Open" if left_is_open else "Hand Closed"

        cv2.putText(frame, f"Fingers Left: {left_num_fingers}", (10, 70),  # Y = 70
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, left_status_text, (10, 120),  # Y = 120
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Display Right Hand Info
        right_num_fingers = gestures.get('right_num_fingers', 0)
        right_is_open = gestures.get('right_is_open', False)
        right_status_text = "Hand Open" if right_is_open else "Hand Closed"

        cv2.putText(frame, f"Fingers Right: {right_num_fingers}", (10, 170),  # Y = 170 (shifted down)
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, right_status_text, (10, 220),  # Y = 220 (shifted down)
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        return str(left_num_fingers + right_num_fingers)
