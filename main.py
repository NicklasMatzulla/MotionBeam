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

import threading
from src.camera_streamer import CameraStreamer
import src.acp as acp
from src.config.config import ConfigManager
from src.motion_detection import MotionDetector

if __name__ == "__main__":
    config_location = "config.json"
    config_manager = ConfigManager(config_location)
    camera_streamer = CameraStreamer(0)
    camera_streamer.start_stream()
    while camera_streamer.get_frame() is None:
        pass
    # noinspection PyPep8
    motion_detection_proc = threading.Thread(
        target=MotionDetector,
        args=(camera_streamer, config_manager, 50)
    )
    motion_detection_proc.start()
    acp.ACP(config_manager, camera_streamer)
