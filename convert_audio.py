# Simple code to convert from MIDI files to .WAV files

from midi2audio import FluidSynth

midi_file_path = "path_to_your_midi_file.mid"
output_wavefile = "output_wavefile.wav"

# Initialize FluidSynth
synth = FluidSynth()
synth.midi_to_audio = (midi_file_path, output_wavefile)