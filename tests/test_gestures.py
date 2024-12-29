import logging
import unittest
from unittest.mock import MagicMock, Mock, patch
from app.camera.gesture.fingers import FingersDetector
from app.camera.gesture.hands import GestureDetector

logger = logging.getLogger("app")

class TestGestureRecognition(unittest.TestCase):
    def setUp(self):
        """
        Set up the GestureRecognition instance.
        """
        self.gesture_recognition = GestureDetector()
        self.gesture_recognition.detect_gesture = MagicMock()
        self.gesture_fingers = FingersDetector()
        self.gesture_fingers.detect_gesture = MagicMock()

    def test_recognize_thumbs_up_gesture(self):
        """
         Test recognizing the 'thumbs up' gesture.
        """
        mock_gesture = Mock()
        mock_gesture.category_name = "Thumb_Up"
        mock_result = MagicMock()
        mock_result.gestures = [[mock_gesture]]

        self.gesture_recognition.detect_gesture.return_value = mock_result

        result = self.gesture_recognition.detect_gesture("mock_frame")

        self.assertIsNotNone(result)
        self.assertEqual(result.gestures[0][0].category_name, "Thumb_Up")


    def test_recognize_thumbs_down_gesture(self):
        """
        Test recognizing the 'thumbs down' gesture.
        """
        mock_gesture = Mock()
        mock_gesture.category_name = "Thumb_Down"
        mock_result = MagicMock()
        mock_result.gestures = [[mock_gesture]]

        self.gesture_recognition.detect_gesture.return_value = mock_result

        result = self.gesture_recognition.detect_gesture("mock_frame")

        self.assertIsNotNone(result)
        self.assertEqual(result.gestures[0][0].category_name, "Thumb_Down")

    def test_recognize_open_palm_gesture(self):
        """
        Test recognizing the 'open palm' gesture.
        """
        mock_gesture = Mock()
        mock_gesture.category_name = "Open_Palm"
        mock_result = MagicMock()
        mock_result.gestures = [[mock_gesture]]

        self.gesture_recognition.detect_gesture.return_value = mock_result

        result = self.gesture_recognition.detect_gesture("mock_frame")

        self.assertIsNotNone(result)
        self.assertEqual(result.gestures[0][0].category_name, "Open_Palm")

    def test_recognize_closed_fist_gesture(self):
        """
        Test recognizing the 'closed fist' gesture.
        """
        mock_gesture = Mock()
        mock_gesture.category_name = "Closed_Fist"
        mock_result = MagicMock()
        mock_result.gestures = [[mock_gesture]]

        self.gesture_recognition.detect_gesture.return_value = mock_result

        result = self.gesture_recognition.detect_gesture("mock_frame")

        self.assertIsNotNone(result)
        self.assertEqual(result.gestures[0][0].category_name, "Closed_Fist")

    def test_recognize_fingers_gesture(self):
        """
            Test recognizing amount of showing fingers gestures.
        """
        for fingers_counter in range(0, 11):
            left_fingers = fingers_counter // 2
            right_fingers = fingers_counter - left_fingers

            mock_result = {
                "left_num_fingers": left_fingers,
                "left_is_open": left_fingers == 5,
                "right_num_fingers": right_fingers,
                "right_is_open": right_fingers == 5,
                "all_fingers": fingers_counter
            }
            self.gesture_fingers.detect_gesture.return_value = mock_result
            result = self.gesture_fingers.detect_gesture("mock_frame")

            self.assertEqual(result['left_num_fingers'], left_fingers)
            self.assertEqual(result['right_num_fingers'], right_fingers)
            self.assertEqual(result['all_fingers'], fingers_counter)
            self.assertEqual(result['left_is_open'], left_fingers == 5)
            self.assertEqual(result['right_is_open'], right_fingers == 5)
            logger.info("Gesture detected successfully passed validations for close fist!")

    def test_recognize_none_fingers_gesture(self):
        """
            Test recognizing none of showing fingers.
        """
        mock_result = {
            "none_gestures": "None",
            "all_fingers": 0,
            "left_num_fingers": 0,
            "right_num_fingers": 0
        }
        self.gesture_fingers.detect_gesture.return_value = mock_result

        result = self.gesture_fingers.detect_gesture("mock_frame")

        self.assertEqual(result['none_gestures'], "None")
        self.assertEqual(result['all_fingers'], 0)
        self.assertEqual(result['left_num_fingers'], 0)
        self.assertEqual(result['right_num_fingers'], 0)

        logger.info("Successfully passed for no fingers detected.")


if __name__ == '__main__':
    unittest.main()
