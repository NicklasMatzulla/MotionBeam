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

import json
from .section import Section


class ConfigManager:
    def __init__(self, config_location):
        self.config_location = config_location
        self.config = self.load_config_from_json()
        self.sections = self.load_sections()

    def load_config_from_json(self):
        with open(self.config_location, 'r') as file:
            return json.load(file)

    def save_config_to_json(self):
        with open(self.config_location, 'w') as file:
            json.dump(self.config, file, indent=4)

    def load_sections(self):
        horizontal_sections = self.config['section']['horizontal']
        vertical_sections = self.config['section']['vertical']
        disabled_sections = self.config['section'].get('disabled', [])
        sections = []
        for i in range(horizontal_sections):
            for j in range(vertical_sections):
                enabled = not {"horizontal": i, "vertical": j} in disabled_sections
                element = Section(i, j, enabled)
                sections.append(element)
        return sections

    def get_horizontal_sections(self):
        return self.config['section']['horizontal']

    def set_horizontal_sections(self, horizontal_sections):
        self.config['section']['horizontal'] = horizontal_sections
        self.save_config_to_json()

    def get_vertical_sections(self):
        return self.config['section']['vertical']

    def set_vertical_sections(self, vertical_sections):
        self.config['section']['vertical'] = vertical_sections
        self.save_config_to_json()

    def get_section(self, horizontal, vertical):
        for section in self.sections:
            if section.get_horizontal() == horizontal and section.get_vertical() == vertical:
                return section
        return None

    def is_section_enabled(self, horizontal, vertical):
        section = self.get_section(horizontal, vertical)
        return section and section.is_enabled()

    def set_section_enabled(self, horizontal, vertical, enabled):
        section = self.get_section(horizontal, vertical)
        if section:
            section.set_enabled(enabled)
            disabled_sections = self.config['section'].get('disabled', [])
            section_entry = {'horizontal': horizontal, 'vertical': vertical}
            if enabled:
                if section_entry in disabled_sections:
                    disabled_sections.remove(section_entry)
            else:
                if section_entry not in disabled_sections:
                    disabled_sections.append(section_entry)
            self.config['section']['disabled'] = disabled_sections
            self.save_config_to_json()
