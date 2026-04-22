import time

import pigpio
import glob
import serial
class touch():
    def __init__(self):
        self.pi = pigpio.pi()
        self.WIDTH, self.HEIGHT = 240, 320
        self.X_MIN, self.X_MAX = 150, 900
        self.Y_MIN, self.Y_MAX = 150, 900
        self.ser = self.__connect_to_nano()

    def __connect_to_nano(self):
        ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
        if ports:
            try:
                # Set a very short timeout for "real-time" feel
                s = serial.Serial(ports[0], 115200, timeout=0)
                s.reset_input_buffer()
                return s
            except Exception as e:
                print(f"Serial Error: {e}")
        return None

    def read_touch_time(self, ms):
        self.pi.set_mode(8, pigpio.INPUT)
        self.pi.set_mode(7, pigpio.INPUT)
        self.pi.set_mode(17, pigpio.INPUT)
        self.pi.set_mode(27, pigpio.INPUT)
        self.pi.set_mode(16, pigpio.OUTPUT)
        self.pi.write(16, 1)
        if self.ser:
            for x in range(ms):
                if self.ser.in_waiting > 0:
                    data = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
                    lines = data.split('\r\n')
                    if len(lines) > 1:
                        last_line = lines[-2]
                        
                        if "," in last_line:
                            try:
                                rx, ry, rz = map(int, last_line.split(','))
                            
                                x = int((rx - self.X_MIN) * self.WIDTH / (self.X_MAX - self.X_MIN))
                                y = int((ry - self.Y_MIN) * self.HEIGHT / (self.Y_MAX - self.Y_MIN))
                                
                                x = max(0, min(self.WIDTH - 1, x))
                                y = max(0, min(self.HEIGHT - 1, y))

                                print(f"\rX: {x:3d} | Y: {y:3d} | Z: {rz:3d}  ")

                            except ValueError:
                                pass
                time.sleep(0.001)
    
    def read_touch(self):
        if self.ser.in_waiting > 0:
            data = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
            lines = data.split('\r\n')
            if len(lines) > 1:
                last_line = lines[-2]
                
                if "," in last_line:
                    try:
                        rx, ry, rz = map(int, last_line.split(','))
                    
                        x = int((rx - self.X_MIN) * self.WIDTH / (self.X_MAX - self.X_MIN))
                        y = int((ry - self.Y_MIN) * self.HEIGHT / (self.Y_MAX - self.Y_MIN))
                        
                        x = max(0, min(self.WIDTH - 1, x))
                        y = max(0, min(self.HEIGHT - 1, y))

                        return x, y, rz


                    except ValueError:
                        pass
                        
