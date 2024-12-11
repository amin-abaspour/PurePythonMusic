
from mathematics import sine, factorial, clamp, PI
from notes import NOTE_FREQUENCIES

# Generate raw audio samples
def generate_samples(frequency, duration, sample_rate, amplitude):
    samples = []
    total_samples = int(sample_rate * duration)
    for n in range(total_samples):
        t = n / sample_rate
        # Generate sine wave sample
        sample = amplitude * sine(2 * PI * frequency * t)
        clamped_sample = clamp(int(sample), -32768, 32767)
        samples.append(clamped_sample)  # Quantize to integer
    return samples

# Generate a 440 Hz tone for 2 seconds
samples = generate_samples(
    440,    # Frequency
    2,      # Duration, Seconds
    44100,  # Sample rate
    32767   # Amplitude, Max amplitude for 16-bit audio
    )
# write_wav('./output/pure_tone.wav', samples, sample_rate)


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


