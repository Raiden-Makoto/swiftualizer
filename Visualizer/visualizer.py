import librosa
import sounddevice as sd
import numpy as np
import queue

import threading
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Set up OpenGL Grid
GRID_SIZE = 128
terrain = np.zeros(GRID_SIZE, GRID_SIZE)

def update_terrain(new_terrain):
    


audio_path = '../TrainingSongs/SpeakNow/Back To December (Taylor\'s Version).mp3'
y, sr = librosa.load(audio_path, sr=None)

print(f"Audio waveform shape: {y.shape}")  # Example: (882000,) for a 40s file at 22050 Hz
print(f"Sample rate: {sr}")  # Example: 44100 Hz

audio_queue = queue.Queue()

def callback(outdata, frames, time, status):
    if status: print(status)
    if not audio_queue.empty():
        outdata[:] = audio_queue.get()
    else:
        outdata.fill(0)

chunk_size = 1024
for i in range(0, len(y), chunk_size):
    chunk = y[i:i+chunk_size]
    if len(chunk) < chunk_size:
        chunk = np.pad(chunk, (0, chunk_size - len(chunk)), mode='constant')
    audio_queue.put(chunk.reshape(-1, 1))

