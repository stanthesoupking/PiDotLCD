import time
from display import Display
from font import Font

print('Loading font...')

font = Font('./font.png')

print("Starting display test...")

display = Display()

# for x in range(0, 64):
#     display.set_pixel(x, x)

# for x in range(0, 64):
#     display.set_pixel(32 + x, x)

for x in range(0, 128):
    display.set_pixel(x, 0)

    display.set_pixel(x, 63)

for y in range(0, 64):
    display.set_pixel(0, y)

    display.set_pixel(127, y)

display.draw_string(12, 16, 'How was work?', font, wrap = True)

while True:
    display.draw_character(60, 40, chr(3), font)
    time.sleep(0.8)
    display.fill_rect(58, 38, 10, 10, False)
    time.sleep(0.8)