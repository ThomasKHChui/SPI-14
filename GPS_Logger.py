import serial, pynmea2 # Import necessary Python modules for GPS sensor
import time, csv, setup # Import other necessary Python modules for time, CSV and setup configuration parameters
from datetime import datetime # For timestamping

# Set serial port and baud rate based on the GPS module specs.
port = '/dev/ttyS0' # Serial port for GPS module
baudrate = 9600 # Baud rate for serial communication

# Start serial polling
ser = serial.Serial(port, baudrate, timeout=1)

# Write to CSV file with headers
csv_headers = ["timestamp", "latitude", "longitude"]
output_file = open(setup.dir_name + datetime.now().strftime("%H:%M:%S") + " GPS Data.csv", "w", newline='')
csv_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
csv_writer.writeheader()

start_time = time.time() # Start time of logging

try:
    while time.time() - start_time < setup.logging_duration:
        data = ser.readline().decode('utf-8') # Read serial data fro GPS sensor
        
        if data.startswith('$'):
            try:
                # Parse the NMEA data using pynmea2
                msg = pynmea2.parse(data)
                
                # Check if the message is of type GGA (Global Position System fix data)
                if isinstance(msg, pynmea2.GGA):
                    # Get the current timestamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # Write timestamp and GPS data to CSV file
                    csv_writer.writerow({"timestamp": timestamp, "latitude": msg.latitude, "longitude": msg.longitude})
                    # Pauses while loop according to the set logging interval
                    time.sleep(setup.logging_interval)
            except pynmea2.ParseError as e:
                print(f"Parse error: {e}")

except KeyboardInterrupt:
    pass

finally:
    # Close the serial port and CSV file
    ser.close()
    output_file.close()
