from PIL import Image

class Font:
    def __init__(self, path):
        # Character data buffer
        self.characters = []

        # Open font source image
        image = Image.open(path)
        
        # Get character dimensions
        w, h = image.size
        cwidth, cheight = (w // 16, h // 16)
        self.cdim = (cwidth, cheight)

        # Get monochrome conversion
        mono_im = image.convert('1')

        # Load pixel data into character buffer
        i = 0
        for y in range(0, 16):
            for x in range(0, 16):
                self.characters.append([])
                for cy in range(0, cheight):
                    row = []
                    for cx in range(0, cwidth):
                        px = x * cwidth + cx
                        py = y * cheight + cy
                        row.append(mono_im.getpixel((px, py)) == 255)
                    self.characters[i].append(row)
                i += 1

        # Close source image stream                
        image.close()
    
    def get_character(self, char):
        return self.characters[ord(char)]
    
    def get_character_dimensions(self):
        return self.cdim
