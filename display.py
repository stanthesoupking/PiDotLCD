import math
from display_driver import DisplayDriver

class Display():

    def __init__(self):
        self.driver = DisplayDriver()

        # Turn on display
        self.driver.display_control(True, False, False)

        # Enable graphics mode
        self.driver.set_graphic_display(True)

        # Clear graphics ram
        self.driver.clear_gdram()

        # Create display buffer
        self.display_buffer = []
        for y in range(0,32):
            row = []
            for x in range(0, 16):
                row.append([0x00, 0x00])
            self.display_buffer.append(row)

    def _update_driver_bytes(self, x, y):
        self.driver.set_gdram_bytes(x, y,
            self.display_buffer[y][x])

    def fill_rect(self, x, y, width, height, state = True):
        for rx in range(x, x + width):
            for ry in range(y, y + height):
                self.set_pixel(rx, ry, state)

    def set_pixel(self, x, y, state = True):
        # Constrain x and y
        if not ((0 <= x < 128) and (0 <= y < 64)):
            return

        if y < 32:
            byte_x = x // 16
            byte_y = y
        else:
            byte_x = 8 + (x // 16)
            byte_y = y - 32
        
        byte_mod = 128 >> (x % 8)

        if state:
            self.display_buffer[byte_y][byte_x][(x % 16) // 8] |= byte_mod
        else:
            self.display_buffer[byte_y][byte_x][(x % 16) // 8] &= ~byte_mod

        self._update_driver_bytes(byte_x, byte_y)

    def draw_character(self, x, y, char, font):
        cwidth, cheight = font.get_character_dimensions()
        pixel_data = font.get_character(char)
        
        for cy in range(0, cheight):
            for cx in range(0, cwidth):
                self.set_pixel(x + cx, y + cy, pixel_data[cy][cx])
    
    def draw_string(self, x, y, text, font, wrap = False):
        cwidth, cheight = font.get_character_dimensions()

        if wrap:
            lines = []
            line_length = 128 // cwidth
            total_lines = math.ceil(len(text) / line_length)
            for l in range(0, total_lines):
                take_length = line_length

                doDash = False
                if len(text) > line_length:
                    if text[line_length] != ' ':
                        take_length -= 1
                        doDash = True

                line = text[:take_length]

                if doDash:
                    line += '-'

                text = text[take_length:]

                lines.append(line)
        else:
            lines = [text]
        
        for line in lines:
            i = 0
            for c in line:
                self.draw_character(x + i * cwidth, y, c, font)
                i += 1
            y += cheight