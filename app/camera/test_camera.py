from .custom import Camera


class TestCamera(Camera):
    """
    TEMP TEST CLASS.
    """
    def capture_image(self):
        # frame = self.cap.read()
        return "FRAME"
