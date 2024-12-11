

# Generate raw audio samples for chords
def generate_chord(chord, duration, sample_rate, amplitude):
    samples = []
    frequencies = [NOTE_FREQUENCIES.get(note, 0) for note in chord]  # Get frequencies for all notes in the chord
    num_samples = int(sample_rate * duration)
    for n in range(num_samples):
        t = n / sample_rate
        if frequencies:
            # Sum the sine waves of each note in the chord
            sample_sum = sum(sine(2 * math.pi * freq * t) for freq in frequencies if freq > 0)
            sample = amplitude * sample_sum / len(frequencies)  # Normalize
            clamped_sample = clamp(int(sample), -32768, 32767)
        else:
            sample = 0
            clamped_sample = 0
        samples.append(clamped_sample)  # Quantize to integer
    return samples

# Generate raw audio samples for a melody with chords
def generate_melody_with_chords(melody, sample_rate, amplitude):
    samples = []
    for item in melody:
        if isinstance(item[0], list):  # Chord (list of notes)
            chord_samples = generate_chord(item[0], item[1], sample_rate, amplitude)
            samples.extend(chord_samples)
        else:  # Single note
            note_samples = generate_samples(NOTE_FREQUENCIES.get(item[0], 0), item[1], sample_rate, amplitude)
            samples.extend(note_samples)
    return samples

# Example melody with chords
melody_with_chords = [
    (["C4", "E4", "G4"], 1.0),  # C major chord
    ("C4", 0.5), ("D4", 0.5), ("E4", 1.0),  # Single notes
    (["F4", "A4", "C5"], 1.0),  # F major chord
    ("G4", 0.5), ("A4", 0.5), ("B4", 1.0),  # Single notes
    (["C4", "G4"], 1.0),  # Simple two-note chord
    ("REST", 0.5),  # Rest
    ("C4", 0.5)
]

# Generate and save the melody with chords
# samples = generate_melody_with_chords(melody_with_chords, sample_rate, amplitude)
# write_wav('./output/melody_with_chords.wav', samples, sample_rate)

# Generate raw audio samples for a melody with chords, rests, and dynamic volume
def generate_melody_with_features(melody, sample_rate, base_amplitude, tempo=1.0):
    samples = []
    for item in melody:
        if isinstance(item[0], list):  # Chord (list of notes with optional volume scaling)
            chord = [(NOTE_FREQUENCIES.get(note[0], 0), note[1] if len(note) > 1 else 1.0) for note in item[0]]
            chord_samples = generate_chord_with_volume(chord, item[1] / tempo, sample_rate, base_amplitude)
            samples.extend(chord_samples)
        elif item[0] == "REST":  # Rest
            duration = item[1] / tempo
            samples.extend([0] * int(sample_rate * duration))
        else:  # Single note with optional volume scaling
            note = item[0]
            duration = item[1] / tempo
            volume_scale = item[2] if len(item) > 2 else 1.0
            frequency = NOTE_FREQUENCIES.get(note, 0)
            if frequency > 0:
                note_samples = generate_samples(frequency, duration, sample_rate, int(base_amplitude * volume_scale))
                samples.extend(note_samples)
            else:
                samples.extend([0] * int(sample_rate * duration))  # REST
    return samples

# Generate raw audio samples for chords with dynamic volume
def generate_chord_with_volume(chord, duration, sample_rate, amplitude):
    samples = []
    num_samples = int(sample_rate * duration)
    for n in range(num_samples):
        t = n / sample_rate
        active_notes = [scale * sine(2 * math.pi * freq * t) for freq, scale in chord if freq > 0]
        if active_notes:
            sample_sum = sum(active_notes)
            sample = (amplitude * sample_sum) / len(active_notes)
            clamped_sample = clamp(int(sample), -32768, 32767)
        else:
            clamped_sample = 0
        samples.append(clamped_sample)  # Quantize to integer
    return samples

# Support for text-based melody input
def parse_melody_from_text(input_text):
    """
    Parse a text-based melody format:
    Each line is either a single note or a chord:
    - Single note: C4,0.5 (note,duration)
    - Chord: [C4,1.0|E4,1.0|G4,1.0],1.0 (chord,duration)
    - REST: REST,0.5 (rest,duration)
    """
    melody = []
    for line in input_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        if line.startswith("["):  # Chord
            chord_part, duration = line.split("],")
            duration = float(duration)
            chord = [
                (note.split(",")[0], float(note.split(",")[1]) if "," in note else 1.0)
                for note in chord_part.strip("[]").split("|")
            ]
            melody.append((chord, duration))
        elif line.startswith("REST"):  # Rest
            _, duration = line.split(",")
            melody.append(("REST", float(duration)))
        else:  # Single note
            parts = line.split(",")
            note = parts[0]
            duration = float(parts[1])
            volume_scale = float(parts[2]) if len(parts) > 2 else 1.0
            melody.append((note, duration, volume_scale))
    return melody

# Example melody with features
text_input = """
C4,0.5,1.0
REST,0.25
G4,0.5,0.8
[A4,1.0|C5,0.8|E5,1.0],1.0
F4,0.5,0.6
REST,0.5
[C4,0.7|E4,1.0|G4,1.0],2.0
"""

# Predefined Chords
CHORDS = {
    "C Major": ["C4", "E4", "G4"],
    "G Major": ["G4", "B4", "D5"],
    "A Minor": ["A4", "C5", "E5"],
    "F Major": ["F4", "A4", "C5"],
    "C Major (Low)": ["C3", "E3", "G3"]
}

# Example: Twinkle Twinkle with Simplified Chord Notation
melody_with_chords = [
    ("C Major", 1.0),  # Named chord
    ("C4", 0.5), ("D4", 0.5), ("E4", 1.0),  # Single notes
    ("F Major", 1.0),  # Named chord
    ("G4", 0.5), ("A4", 0.5), ("B4", 1.0),  # Single notes
    (["C4", "G4"], 1.0),  # Inline chord
    ("REST", 0.5),  # Rest
    ("C4", 0.5)
]