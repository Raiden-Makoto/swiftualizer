import numpy as np
import librosa # loading audio
from opensimplex import OpenSimplex
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui
from PyQt6.QtWidgets import QApplication
import sys

# This is for streaming the song
import struct
import pygame
import pyaudio

class Terrain(object):
    def __init__(self, audio_file_path: str):
        self.audio_file_path = audio_file_path
        self.audio_data, self.sr = librosa.load(audio_file_path, sr=44100, mono=True)
        self.frame_idx = 0

        self.app = QApplication(sys.argv)
        self.window = gl.GLViewWidget()
        self.window.setWindowTitle('Swiftualizer')
        self.window.setGeometry(0, 110, 1920, 1080)
        self.window.setCameraPosition(distance=30, elevation=12)
        self.window.show()

        self.nsteps = 1.3
        self.offset = 0
        self.ypoints = np.arange(-20, 20 + self.nsteps, self.nsteps)
        self.xpoints = np.arange(-20, 20 + self.nsteps, self.nsteps)
        self.nfaces = len(self.ypoints)

        self.CHUNK = len(self.xpoints) * len(self.ypoints)
        self.noise = OpenSimplex(seed=324) # Perlin Noise object
        verts, faces, colors = self.mesh() # create mesh

        self.main_mesh = gl.GLMeshItem(
            facces=faces,
            vertexes=verts,
            faceColor=colors,
            drawEdges=True,
            smooth=False,
        )
        self.main_mesh.setGLOptions('additive')
        self.window.addItem(self.main_mesh)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_mesh)

    def get_audio_chunk(self):
        start = self.frame_idx
        end = min(start + self.CHUNK, len(self.audio_data)) # don't go out of bounds
        chungus = self.audio_data[start:end] # extract the chungus

        if len(chungus) < self.CHUNK:
            chungus = np.pad(chungus, (0, self.CHUNK - len(chungus)))

        self.frame_idx += self.CHUNK
        return  chungus * 9.39  # Scale waveform height
    
    def mesh(self, offset: float=0.0, wf_data=None):
        if wf_data is None: wf_data = np.ones((len(self.xpoints), len(self.ypoints)))  # Default flat terrain
        else: wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))

        faces, colors = [], []
        vertices = np.array([
            [x, y, wf_data[xid][yid] * self.noise.noise2(x=xid / 5 + offset, y=yid / 5 + offset)] \
            for xid, x in enumerate(self.xpoints) for yid, y in enumerate(self.ypoints)
        ], dtype=np.float32)

        for yid in range(self.nfaces - 1):
            yoff = yid * self.nfaces
            for xid in range(self.nfaces - 1):
                faces.append([
                    xid + yoff,
                    xid + yoff + self.nfaces,
                    xid + yoff + self.nfaces + 1,
                ])
                faces.append([
                    xid + yoff,
                    xid + yoff + 1,
                    xid + yoff + self.nfaces + 1,
                ])
                colors.append([xid / self.nfaces, 1 - xid / self.nfaces, yid / self.nfaces, 0.7])
                colors.append([xid / self.nfaces, 1 - xid / self.nfaces, yid / self.nfaces, 0.8])

        faces = np.array(faces, dtype=np.uint32)
        colors = np.array(colors, dtype=np.float32)

        return vertices, faces, colors

    def update_mesh(self):
        if self.frame_idx >= len(self.audio_data):
            print("Audio finished. Stopping animation.")
            self.timer.stop()  # Stop the animation
            QtCore.QTimer.singleShot(1000, self.window.close)  # Close the window after 1 sec
            return
        
        wf_data = self.get_audio_chunk()
        verts, faces, colors = self.mesh(offset=self.offset, wf_data=wf_data)
        self.main_mesh.setMeshData(vertexes=verts, faces=faces, faceColors=colors)
        self.offset -= 0.05

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QApplication.instance().exec() # PyQT API changed (exec_ became exec)

    def animate(self, frametime=None):
        if frametime is None:
            # Calculate the frame time based on audio length
            audio_duration = librosa.get_duration(y=self.audio_data, sr=self.sr)
            num_frames = 1600  # Change as needed
            frame_time = audio_duration / num_frames
            frametime = frame_time * 1000  # Convert to ms

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update_mesh)
        timer.start(round(frametime)) # no floats allowed, unfrtunately
        self.start()

if __name__ == '__main__':
    audio_file_path = "../TrainingSongs/Fearless/LoveStory.mp3" # change this later!!
    terrain = Terrain(audio_file_path)
    terrain.animate()