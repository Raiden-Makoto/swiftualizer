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
audio_file_path = "path_to_your_audio_file.mp3"
data, RATE = librosa.load(audio_file_path, sr=44100, mono=True)

total_frames = len(data)
frame_index = 0

# ------------ Plot Setup ---------------
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
x = np.arange(0, 2 * CHUNK, 2)  # Time-domain samples
xf = np.linspace(0, RATE, CHUNK)  # Frequency bins

# Create placeholder lines for waveform and FFT
line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)
line_fft, = ax2.semilogx(xf, np.random.rand(CHUNK), '-', lw=2)

# Format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('amplitude')
ax1.set_ylim(-AMP_LIMIT, AMP_LIMIT)
ax1.set_xlim(0, 2 * CHUNK)

# Format FFT axes
ax2.set_xlim(20, RATE / 2)

print("Playing File", audio_file_path)

def on_close(event):
    print("Closing...")
    plt.close() #or quit()

def animate(i):
    global frame_index
    if frame_index + CHUNK >= total_frames:
        print("End of audio reached.")
        return

    # Update waveform and FFT
    data_np = data[frame_index:frame_index+CHUNK]
    frame_index += CHUNK
    line.set_ydata(data_np)
    fft_data = fft(data_np)
    line_fft.set_ydata(np.abs(fft_data)[:CHUNK // 2])

if __name__ == '__main__':
    amogus = animation.FuncAnimation(fig, animate, blit=False, interval=1)
    fig.canvas.mpl_connect('close_event', on_close)
    plt.show()

