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
from flask import Flask, render_template, Response, request


class ACP:
    def __init__(self, config_manager, camera_streamer):
        self.app = Flask(__name__, template_folder='../htdocs/templates', static_folder='../htdocs/static')
        self.camera_streamer = camera_streamer
        self.config_manager = config_manager
        self.section_width = None
        self.section_height = None
        self.border_thickness = 1
        self.border_color = (155, 155, 155)
        self.app.route('/')(self.index)
        self.app.route('/configuration')(self.configuration)
        self.app.route('/sections')(self.sections)
        self.app.route('/toggle_section', methods=['POST'])(self.toggle_section)
        self.app.route('/video_feed')(self.video_feed)
        self.app.run(port=80)

    # noinspection PyUnresolvedReferences
    def configuration(self):
        return render_template('configuration.html')

    def index(self):
        return self.app.redirect('/sections', code=301)

    # noinspection PyUnresolvedReferences
    def sections(self):
        horizontal_sections = self.config_manager.get_horizontal_sections()
        vertical_sections = self.config_manager.get_vertical_sections()
        sections_enabled = [
            [self.config_manager.is_section_enabled(x, y) for x in range(horizontal_sections)]
            for y in range(vertical_sections)
        ]
        return render_template(
            'sections.html',
            NUM_SECTIONS_X=horizontal_sections,
            NUM_SECTIONS_Y=vertical_sections,
            sections_enabled=sections_enabled
        )

    def generate_frames(self):
        while True:
            frame = self.camera_streamer.get_frame()
            copied_frame = frame.copy()
            processed_frame = self.process_sections(copied_frame)
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def process_sections(self, frame):
        height, width, _ = frame.shape
        horizontal_sections = self.config_manager.get_horizontal_sections()
        vertical_sections = self.config_manager.get_vertical_sections()
        if self.section_width is None or self.section_height is None:
            self.section_width = width // horizontal_sections
            self.section_height = height // vertical_sections

        for y in range(vertical_sections):
            for x in range(horizontal_sections):
                if not self.config_manager.is_section_enabled(x, y):
                    frame[
                        y * self.section_height:(y + 1) * self.section_height,
                        x * self.section_width:(x + 1) * self.section_width
                    ] = self.border_color

                frame[
                    y * self.section_height:(y + 1) * self.section_height,
                    x * self.section_width - self.border_thickness:x * self.section_width
                ] = self.border_color

                frame[
                    y * self.section_height - self.border_thickness:y * self.section_height,
                    x * self.section_width:(x + 1) * self.section_width
                ] = self.border_color

        return frame

    def toggle_section(self):
        x = int(request.form['x'])
        y = int(request.form['y'])
        enabled = not self.config_manager.is_section_enabled(x, y)
        self.config_manager.set_section_enabled(x, y, enabled)
        return ""

    def video_feed(self):
        return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
