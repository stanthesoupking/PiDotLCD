# Import from parent directory
import sys
sys.path.insert(0,'..')

import time
from pidotlcd import Display, Font

print('Loading font...')
font = Font('./font.png')

print("Starting display test...")

display = Display()
display.draw_string(30, 16, 'Hello Pi!', font)
display.draw_rect(0, 0, 128, 64)

while True:
    display.draw_character(60, 40, chr(3), font)
    time.sleep(0.8)
    display.fill_rect(58, 38, 10, 10, False)
    time.sleep(0.8)