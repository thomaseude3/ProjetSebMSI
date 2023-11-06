import cv2
from pypylon import pylon
from PyQt6.QtCore import QThread, Qt, pyqtSignal

class CameraManager(QThread):
    frame_signal = pyqtSignal(bytearray)  # Signal pour transmettre le frame à la fenêtre principale

    def run(self):
        tl_factory = pylon.TlFactory.GetInstance()
        camera = pylon.InstantCamera()
        camera.Attach(tl_factory.CreateFirstDevice())

        camera.Open()
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        try:
            while True:
                grab = camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
                if grab.GrabSucceeded():
                    image = grab.Array.tobytes()

                    # Émettre le signal avec le frame capturé en tant que bytearray
                    self.frame_signal.emit(bytearray(image))

        finally:
            camera.StopGrabbing()
            camera.Close()
