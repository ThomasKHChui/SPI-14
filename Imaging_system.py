# Import all necessary Python packages for the camera and LED module 
from picamera2 import Picamera2 # Camera module
from PIL import Image # Image processing
import board, neopixel #LED module

# Import other necessary Python packages
from datetime import datetime # For timestamping
import time, os, setup # import configuration parameters from setup.py file

#Camera initialisation
picam2 = Picamera2()
picam2.options["quality"] = 95   #JPEG quality level, where 0 is worst and 95 is best

#Flash initialisation
pixels1 = neopixel.NeoPixel(board.D18, 9, brightness=setup.brightness)

#List of functions

def image_size(height,width):
    """
    Sets the image size in pixels pre-capture
    """
    camera_config = picam2.create_still_configuration(main={"size":(width,height)})
    picam2.configure(camera_config)

def manual_focus(lens_position):
    """
    Sets the focal distance of the lens
    """
    picam2.start()
    picam2.set_controls({"AfMode": 0, "LensPosition": lens_position})
    time.sleep(5)
    
def capture_image(i, file_type):
    """
    Captures an image and transposes the image by 270 degrees
    """
    picam2.capture_file(str(i+1) + file_type)
    original_image = Image.open(str(i+1) + file_type)
    rotate_image = original_image.transpose(Image.Transpose.ROTATE_270)   
    rotate_image.save(setup.dir_name + datetime.now().strftime("%H:%M:%S") + " Image " + str(i+1) + file_type)
    os.remove(str(i+1) + file_type)
      
def flash_countdown():
    """
    Triggers the LED module to flash on and off for 10 seconds
    """
    for i in range(10):
        pixels1.fill((255,255,255))
        time.sleep(0.1)
        pixels1.fill((0, 0, 0))
        time.sleep(0.9)

def flash_on():
    """
    Turns on flash in RGB white
    """
    pixels1.fill((255,255,255))
    
def flash_off():
    """
    Turns off flash
    """
    pixels1.fill((0, 0, 0))

# Defines a variable for the time when the script started running
start_time = time.time()

# Start of imaging system script
i = 0	# Counter for image file
image_size(setup.width,setup.height) # Set image size
manual_focus(setup.lens_position) # Set lens focus
flash_countdown() # Trigger LED flash countdown
# Main loop for capturing images
try:
    while time.time() - start_time < setup.logging_duration:
        
        flash_on() # Turn on flash
        time.sleep(1)
        capture_image(i, setup.file_type) # Capture image
        print("Image " + str(i+1)) # Print image number
        flash_off() # Turn off flash
        time.sleep(setup.logging_interval-2) # Wait for logging interval
        i += 1
except KeyboardInterrupt:
    print("KeyboardInterrupt: Exiting Imaging_system script")
    picam2.close()

finally:
    picam2.close() # Close camera
