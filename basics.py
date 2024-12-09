import math
import random

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
    x %= 2 * math.pi  # Reduce to within 0 to 2π
    result = 0
    for n in range(terms):
        coef = (-1) ** n  # Alternate between addition and subtraction
        power = 2 * n + 1
        result += coef * (x ** power) / factorial(power)
    return result

# Clamp function to restrict values within a range
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

# Generate raw audio samples
def generate_samples(frequency, duration, sample_rate, amplitude):
    samples = []
    total_samples = int(sample_rate * duration)
    for n in range(total_samples):
        t = n / sample_rate
        # Generate sine wave sample
        sample = amplitude * sine(2 * math.pi * frequency * t)
        clamped_sample = clamp(int(sample), -32768, 32767)
        samples.append(clamped_sample)  # Quantize to integer
    return samples

# Write WAV file manually
def write_wav(filename, samples, sample_rate):
    num_channels = 1  # Mono
    bytes_per_sample = 2  # 16-bit
    num_samples = len(samples)
    byte_rate = sample_rate * num_channels * bytes_per_sample
    block_align = num_channels * bytes_per_sample
    max_amplitude = 32767
    min_amplitude = -32768

    with open(filename, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        f.write((36 + num_samples * bytes_per_sample).to_bytes(4, 'little'))
        f.write(b'WAVE')

        # fmt subchunk
        f.write(b'fmt ')
        f.write((16).to_bytes(4, 'little'))  # Subchunk size
        f.write((1).to_bytes(2, 'little'))  # Audio format (1 = PCM)
        f.write((num_channels).to_bytes(2, 'little'))
        f.write((sample_rate).to_bytes(4, 'little'))
        f.write((byte_rate).to_bytes(4, 'little'))
        f.write((block_align).to_bytes(2, 'little'))
        f.write((bytes_per_sample * 8).to_bytes(2, 'little'))  # Bits per sample

        # data subchunk
        f.write(b'data')
        f.write((num_samples * bytes_per_sample).to_bytes(4, 'little'))

        for sample in samples:
            # Clamp the sample to 16-bit range
            clamped_sample = clamp(sample, min_amplitude, max_amplitude)
            f.write(int(clamped_sample).to_bytes(2, 'little', signed=True))

# Generate a 440 Hz tone for 2 seconds
sample_rate = 44100
frequency = 440  # A4
duration = 2  # Seconds
amplitude = 32767  # Max amplitude for 16-bit audio

samples = generate_samples(frequency, duration, sample_rate, amplitude)
write_wav('./output/pure_tone.wav', samples, sample_rate)

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
            if frequency > 0:
                sample = amplitude * sine(2 * math.pi * frequency * t)
                clamped_sample = clamp(int(sample), -32768, 32767)
            else:
                clamped_sample = 0  # REST
            samples.append(clamped_sample)  # Quantize to integer
    return samples

# Example melody: Twinkle, Twinkle, Little Star
melody = [
    ("C4", 0.5), ("C4", 0.5), ("G4", 0.5), ("G4", 0.5),
    ("A4", 0.5), ("A4", 0.5), ("G4", 1.0),
    ("F4", 0.5), ("F4", 0.5), ("E4", 0.5), ("E4", 0.5),
    ("D4", 0.5), ("D4", 0.5), ("C4", 1.0)
]

# Generate and save the melody
samples = generate_melody(melody, sample_rate, amplitude)
write_wav('./output/twinkle_twinkle.wav', samples, sample_rate)

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
samples = generate_melody_with_chords(melody_with_chords, sample_rate, amplitude)
write_wav('./output/melody_with_chords.wav', samples, sample_rate)

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

# Parse the text-based melody
parsed_melody = parse_melody_from_text(text_input)

# Generate and save the melody with features
tempo = 1.2  # Adjust tempo (1.0 = original speed, >1.0 = faster, <1.0 = slower)
base_amplitude = 32767  # Max amplitude for 16-bit audio

samples = generate_melody_with_features(parsed_melody, sample_rate, base_amplitude, tempo)
write_wav('./output/melody_with_features.wav', samples, sample_rate)

# --- New Waveform Functions ---

# Square Wave using Fourier series
def square(x, terms=10):
    x %= 2 * math.pi
    result = 0
    for n in range(terms):
        k = 2 * n + 1
        result += (1 / k) * sine(k * x)
    return (4 / math.pi) * result  # Normalize to approximately [-1.2732, 1.2732]

# Triangle Wave using Fourier series
def triangle(x, terms=10):
    x %= 2 * math.pi
    result = 0
    for n in range(terms):
        k = 2 * n + 1
        coef = ((-1) ** n) / (k ** 2)
        result += coef * sine(k * x)
    return (8 / (math.pi ** 2)) * result  # Normalize to approximately [-0.809, 0.809]

# Sawtooth Wave using Fourier series
def sawtooth(x, terms=10):
    x %= 2 * math.pi
    result = 0
    for k in range(1, terms + 1):
        result += (1 / k) * sine(k * x)
    return (2 / math.pi) * result  # Normalize to approximately [-0.6366, 0.6366]

# Generate Square Wave samples
def generate_square_samples(frequency, duration, sample_rate, amplitude, terms=10):
    samples = []
    total_samples = int(sample_rate * duration)
    for n in range(total_samples):
        t = n / sample_rate
        sample = amplitude * square(2 * math.pi * frequency * t, terms)
        clamped_sample = clamp(int(sample), -32768, 32767)
        samples.append(clamped_sample)
    return samples

# Generate Triangle Wave samples
def generate_triangle_samples(frequency, duration, sample_rate, amplitude, terms=10):
    samples = []
    total_samples = int(sample_rate * duration)
    for n in range(total_samples):
        t = n / sample_rate
        sample = amplitude * triangle(2 * math.pi * frequency * t, terms)
        clamped_sample = clamp(int(sample), -32768, 32767)
        samples.append(clamped_sample)
    return samples

# Generate Sawtooth Wave samples
def generate_sawtooth_samples(frequency, duration, sample_rate, amplitude, terms=10):
    samples = []
    total_samples = int(sample_rate * duration)
    for n in range(total_samples):
        t = n / sample_rate
        sample = amplitude * sawtooth(2 * math.pi * frequency * t, terms)
        clamped_sample = clamp(int(sample), -32768, 32767)
        samples.append(clamped_sample)
    return samples

# --- Example Usages ---

# Generate and save a 440 Hz square wave for 2 seconds
square_samples = generate_square_samples(frequency=440, duration=2, sample_rate=44100, amplitude=32767, terms=10)
write_wav('./output/square_tone.wav', square_samples, 44100)

# Generate and save a 440 Hz triangle wave for 2 seconds
triangle_samples = generate_triangle_samples(frequency=440, duration=2, sample_rate=44100, amplitude=32767, terms=10)
write_wav('./output/triangle_tone.wav', triangle_samples, 44100)

# Generate and save a 440 Hz sawtooth wave for 2 seconds
sawtooth_samples = generate_sawtooth_samples(frequency=440, duration=2, sample_rate=44100, amplitude=32767, terms=10)
write_wav('./output/sawtooth_tone.wav', sawtooth_samples, 44100)

# --- ADSR Envelope Functions ---

def apply_adsr(samples, sample_rate, attack_time, decay_time, sustain_level, release_time):
    """
    Applies an ADSR envelope to the given samples.
    
    Parameters:
        samples (list[int]): The samples to modify.
        sample_rate (int): Sample rate in Hz.
        attack_time (float): Attack time in seconds.
        decay_time (float): Decay time in seconds.
        sustain_level (float): Sustain amplitude level (0.0 to 1.0).
        release_time (float): Release time in seconds.
        
    Returns:
        list[int]: The samples with ADSR envelope applied.
    """
    
    total_samples = len(samples)
    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    release_samples = int(release_time * sample_rate)
    
    # The main portion (sustain phase) starts after attack+decay and goes until we hit the release at the end.
    sustain_start = attack_samples + decay_samples
    sustain_end = total_samples - release_samples
    
    # Prevent invalid segments if durations are too large or short.
    if sustain_end < sustain_start:
        sustain_end = sustain_start
    
    # Apply ADSR
    modified_samples = []
    
    for i, sample in enumerate(samples):
        if i < attack_samples:
            # Attack phase: ramp from 0.0 to 1.0
            env = (i / attack_samples) if attack_samples > 0 else 1.0
        elif i < sustain_start:
            # Decay phase: ramp down from 1.0 to sustain_level
            decay_pos = i - attack_samples
            env = 1.0 - (1.0 - sustain_level) * (decay_pos / decay_samples if decay_samples > 0 else 1.0)
        elif i < sustain_end:
            # Sustain phase: hold at sustain_level
            env = sustain_level
        else:
            # Release phase: ramp down from sustain_level to 0.0
            release_pos = i - sustain_end
            env = sustain_level * (1.0 - (release_pos / release_samples if release_samples > 0 else 1.0))
        
        # Apply the envelope to the sample and clamp
        new_sample = int(sample * env)
        clamped_sample = clamp(new_sample, -32768, 32767)
        modified_samples.append(clamped_sample)
    
    return modified_samples

# --- Example Usage of ADSR Envelope ---

# Let's generate a 440 Hz sine wave for 2 seconds, then apply an ADSR envelope:
adsr_sample_rate = 44100
adsr_frequency = 440
adsr_duration = 2.0
adsr_amplitude = 32767

# Generate plain sine samples
adsr_samples = generate_samples(adsr_frequency, adsr_duration, adsr_sample_rate, adsr_amplitude)

# Apply an ADSR envelope: 
# Attack: 0.2s, Decay: 0.2s, Sustain: 0.5 (50%), Release: 0.5s
adsr_samples = apply_adsr(adsr_samples, adsr_sample_rate, attack_time=0.2, decay_time=0.2, sustain_level=0.5, release_time=0.5)

# Save the resulting sound to a WAV file
write_wav('./output/sine_with_adsr.wav', adsr_samples, adsr_sample_rate)


# --- ADSR Envelope Functions ---

def apply_adsr(samples, sample_rate, attack_time, decay_time, sustain_level, release_time):
    """
    Applies an ADSR envelope to the given samples.
    
    Parameters:
        samples (list[int]): The samples to modify.
        sample_rate (int): Sample rate in Hz.
        attack_time (float): Attack time in seconds.
        decay_time (float): Decay time in seconds.
        sustain_level (float): Sustain amplitude level (0.0 to 1.0).
        release_time (float): Release time in seconds.
        
    Returns:
        list[int]: The samples with ADSR envelope applied.
    """
    
    total_samples = len(samples)
    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    release_samples = int(release_time * sample_rate)
    
    # The main portion (sustain phase) starts after attack+decay and goes until we hit the release at the end.
    sustain_start = attack_samples + decay_samples
    sustain_end = total_samples - release_samples
    
    # Prevent invalid segments if durations are too large or short.
    if sustain_end < sustain_start:
        sustain_end = sustain_start
    
    # Apply ADSR
    modified_samples = []
    
    for i, sample in enumerate(samples):
        if i < attack_samples:
            # Attack phase: ramp from 0.0 to 1.0
            env = (i / attack_samples) if attack_samples > 0 else 1.0
        elif i < sustain_start:
            # Decay phase: ramp down from 1.0 to sustain_level
            decay_pos = i - attack_samples
            env = 1.0 - (1.0 - sustain_level) * (decay_pos / decay_samples if decay_samples > 0 else 1.0)
        elif i < sustain_end:
            # Sustain phase: hold at sustain_level
            env = sustain_level
        else:
            # Release phase: ramp down from sustain_level to 0.0
            release_pos = i - sustain_end
            env = sustain_level * (1.0 - (release_pos / release_samples if release_samples > 0 else 1.0))
        
        # Apply the envelope to the sample and clamp
        new_sample = int(sample * env)
        clamped_sample = clamp(new_sample, -32768, 32767)
        modified_samples.append(clamped_sample)
    
    return modified_samples

# --- Example Usage of ADSR Envelope ---

# Let's generate a 440 Hz sine wave for 2 seconds, then apply an ADSR envelope:
adsr_sample_rate = 44100
adsr_frequency = 440
adsr_duration = 2.0
adsr_amplitude = 32767

# Generate plain sine samples
adsr_samples = generate_samples(adsr_frequency, adsr_duration, adsr_sample_rate, adsr_amplitude)

# Apply an ADSR envelope: 
# Attack: 0.2s, Decay: 0.2s, Sustain: 0.5 (50%), Release: 0.5s
adsr_samples = apply_adsr(adsr_samples, adsr_sample_rate, attack_time=0.2, decay_time=0.2, sustain_level=0.5, release_time=0.5)

# Save the resulting sound to a WAV file
write_wav('./output/sine_with_adsr.wav', adsr_samples, adsr_sample_rate)
