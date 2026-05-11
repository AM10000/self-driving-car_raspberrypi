import time
from picamera2 import Picamera2
import lcdDraw
import os

l = lcdDraw.lcd()
picam2 = Picamera2()

# 1. Use the VIDEO configuration instead of STILL
# This tells the Pi to keep the frames "ready" in a buffer
config = picam2.create_video_configuration(main={'size': (640, 480)})
picam2.configure(config)
picam2.start()

filename = "fast_capture.jpg"

try:
    while True:
        # print("Capturing...")
        # 2. Capture the current frame from the video stream
        # This is much faster than the 'still' mode
        picam2.capture_file(filename)
        
        # 3. TEST THIS: Try dropping this to 0.1 or 0.05
        time.sleep(0.1) 
        
        print("Displaying...")
        l.display_image(filename)
        time.sleep(0.6)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    picam2.stop()
    print("Camera closed.")
