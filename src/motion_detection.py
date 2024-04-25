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
import time


class MotionDetector:
    def __init__(self, camera_streamer, config, sensitivity):
        self.camera_streamer = camera_streamer
        self.prev_frame = self.camera_streamer.get_frame().copy()
        self.prev_gray = cv2.cvtColor(self.prev_frame, cv2.COLOR_BGR2GRAY)
        self.prev_gray = cv2.GaussianBlur(self.prev_gray, (21, 21), 0)
        self.last_detection_time = time.time()
        self.sensitivity = sensitivity
        self.config = config
        self.start_detection()

    def has_detected(self):
        return time.time() - self.last_detection_time <= 30

    def start_detection(self):
        while True:
            frame = self.camera_streamer.get_frame().copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            frame_diff = cv2.absdiff(self.prev_gray, gray)
            _, thresh = cv2.threshold(frame_diff, self.sensitivity, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) < 1000:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                horizontal = x // (frame.shape[1] // self.config.get_horizontal_sections())
                vertical = y // (frame.shape[0] // self.config.get_vertical_sections())
                if not self.config.is_section_enabled(horizontal, vertical):
                    continue
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                self.last_detection_time = time.time()
                cv2.imshow('Motion Detection', frame)
                cv2.waitKey(1)
            self.prev_gray = gray
