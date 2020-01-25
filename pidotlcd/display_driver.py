import spidev
import time

class DisplayDriver:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)

        self.spi.max_speed_hz = 600000 #540 khz
        self.spi.cshigh = True

        # Turn display on
        self.display_control(True, cursor = True, character_blink = True)
    
    def send_instruction(self, rs, rw, data):
        # Output bytes (3)
        out = [0x00, 0x00, 0x00]

        # Write synchronisation string
        out[0] = (0b1111_1000 | (rs << 1) | (rw << 2))

        # Write higher data (first 4 bits)
        out[1] = (data & 0b1111_0000)

        # Write lower data (last 4 bits)
        out[2] = (data << 4)

        self.spi.writebytes(out)
    
    def send_instructions(self, instructions):
        out = [0x00] * len(instructions) * 3
        i = 0
        for (rs, rw, data) in instructions:
            # Write synchronisation string
            out[i] = (0b1111_1000 | (rs << 1) | (rw << 2))
            i += 1

            # Write higher data (first 4 bits)
            out[i] = (data & 0b1111_0000)
            i += 1

            # Write lower data (last 4 bits)
            out[i] = (data << 4)
            i+= 1

        self.spi.writebytes(out)

    def display_control(self, display_on, cursor = False, character_blink = False):
        data = 0b0000_1000

        if (display_on):
            data = data | 0b0000_0100

        if (cursor):
            data = data | 0b0000_0010

        if (character_blink):
            data = data | 0b0000_0001

        self.send_instruction(0, 0, data)
    
    def _set_extended_function_set(self, extended):
        data = 0b0010_0000

        if (extended):
            data = data | 0b0000_0100

        self.send_instruction(0, 0, data)
    
    def set_graphic_display(self, graphic_display):
        self._set_extended_function_set(True)

        data = 0b0010_0100

        if (graphic_display):
            data = data | 0b0000_0010

        self.send_instruction(0, 0, data)

    def _set_gdram_address(self, x, y):
        self.send_instructions([
            (0, 0, 0b1000_0000 | (y & 0b0011_1111)),
            (0, 0, 0b1000_0000 | (x & 0b0000_1111))
        ])
        
    def set_gdram_bytes(self, x, y, gdram_bytes = [0x00, 0x00]):
        self._set_gdram_address(x, y)

        instructions = [ (1, 0, data) for data in gdram_bytes ]
        self.send_instructions(instructions)

    def clear_gdram(self):
        for y in range(0, 32):
            for x in range(0, 16):
                self.set_gdram_bytes(x, y, [0x00, 0x00])

    def clear(self):
        self.send_instruction(0, 0, 0b0000_0001)

    def close(self):
        self.spi.close()