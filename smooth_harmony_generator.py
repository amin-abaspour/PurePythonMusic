from wav import write_wav, chords_to_wave
from waves import sine_wave, square_wave, triangle_wave, sawtooth_wave
from chords import build_chord
from songs import twinkle_twinkle, ode_to_joy

# Define a smooth harmony sequence
smooth_harmony_sequence = [
    {"type": "chord", "root": "C4", "chord_type": "major", "duration": 1.0, "wave_type": sine_wave},
    {"type": "melody", "notes": ["E4", "F4", "G4"], "durations": [0.5, 0.5, 1.0], "wave_type": triangle_wave},
    {"type": "chord", "root": "D4", "chord_type": "minor", "duration": 1.0, "wave_type": sawtooth_wave},
    {"type": "melody", "notes": ["A4", "G4", "F4"], "durations": [0.5, 0.5, 1.0], "wave_type": square_wave},
    {"type": "chord", "root": "G4", "chord_type": "major", "duration": 1.0, "wave_type": sine_wave}
]

# Generate wave samples for the sequence
def generate_smooth_harmony(sequence, sample_rate=44100, attack=0.05, decay=0.05, sustain_level=0.7, release=0.1, cutoff_frequency=5000):
    samples = []
    for segment in sequence:
        if segment["type"] == "chord":
            chord = build_chord(segment["root"], segment["chord_type"], duration=segment["duration"])
            chord_wave = chords_to_wave([chord], sample_rate, wave_type=segment["wave_type"], use_adsr=True,
                                        attack=attack, decay=decay, sustain_level=sustain_level, release=release, cutoff_frequency=cutoff_frequency)
            samples.extend(chord_wave)
        elif segment["type"] == "melody":
            melody = [(note, duration) for note, duration in zip(segment["notes"], segment["durations"])]
            melody_wave = chords_to_wave([[note] for note in melody], sample_rate, wave_type=segment["wave_type"],
                                         use_adsr=True, attack=attack, decay=decay, sustain_level=sustain_level, release=release, cutoff_frequency=cutoff_frequency)
            samples.extend(melody_wave)
    return samples

# Generate the smooth harmony sequence samples
samples = generate_smooth_harmony(smooth_harmony_sequence)

# Write the output to a WAV file
write_wav("./output/smooth_harmony_sequence.wav", samples, 44100)

print("Smooth harmony sequence generated and saved as 'smooth_harmony_sequence.wav'")
