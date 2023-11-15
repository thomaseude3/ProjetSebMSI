import cv2
from pypylon import pylon
from PyQt6.QtCore import QThread, Qt, pyqtSignal


class CameraManager(QThread):
    frame_signal = pyqtSignal(bytearray)  # Signal pour transmettre le frame à la fenêtre principale

    def __init__(self):
        super().__init__()
        self.camera = None

    def run(self):
        tl_factory = pylon.TlFactory.GetInstance()
        self.camera = pylon.InstantCamera()
        self.camera.Attach(tl_factory.CreateFirstDevice())

        #self.camera.Open()
        #self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        try:
            while True:
                grab = self.camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
                if grab.GrabSucceeded():
                    image = grab.Array.tobytes()

                    # Émettre le signal avec le frame capturé en tant que bytearray
                    self.frame_signal.emit(bytearray(image))

        finally:
            self.camera.StopGrabbing()
            self.camera.Close()

    def start_live_video(self):
        if self.camera is not None:
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def stop_live_video(self):
        if self.camera is not None:
            self.camera.StopGrabbing()
