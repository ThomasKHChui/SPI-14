import ms5837 # Import the necessary module for the BlueRobotics pressure sensor
import time, csv, setup # Import necessary modules for time, CSV file handling, and setup configuration parameters
from datetime import datetime # For timestamping

#Bar02 pressure sensor initialisation
sensor = ms5837.MS5837_02BA()

# Check if pressure sensor initialisation was successful
if not sensor.init():
    print("Sensor could not be initialized")
    exit(1)

# Write to CSV file with headers
csv_headers = ["timestamp", "depth (m)", "pressure (bar)", "temperature (degC)"]
output_file_path = setup.dir_name + datetime.now().strftime("%H:%M:%S") + " Pressure Sensor Data.csv"

with open(output_file_path, "w", newline='') as output_file:
    csv_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
    csv_writer.writeheader() # Write CSV headers

start_time = time.time() # Record the start time of the logging process

try:
    # Main loop for logging pressure sensor data
    while time.time() - start_time < setup.logging_duration:
        with open(output_file_path, "a", newline='') as output_file:
            csv_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
            if sensor.read(): # Read sensor data
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Get current timestamp
                #Write sensor data to CSV file row by row                
                csv_writer.writerow({"timestamp": timestamp, "depth (m)": sensor.depth(), "pressure (bar)": sensor.pressure(ms5837.UNITS_bar), "temperature (degC)": sensor.temperature()})
                output_file.flush()  # Flush buffer to disk
                time.sleep(setup.pressure_logging_interval) # Wait for logging interval
            else:
                print("Pressure sensor read failed!")
                exit(1) # Exit the script if sensor reading fails
except KeyboardInterrupt:
    print("KeyboardInterrupt: Exiting Pressure_Sensor_Logger.py script")
finally:
    pass  # The output file will be closed automatically when exiting the context manager

