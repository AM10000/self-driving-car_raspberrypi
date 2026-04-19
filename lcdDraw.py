import pigpio
import time
import os
from PIL import Image
class lcd():
    def __init__(self):
        self.DATA_PINS = [17, 27, 22, 26, 23, 24, 25, 4]
        self.LCD_RD, self.LCD_WR, self.LCD_CD, self.LCD_CS, self.LCD_RST = 10, 18, 7, 8, 9
        self.WR_MASK = (1 << self.LCD_WR)
        self.WIDTH = 240
        self.HEIGHT = 320
        self.pi = pigpio.pi()
        if not self.pi.connected:
            exit("Start pigpiod first: sudo pigpiod")
        self.FONT = {
            ' ': [0x00, 0x00, 0x00, 0x00, 0x00], '!': [0x00, 0x00, 0x5F, 0x00, 0x00],
            '"': [0x00, 0x07, 0x00, 0x07, 0x00], '#': [0x14, 0x7F, 0x14, 0x7F, 0x14],
            '$': [0x24, 0x2A, 0x7F, 0x2A, 0x12], '%': [0x23, 0x13, 0x08, 0x64, 0x62],
            '&': [0x36, 0x49, 0x55, 0x22, 0x50], "'": [0x00, 0x05, 0x03, 0x00, 0x00],
            '(': [0x00, 0x1C, 0x22, 0x41, 0x00], ')': [0x00, 0x41, 0x22, 0x1C, 0x00],
            '*': [0x14, 0x08, 0x3E, 0x08, 0x14], '+': [0x08, 0x08, 0x3E, 0x08, 0x08],
            ',': [0x00, 0x50, 0x30, 0x00, 0x00], '-': [0x08, 0x08, 0x08, 0x08, 0x08],
            '.': [0x00, 0x60, 0x60, 0x00, 0x00], '/': [0x20, 0x10, 0x08, 0x04, 0x02],
            '0': [0x3E, 0x51, 0x49, 0x45, 0x3E], '1': [0x00, 0x42, 0x7F, 0x40, 0x00],
            '2': [0x42, 0x61, 0x51, 0x49, 0x46], '3': [0x21, 0x41, 0x45, 0x4B, 0x31],
            '4': [0x18, 0x14, 0x12, 0x7F, 0x10], '5': [0x27, 0x45, 0x45, 0x45, 0x39],
            '6': [0x3C, 0x4A, 0x49, 0x49, 0x30], '7': [0x01, 0x71, 0x09, 0x05, 0x03],
            '8': [0x36, 0x49, 0x49, 0x49, 0x36], '9': [0x06, 0x49, 0x49, 0x29, 0x1E],
            ':': [0x00, 0x36, 0x36, 0x00, 0x00], ';': [0x00, 0x56, 0x36, 0x00, 0x00],
            '<': [0x08, 0x14, 0x22, 0x41, 0x00], '=': [0x14, 0x14, 0x14, 0x14, 0x14],
            '>': [0x00, 0x41, 0x22, 0x14, 0x08], '?': [0x02, 0x01, 0x51, 0x09, 0x06],
            '@': [0x32, 0x49, 0x79, 0x41, 0x3E], 'A': [0x7E, 0x11, 0x11, 0x11, 0x7E],
            'B': [0x7F, 0x49, 0x49, 0x49, 0x36], 'C': [0x3E, 0x41, 0x41, 0x41, 0x22],
            'D': [0x7F, 0x41, 0x41, 0x22, 0x1C], 'E': [0x7F, 0x49, 0x49, 0x49, 0x41],
            'F': [0x7F, 0x09, 0x09, 0x09, 0x01], 'G': [0x3E, 0x41, 0x49, 0x49, 0x7A],
            'H': [0x7F, 0x08, 0x08, 0x08, 0x7F], 'I': [0x00, 0x41, 0x7F, 0x41, 0x00],
            'J': [0x20, 0x40, 0x41, 0x3F, 0x01], 'K': [0x7F, 0x08, 0x14, 0x22, 0x41],
            'L': [0x7F, 0x40, 0x40, 0x40, 0x40], 'M': [0x7F, 0x02, 0x0C, 0x02, 0x7F],
            'N': [0x7F, 0x04, 0x08, 0x10, 0x7F], 'O': [0x3E, 0x41, 0x41, 0x41, 0x3E],
            'P': [0x7F, 0x09, 0x09, 0x09, 0x06], 'Q': [0x3E, 0x41, 0x51, 0x21, 0x5E],
            'R': [0x7F, 0x09, 0x19, 0x29, 0x46], 'S': [0x46, 0x49, 0x49, 0x49, 0x31],
            'T': [0x01, 0x01, 0x7F, 0x01, 0x01], 'U': [0x3F, 0x40, 0x40, 0x40, 0x3F],
            'V': [0x1F, 0x20, 0x40, 0x20, 0x1F], 'W': [0x3F, 0x40, 0x38, 0x40, 0x3F],
            'X': [0x63, 0x14, 0x08, 0x14, 0x63], 'Y': [0x07, 0x08, 0x70, 0x08, 0x07],
            'Z': [0x61, 0x51, 0x49, 0x45, 0x43], '[': [0x00, 0x7F, 0x41, 0x41, 0x00],
            '\\': [0x02, 0x04, 0x08, 0x10, 0x20], ']': [0x00, 0x41, 0x41, 0x7F, 0x00],
            '^': [0x04, 0x02, 0x01, 0x02, 0x04], '_': [0x40, 0x40, 0x40, 0x40, 0x40],
            '`': [0x00, 0x01, 0x02, 0x05, 0x00], 'a': [0x20, 0x54, 0x54, 0x54, 0x78],
            'b': [0x7F, 0x48, 0x44, 0x44, 0x38], 'c': [0x38, 0x44, 0x44, 0x44, 0x20],
            'd': [0x38, 0x44, 0x44, 0x48, 0x7F], 'e': [0x38, 0x54, 0x54, 0x54, 0x18],
            'f': [0x08, 0x7E, 0x09, 0x01, 0x02], 'g': [0x0C, 0x52, 0x52, 0x52, 0x3E],
            'h': [0x7F, 0x08, 0x04, 0x04, 0x78], 'i': [0x00, 0x44, 0x7D, 0x40, 0x00],
            'j': [0x20, 0x40, 0x44, 0x3D, 0x00], 'k': [0x7F, 0x10, 0x28, 0x44, 0x00],
            'l': [0x00, 0x41, 0x7F, 0x40, 0x00], 'm': [0x7C, 0x04, 0x18, 0x04, 0x78],
            'n': [0x7C, 0x08, 0x04, 0x04, 0x78], 'o': [0x38, 0x44, 0x44, 0x44, 0x38],
            'p': [0x7C, 0x14, 0x14, 0x14, 0x08], 'q': [0x08, 0x14, 0x14, 0x18, 0x7C],
            'r': [0x7C, 0x08, 0x04, 0x04, 0x08], 's': [0x48, 0x54, 0x54, 0x54, 0x20],
            't': [0x04, 0x3F, 0x44, 0x40, 0x20], 'u': [0x3C, 0x40, 0x40, 0x20, 0x7C],
            'v': [0x1C, 0x20, 0x40, 0x20, 0x1C], 'w': [0x3C, 0x40, 0x30, 0x40, 0x3C],
            'x': [0x44, 0x28, 0x10, 0x28, 0x44], 'y': [0x0C, 0x50, 0x50, 0x50, 0x3C],
            'z': [0x44, 0x64, 0x54, 0x4C, 0x44], '{': [0x00, 0x08, 0x36, 0x41, 0x00],
            '|': [0x00, 0x00, 0x7F, 0x00, 0x00], '}': [0x00, 0x41, 0x36, 0x08, 0x00],
            '~': [0x08, 0x04, 0x08, 0x10, 0x08]
        }

        for p in self.DATA_PINS + [self.LCD_RD, self.LCD_WR, self.LCD_CD, self.LCD_CS, self.LCD_RST]:
            self.pi.set_mode(p, pigpio.OUTPUT)
        self.pi.write(self.LCD_RST, 0); time.sleep(0.1); self.pi.write(self.LCD_RST, 1); time.sleep(0.1)
        self.pi.write(self.LCD_CS, 0); self.pi.write(self.LCD_RD, 1)
        self.pi.write(self.LCD_CD, 0)
        self.__write8_init(0x01); time.sleep(0.1)
        self.__write8_init(0x11); time.sleep(0.1)
        self.__write8_init(0x36); self.pi.write(self.LCD_CD, 1); self.__write8_init(0x88)
        self.pi.write(self.LCD_CD, 0); self.__write8_init(0x3A); self.pi.write(self.LCD_CD, 1); self.__write8_init(0x55)
        self.pi.write(self.LCD_CD, 0); self.__write8_init(0x29); time.sleep(0.1)
    
    def rgb(self, r, g, b):
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

    def __get_bit_masks(self, val):
        s_mask, c_mask = 0, 0
        for i in range(8):
            if (val >> i) & 1: s_mask |= (1 << self.DATA_PINS[i])
            else: c_mask |= (1 << self.DATA_PINS[i])
        return s_mask, c_mask

    def __write8_init(self, val):
        s, c = self.__get_bit_masks(val)
        self.pi.clear_bank_1(c | self.WR_MASK); self.pi.set_bank_1(s); self.pi.set_bank_1(self.WR_MASK)

    def __set_window(self, x1, y1, x2, y2):
        self.pi.write(self.LCD_CD, 0); self.__write8_init(0x2A); self.pi.write(self.LCD_CD, 1)
        self.__write8_init(x1 >> 8); self.__write8_init(x1 & 0xFF)
        self.__write8_init(x2 >> 8); self.__write8_init(x2 & 0xFF)
        self.pi.write(self.LCD_CD, 0); self.__write8_init(0x2B); self.pi.write(self.LCD_CD, 1)
        self.__write8_init(y1 >> 8); self.__write8_init(y1 & 0xFF)
        self.__write8_init(y2 >> 8); self.__write8_init(y2 & 0xFF)
        self.pi.write(self.LCD_CD, 0); self.__write8_init(0x2C); self.pi.write(self.LCD_CD, 1)

    def __create_pixel_wave(self, color_565):
        hi, lo = color_565 >> 8, color_565 & 0xFF
        hi_s, hi_c = self.__get_bit_masks(hi); lo_s, lo_c = self.__get_bit_masks(lo)

        wf = [
            pigpio.pulse(hi_s, hi_c | self.WR_MASK, 1), pigpio.pulse(self.WR_MASK, 0, 1),
            pigpio.pulse(lo_s, lo_c | self.WR_MASK, 1), pigpio.pulse(self.WR_MASK, 0, 1)
        ]
        self.pi.wave_add_generic(wf)
        return self.pi.wave_create()

    def fillRect(self, x, y, w, h, color):
        self.__set_window(x, y, x + w - 1, y + h - 1)
        wave_id = self.__create_pixel_wave(color)
        total_pixels = w * h
        
        pixels_per_loop = min(total_pixels, 60000)
        loops = total_pixels // pixels_per_loop
        remainder = total_pixels % pixels_per_loop

        def send_chain(count):
            if count <= 0: return
            l, h = count & 0xFF, (count >> 8) & 0xFF
            self.pi.wave_chain([255, 0, wave_id, 255, 1, l, h])
            while self.pi.wave_tx_busy(): pass

        for _ in range(loops): send_chain(pixels_per_loop)
        send_chain(remainder)
        self.pi.wave_delete(wave_id)

    def fillScreen(self, color):
        self.fillRect(0, 0, 240, 320, color)

    def drawPixel(self, x, y, color):
        self.__set_window(x, y, x, y)
        s1, c1 = self.__get_bit_masks(color >> 8)
        s2, c2 = self.__get_bit_masks(color & 0xFF)
        self.pi.clear_bank_1(c1 | self.WR_MASK); self.pi.set_bank_1(s1); self.pi.set_bank_1(self.WR_MASK)
        self.pi.clear_bank_1(c2 | self.WR_MASK); self.pi.set_bank_1(s2); self.pi.set_bank_1(self.WR_MASK)

    def __draw_char(self, x, y, char, color, bg=None, size=1):
        if char not in self.FONT: return
        data = self.FONT[char]
        for i in range(5):
            line = data[i]
            for j in range(8):
                if line & (1 << j):
                    self.__set_window(x+(i*size), y+(j*size), x+(i*size)+size-1, y+(j*size)+size-1)
                    for _ in range(size*size): self.__write8_init(color >> 8); self.__write8_init(color & 0xFF)
                elif bg is not None:
                    self.__set_window(x+(i*size), y+(j*size), x+(i*size)+size-1, y+(j*size)+size-1)
                    for _ in range(size*size): self.__write8_init(bg >> 8); self.__write8_init(bg & 0xFF)

    def draw_strings(self, x, y, string, color, bg=None, size=1):
        curr_x = x
        for char in string:
            self.__draw_char(curr_x, y, char, color, bg, size)
            curr_x += (6 * size)
    
    def display_image(self, path):
        if not os.path.exists(path):
            print("File does not exist.")
            return

        mask_cache = []
        for i in range(256):
            mask_cache.append(self.__get_bit_masks(i))

        try:
            img = Image.open(path).convert("RGB")
            img = img.resize((240, 320), Image.Resampling.LANCZOS)
            pixels = img.load()
            
            self.__set_window(0, 0, 239, 319)

            start_time = time.time()

            for y in range(320):
                pulses = []
                for x in range(240):

                    r, g, b = pixels[x, y]
                    color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
                    hi, lo = color >> 8, color & 0xFF
                    
                    hi_s, hi_c = mask_cache[hi]
                    lo_s, lo_c = mask_cache[lo]

                    pulses.append(pigpio.pulse(hi_s, hi_c | self.WR_MASK, 1))
                    pulses.append(pigpio.pulse(self.WR_MASK, 0, 1))
                    pulses.append(pigpio.pulse(lo_s, lo_c | self.WR_MASK, 1))
                    pulses.append(pigpio.pulse(self.WR_MASK, 0, 1))

                self.pi.wave_add_generic(pulses)
                row_wave = self.pi.wave_create()
                self.pi.wave_send_once(row_wave)
                
                while self.pi.wave_tx_busy():
                    pass

                self.pi.wave_delete(row_wave)

        except Exception as e:
            print(f"FAILED: {e}")
    