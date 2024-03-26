from datetime import datetime # For timestamping
import time, os # For time and file management


logging_duration = 8 # Duration of data logging in seconds
logging_interval = 5 # Data logging interval in seconds
pressure_logging_interval = 5 #60 * 15 # Pressure sensor data logging interval: 60 * n, where n is minutes

#CAMERA SETUP
height = 2 * 2600 # Height of the image in pixels
width = 1 * 2600 # Width of the image in pixels
lens_position = 9.15 # Lens position for manual focus
file_type = ".jpg" # File type for saved images

#Flash Setup
brightness = 1 # Brightness level for the flash, from 0 to 1 where 1 is the maximum brightness

#File Save Setup
dir_name = "/home/group14/Documents/" + datetime.now().strftime("%d-%m-%Y") + " Test_Data/" # Directory for saving data

#Try to create directory for saving data if it doesn't already exist
try:
    os.mkdir(dir_name)
except:
    pass # If directory already exists, do nothing