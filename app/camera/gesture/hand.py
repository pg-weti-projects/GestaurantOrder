from ..custom import Camera
from cvzone import HandTrackingModule
import cv2


class GestureDetector(Camera):
    def __init__(self):
        super().__init__()

    def detect_gesture(self, hands):
        gestures = {}
        if hands:
            hand = hands[0]
            fingers = self.hand.fingersUp(hand)
            gestures['num_fingers'] = sum(fingers)
            gestures['is_open'] = all(fingers)
        else:
            gestures['num_fingers'] = 0
            gestures['is_open'] = False
        return gestures

    def display_gestures(self, frame, gestures):
        num_fingers = gestures['num_fingers']
        is_open = gestures['is_open']
        status_text = "Hand Open" if is_open else "Hand Closed"
        cv2.putText(frame, f"Fingers: {num_fingers}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, status_text, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)