#  Copyright (c) 2024 Nicklas Matzulla
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import cv2
import threading


class CameraStreamer:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.frame = None
        self.running = False
        self.thread = threading.Thread(target=self._capture_frames)

    def _capture_frames(self):
        self.running = True
        camera = cv2.VideoCapture(self.camera_id)
        if not camera.isOpened():
            print(f"Error: Could not open camera {self.camera_id}")
            return

        while self.running:
            ret, frame = camera.read()
            if not ret:
                print(f"Error: Failed to capture frame from camera {self.camera_id}")
                break
            self.frame = frame

        camera.release()

    def start_stream(self):
        self.thread.start()

    def stop_stream(self):
        self.running = False
        self.thread.join()

    def get_frame(self):
        return self.frame
