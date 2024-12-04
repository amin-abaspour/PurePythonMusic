
# Custom factorial function
def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Custom sine function using Taylor series
def sine(x, terms=10):
    x %= 2 * 3.141592653589793  # Reduce to within 0 to 2π
    result = 0
    for n in range(terms):
        coef = (-1) ** n  # Alternate between addition and subtraction
        power = 2 * n + 1
        result += coef * (x ** power) / factorial(power)
    return result

# Generate raw audio samples
def generate_samples(frequency, duration, sample_rate, amplitude):
    samples = []
    total_samples = int(sample_rate * duration)
    for n in range(total_samples):
        t = n / sample_rate
        # Generate sine wave sample
        sample = amplitude * sine(2 * 3.141592653589793 * frequency * t)
        samples.append(int(sample))  # Quantize to integer
    return samples

# Write WAV file manually
def write_wav(filename, samples, sample_rate):
    # WAV file header components
    num_channels = 1  # Mono
    bytes_per_sample = 2  # 16-bit
    num_samples = len(samples)
    byte_rate = sample_rate * num_channels * bytes_per_sample
    block_align = num_channels * bytes_per_sample

    with open(filename, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        f.write((36 + num_samples * bytes_per_sample).to_bytes(4, 'little'))  # File size
        f.write(b'WAVE')

        # Format chunk
        f.write(b'fmt ')
        f.write((16).to_bytes(4, 'little'))  # Subchunk size
        f.write((1).to_bytes(2, 'little'))  # Audio format (1 = PCM)
        f.write((num_channels).to_bytes(2, 'little'))  # Num channels
        f.write((sample_rate).to_bytes(4, 'little'))  # Sample rate
        f.write((byte_rate).to_bytes(4, 'little'))  # Byte rate
        f.write((block_align).to_bytes(2, 'little'))  # Block align
        f.write((bytes_per_sample * 8).to_bytes(2, 'little'))  # Bits per sample

        # Data chunk
        f.write(b'data')
        f.write((num_samples * bytes_per_sample).to_bytes(4, 'little'))  # Data size
        for sample in samples:
            f.write(int(sample).to_bytes(2, 'little', signed=True))  # 16-bit PCM data

# Generate a 440 Hz tone for 2 seconds
sample_rate = 44100
frequency = 440  # A4
duration = 2  # Seconds
amplitude = 32767  # Max amplitude for 16-bit audio

samples = generate_samples(frequency, duration, sample_rate, amplitude)
write_wav('pure_tone.wav', samples, sample_rate)


# Frequency mapping for musical notes (in Hz)
NOTE_FREQUENCIES = {
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
    "G4": 392.00, "A4": 440.00, "B4": 493.88,
    "C5": 523.25, "REST": 0  # REST has 0 frequency
}

# Generate raw audio samples for a melody
def generate_melody(melody, sample_rate, amplitude):
    samples = []
    for note, duration in melody:
        frequency = NOTE_FREQUENCIES.get(note, 0)  # Default to 0 if note not found
        num_samples = int(sample_rate * duration)
        for n in range(num_samples):
            t = n / sample_rate
            sample = amplitude * sine(2 * 3.141592653589793 * frequency * t) if frequency > 0 else 0
            samples.append(int(sample))  # Quantize to integer
    return samples

# Example melody: Twinkle, Twinkle, Little Star
melody = [
    ("C4", 0.5), ("C4", 0.5), ("G4", 0.5), ("G4", 0.5),
    ("A4", 0.5), ("A4", 0.5), ("G4", 1.0),
    ("F4", 0.5), ("F4", 0.5), ("E4", 0.5), ("E4", 0.5),
    ("D4", 0.5), ("D4", 0.5), ("C4", 1.0)
]

# Generate and save the melody
sample_rate = 44100
amplitude = 32767  # Max amplitude for 16-bit audio

samples = generate_melody(melody, sample_rate, amplitude)
write_wav('twinkle_twinkle.wav', samples, sample_rate)


# Generate raw audio samples for chords
def generate_chord(chord, duration, sample_rate, amplitude):
    samples = []
    frequencies = [NOTE_FREQUENCIES.get(note, 0) for note in chord]  # Get frequencies for all notes in the chord
    num_samples = int(sample_rate * duration)
    for n in range(num_samples):
        t = n / sample_rate
        sample = sum(amplitude * sine(2 * 3.141592653589793 * freq * t) for freq in frequencies if freq > 0) / len(chord)
        samples.append(int(sample))  # Quantize to integer
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
samples = generate_melody_with_chords(melody_with_chords, sample_rate, amplitude)
write_wav('melody_with_chords.wav', samples, sample_rate)

# Generate raw audio samples for a melody with chords, rests, and dynamic volume
def generate_melody_with_features(melody, sample_rate, base_amplitude, tempo=1.0):
    samples = []
    for item in melody:
        duration = item[1] / tempo  # Adjust duration by tempo
        if isinstance(item[0], list):  # Chord (list of notes with optional volume scaling)
            notes = [(NOTE_FREQUENCIES.get(note[0], 0), note[1] if len(note) > 1 else 1.0) for note in item[0]]
            chord_samples = generate_chord_with_volume(notes, duration, sample_rate, base_amplitude)
            samples.extend(chord_samples)
        elif item[0] == "REST":  # Rest
            samples.extend([0] * int(sample_rate * duration))
        else:  # Single note with optional volume scaling
            frequency = NOTE_FREQUENCIES.get(item[0], 0)
            volume_scale = item[2] if len(item) > 2 else 1.0
            note_samples = generate_samples(frequency, duration, sample_rate, int(base_amplitude * volume_scale))
            samples.extend(note_samples)
    return samples

# Generate raw audio samples for chords with dynamic volume
def generate_chord_with_volume(chord, duration, sample_rate, amplitude):
    samples = []
    num_samples = int(sample_rate * duration)
    for n in range(num_samples):
        t = n / sample_rate
        sample = sum(
            amplitude * scale * sine(2 * 3.141592653589793 * freq * t) 
            for freq, scale in chord if freq > 0
        ) / len(chord)
        samples.append(int(sample))  # Quantize to integer
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

# Parse the text-based melody
parsed_melody = parse_melody_from_text(text_input)

# Generate and save the melody with features
tempo = 1.2  # Adjust tempo (1.0 = original speed, >1.0 = faster, <1.0 = slower)
samples = generate_melody_with_features(parsed_melody, sample_rate, amplitude, tempo)
write_wav('melody_with_features.wav', samples, sample_rate)
