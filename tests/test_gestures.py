import logging
import os
import unittest
import cv2
from app.camera.gesture.fingers import FingersDetector
from app.camera.gesture.hands import GestureDetector

logger = logging.getLogger("app")

class TestGestureRecognition(unittest.TestCase):
    def setUp(self):
        """
        Set up the GestureRecognition instance.
        """
        self.gesture_recognition = GestureDetector()
        # self.gesture_fingers = FingersDetector()

        self.gestures_folder = os.path.join(os.path.dirname(__file__), "../resources/img/test_gesture_img/")
        self.gestures_folder = os.path.abspath(self.gestures_folder)


    def test_recognize_thumbs_up_gesture(self):
        """
        Test recognizing the 'thumbs up' gesture.
        """
        frame = cv2.imread(self.gestures_folder + '/thump_up.png')

        self.assertIsNotNone(frame, "Frame loading failed. Check if the file path is correct.")

        result = self.gesture_recognition.detect_gesture(frame)
        self.assertIsNotNone(result, "Gesture detection failed.")

        if result and result.gestures:
            self.assertEqual(result.gestures[0][0].category_name, 'Thumb_Up')
            logger.info("Gesture detected successfully passed validations for thumb up!")
        else:
            self.fail("No gestures detected in frame.")

    def test_recognize_thumbs_down_gesture(self):
        """
        Test recognizing the 'thumbs down' gesture.
        """
        frame = cv2.imread(self.gestures_folder + '/thump_down.png')

        self.assertIsNotNone(frame, "Frame loading failed. Check if the file path is correct.")

        result = self.gesture_recognition.detect_gesture(frame)
        self.assertIsNotNone(result, "Gesture detection failed.")

        if result and result.gestures:
            self.assertEqual(result.gestures[0][0].category_name, 'Thumb_Down')
            logger.info("Gesture detected successfully passed validations for thumb up!")

    def test_recognize_open_palm_gesture(self):
        """
        Test recognizing the 'open palm' gesture.
        """
        frame = cv2.imread(self.gestures_folder + '/open_palm.png')

        self.assertIsNotNone(frame, "Frame loading failed. Check if the file path is correct.")

        result = self.gesture_recognition.detect_gesture(frame)
        self.assertIsNotNone(result, "Gesture detection failed.")

        if result and result.gestures:
            self.assertEqual(result.gestures[0][0].category_name, 'Open_Palm')
            logger.info("Gesture detected successfully passed validations for thumb up!")

    def test_recognize_closed_fist_gesture(self):
        """
        Test recognizing the 'closed fist' gesture.
        """
        frame = cv2.imread(self.gestures_folder + '/closed_fist.png')

        self.assertIsNotNone(frame, "Frame loading failed. Check if the file path is correct.")

        result = self.gesture_recognition.detect_gesture(frame)
        self.assertIsNotNone(result, "Gesture detection failed.")

        if result and result.gestures:
            self.assertEqual(result.gestures[0][0].category_name, 'Closed_Fist')
            logger.info("Gesture detected successfully passed validations for thumb up!")

    # def test_recognize_fingers_gesture(self):
    #     """
    #         Test recognizing amount of showing fingers gestures.
    #     """
    #     for fingers_counter in range(0, 11):
    #         frame = cv2.imread(self.gestures_folder + f"fingers_{str(fingers_counter)}.png")
    #
    #         result = self.gesture_recognition.detect_gesture(frame)
    #         self.assertEqual(result['all_fingers'], fingers_counter)
    #         logger.info("Gesture detected successfully passed validations for close fist!")

    # def test_recognize_none_fingers_gesture(self):
    #     """
    #         Test recognizing none of showing fingers.
    #     """
    #     frame = cv2.imread(self.gestures_folder + f"fingers_none.png")
    #
    #     result = self.gesture_recognition.detect_gesture(frame)
    #     self.assertEqual(result['none_gestures'], "None")
    #     logger.info("Gesture detected successfully passed validations for close fist!")


if __name__ == '__main__':
    unittest.main()
