import socket
import numpy as np
import argparse
import pathlib
import matplotlib.pyplot as plt
import sys
import os
import time
import grovepi
import math
from grove_rgb_lcd import *
import scipy.fft as fft

# Set the server IP address and port number
SERVER_IP = '172.20.10.9'
SERVER_PORT = 12345

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the sampling rate and duration
fs = 100  # Hz
duration = 25  # seconds
n_samples = int(fs * duration)
sensor = 4
blue = 0
white = 1
temp_data = []
hum_data = []
setRGB(0, 255, 0)
grovepi.pinMode(0, "OUTPUT")
sock.sendto(b'image', (SERVER_IP, SERVER_PORT))

# Collect the data for the specified duration
start_time = time.time()
while time.time() - start_time < duration:
    try:
        [temp, hum] = grovepi.dht(sensor, blue)
        if not math.isnan(temp) and not math.isnan(hum):
            temp_data.append(temp)
            hum_data.append(hum)
            print(f"Temp = {temp:.2f} C, Humidity = {hum:.2f}%")
            setText(f"Temp: {temp:.2f} C\nHumidity: {hum:.2f}%")
            # Send the data to the server
            data = f"{temp:.2f},{hum:.2f}"
            sock.sendto(data.encode(), (SERVER_IP, SERVER_PORT))
    except KeyboardInterrupt:
        exit()
    except IOError:
        print("Error")

# Convert the data to numpy arrays
temp_data = np.array(temp_data)
hum_data = np.array(hum_data)

# Apply FFT to the data
temp_fft = fft.fft(temp_data)
hum_fft = fft.fft(hum_data)

# Calculate the frequency bins
freq_bins = fft.fftfreq(n_samples, 1/fs)

# Create a new x array with the same length as the y array
x = np.linspace(0, fs/2, len(hum_data))

# Plot the results
plt.figure(figsize=(10, 4))
plt.subplot(121)
plt.plot(x, np.abs(temp_fft[:n_samples//2]))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('Temperature FFT')

plt.subplot(122)
plt.plot(x, np.abs(hum_fft[:n_samples//2]))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('Humidity FFT')

home_dir = str(pathlib.Path.home())

desktop_dir = os.path.join(home_dir, 'Desktop')
plt.savefig(os.path.join(desktop_dir, 'myplot.png'))

with open(os.path.join(desktop_dir, 'myplot.png'), 'rb') as f:
    data = f.read()
    sock.sendto(data, (SERVER_IP, SERVER_PORT))
plt.show()



