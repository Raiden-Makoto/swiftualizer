import matplotlib
from matplotlib import animation

import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

import numpy as np
import librosa
import librosa.display

from scipy.fftpack import fft
import time

import warnings
warnings.filterwarnings('ignore')

# ------------ Audio Setup ---------------
# Constants
CHUNK = 1024 * 2
AMP_LIMIT = 1.0

# Load audio file
audio_file_path = "../TrainingSongs/Fearless/LoveStory.mp3" # change this later!!
data, RATE = librosa.load(audio_file_path, sr=44100, mono=True)

total_frames = len(data)
frame_idx = 0

# ------------ Plot Setup ---------------
fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 6))
x = np.arange(0, CHUNK, 1)  # Time-domain samples
xf = np.linspace(0, RATE, CHUNK)  # Frequency bins

# Create placeholder lines for waveform and FFT
line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)
line_fft, = ax2.semilogx(xf, np.random.rand(CHUNK), '-', lw=2)

# Format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('amplitude')
ax1.set_ylim(-AMP_LIMIT, AMP_LIMIT)
ax1.set_xlim(0, CHUNK)
plt.setp(ax1, xticks=[0, CHUNK // 2, CHUNK])

# Format FFT axes
ax2.set_xlim(20, RATE / 2)
ax2.set_title('FFT')
ax2.set_xlabel('frequency (Hz)')
ax2.set_ylabel('magnitude')

print("Playing File", audio_file_path)

def on_close(event):
    print("Closing...")
    plt.close() #or quit()

def animate(i):
    global frame_idx

    # Stop when we reach the last chunk
    if frame_idx >= total_frames:
        print("End of audio file reached.")
        amogus.event_source.stop()
        return

    # Handle last partial chunk
    end_idx = min(frame_idx + CHUNK, total_frames)
    data_np = data[frame_idx:end_idx]
    frame_idx = end_idx  # Move index forward

    # Adjust x-axis to match the remaining samples
    line.set_color('black')
    line.set_xdata(np.arange(len(data_np)))
    line.set_ydata(data_np)

    # Compute FFT and update spectrum

    # Normalize the magnitude to [0, 1]
    yf = fft(data_np, n=CHUNK)  # Zero-padding if necessary
    yf_mag = np.abs(yf[:CHUNK])  # Get the magnitude (absolute value)
    yf_mag_normalized = yf_mag / np.max(yf_mag)  #
    
    line_fft.set_color('black')
    line_fft.set_ydata(yf_mag_normalized)

if __name__ == '__main__':
    amogus = animation.FuncAnimation(fig, animate, blit=False, interval=1)
    fig.canvas.mpl_connect('close_event', on_close)
    plt.tight_layout()
    plt.show()

