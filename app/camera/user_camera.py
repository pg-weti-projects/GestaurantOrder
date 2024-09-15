import cv2
import mediapipe as mp
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QImage


class UserCamera(QObject):
    frame_ready = Signal(QImage)

    def __init__(self, logger):
        super().__init__()
        self.__logger = logger
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.running = True

        if not self.cap.isOpened():
            raise ValueError("Could not open video stream from selected camera!")

    def capture_image(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                output_img = frame.copy()
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detect hands
                with self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                                         min_tracking_confidence=0.5) as hands:

                    results = hands.process(rgb_frame)  # Przetworzenie obrazu z użyciem MediaPipe

                    # if detect hands
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_drawing.draw_landmarks(image=output_img, landmark_list=hand_landmarks,
                                                           connections=self.mp_hands.HAND_CONNECTIONS)

                        self.countFingers(output_img, results, draw=True)

                h, w, ch = output_img.shape
                q_img = QImage(output_img.data, w, h, ch * w, QImage.Format_RGB888)
                self.frame_ready.emit(q_img)

    def countFingers(self, image, results, draw=True, display=True):
        count = {'RIGHT': 0, 'LEFT': 0}
        finger_tips_ids = [self.mp_hands.HandLandmark.INDEX_FINGER_TIP, self.mp_hands.HandLandmark.RING_FINGER_TIP,
                           self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP, self.mp_hands.HandLandmark.PINKY_TIP]
        fingers_statuses = {'RIGHT_THUMB': False, 'LEFT_THUMB': False, 'RIGHT_INDEX': False, 'LEFT_INDEX': False,
                            'RIGHT_PINKY': False, 'LEFT_PINKY': False, 'RIGHT_MIDDLE': False, 'LEFT_MIDDLE': False,
                            'RIGHT_RING': False, 'LEFT_RING': False}

        for hand_index, hand_info in enumerate(results.multi_handedness):
            hand_label = hand_info.classification[0].label
            hand_landmarks = results.multi_hand_landmarks[hand_index]
            for tip_id in finger_tips_ids:
                self.__logger.info(tip_id)
                finger_name = tip_id.name.split("_")[0]
                self.__logger.info(finger_name)
                if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
                    fingers_statuses[hand_label.upper()+"_"+finger_name] = True
                    ok = hand_label.upper() + "_" + finger_name
                    self.__logger.info(ok)
                    count[hand_label.upper()] += 1
                    if draw:
                        cv2.circle(image, (int(hand_landmarks.landmark[tip_id].x * image.shape[1]),
                                           int(hand_landmarks.landmark[tip_id].y * image.shape[0])), 10, (0, 255, 0), cv2.FILLED)

            thumb_tip_x = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x
            thumb_mcp_x = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP - 2].x
            self.__logger.info(hand_label)
            self.__logger.info(thumb_tip_x)
            self.__logger.info(thumb_mcp_x)
            if (hand_label == 'Right' and (thumb_tip_x < thumb_mcp_x)) or (hand_label == 'Left' and (thumb_tip_x > thumb_mcp_x)):
                fingers_statuses[hand_label.upper()+"_THUMB"] = True
                count[hand_label.upper()] += 1
                if draw:
                    cv2.circle(image, (int(hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x * image.shape[1]),
                                       int(hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y * image.shape[0])), 10, (0, 255, 0), cv2.FILLED)

        # Display information about number of fingers
        if draw:
            cv2.putText(image, f'Right Hand: {count["RIGHT"]} Fingers', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f'Left Hand: {count["LEFT"]} Fingers', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        return count

    def stop(self):
        self.running = False

    def __del__(self):
        self.cap.release()
