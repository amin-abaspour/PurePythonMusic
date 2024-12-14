
from mathematics import clamp
from waves import sine_wave
from notes import NOTES

def write_wav(filename, samples, sample_rate):
    with open(filename, 'wb') as f:
        f.write(b'RIFF')
        f.write((36 + len(samples) * 2).to_bytes(4, 'little'))
        f.write(b'WAVEfmt ') 
        f.write((16).to_bytes(4, 'little'))
        f.write((1).to_bytes(2, 'little'))
        f.write((1).to_bytes(2, 'little'))
        f.write(sample_rate.to_bytes(4, 'little'))
        f.write((sample_rate * 2).to_bytes(4, 'little'))
        f.write((2).to_bytes(2, 'little'))
        f.write((16).to_bytes(2, 'little'))
        f.write(b'data')
        f.write((len(samples) * 2).to_bytes(4, 'little'))
        for sample in samples:
            clamped = max(-1.0, min(1.0, sample))
            f.write(int(clamped * 32767).to_bytes(2, 'little', signed=True))

def note_to_wave(note, duration, sample_rate, wave_type=sine_wave):
    frequency = NOTES[note]
    return wave_type(frequency, sample_rate, duration)

def melody_to_wave(melody, sample_rate, wave_type=sine_wave):
    samples = []
    for note, duration in melody:
        samples.extend(note_to_wave(note, duration, sample_rate, wave_type))
    return samples

def apply_adsr(samples, sample_rate, attack=0.1, decay=0.1, sustain_level=0.7, release=0.2):
    total_samples = len(samples)
    attack_samples = int(attack * sample_rate)
    decay_samples = int(decay * sample_rate)
    release_samples = int(release * sample_rate)
    sustain_samples = total_samples - (attack_samples + decay_samples + release_samples)

    envelope = []

    # Attack phase
    for i in range(attack_samples):
        envelope.append(i / attack_samples)

    # Decay phase
    for i in range(decay_samples):
        envelope.append(1 - (1 - sustain_level) * (i / decay_samples))

    # Sustain phase
    envelope.extend([sustain_level] * sustain_samples)

    # Release phase
    for i in range(release_samples):
        envelope.append(sustain_level * (1 - i / release_samples))

    # Apply envelope
    return [sample * env for sample, env in zip(samples, envelope)]

def melody_with_adsr(melody, sample_rate, wave_type=sine_wave, attack=0.1, decay=0.1, sustain_level=0.7, release=0.2):
    samples = []
    for note, duration in melody:
        raw_wave = note_to_wave(note, duration, sample_rate, wave_type)
        shaped_wave = apply_adsr(raw_wave, sample_rate, attack, decay, sustain_level, release)
        samples.extend(shaped_wave)
    return samples

def polyphony_to_wave(chords, sample_rate, wave_type=sine_wave, use_adsr=True, attack=0.1, decay=0.1, sustain_level=0.7, release=0.2):
    """Generate waveforms for polyphonic (chord) playback with ADSR and amplitude normalization."""
    max_length = max(int(note[1] * sample_rate) for chord in chords for note in chord)
    combined_wave = [0.0] * max_length

    for chord in chords:
        chord_wave = [0.0] * max_length
        for note, duration in chord:
            note_wave = note_to_wave(note, duration, sample_rate, wave_type)
            if use_adsr:
                note_wave = apply_adsr(note_wave, sample_rate, attack, decay, sustain_level, release)
            for i, sample in enumerate(note_wave):
                chord_wave[i] += sample / len(chord)  # Normalize per chord
        combined_wave = [a + b for a, b in zip(combined_wave, chord_wave)]

    # Normalize entire waveform to prevent clipping
    max_amplitude = max(abs(sample) for sample in combined_wave)
    if max_amplitude > 1.0:
        combined_wave = [sample / max_amplitude for sample in combined_wave]
    return combined_wave


def chords_to_wave(chords, sample_rate, wave_type=sine_wave, use_adsr=True, attack=0.05, decay=0.05, sustain_level=0.7, release=0.05):
    """
    Generate waveforms for a sequence of chords with polyphony and ADSR envelope.

    Parameters:
        chords (list): List of chords, where each chord is a list of (note, duration) tuples.
        sample_rate (int): Samples per second.
        wave_type (function): Function to generate waveforms for individual notes.
        use_adsr (bool): Whether to apply ADSR envelope to notes.
        attack (float): Attack time in seconds.
        decay (float): Decay time in seconds.
        sustain_level (float): Sustain level (0 to 1).
        release (float): Release time in seconds.

    Returns:
        list: Combined waveform samples.
    """
    samples = []

    for chord in chords:
        # Determine the duration of the chord (assuming all notes in the chord have the same duration)
        chord_duration = chord[0][1]
        chord_length = int(chord_duration * sample_rate)
        chord_wave = [0.0] * chord_length

        for note, duration in chord:
            note_wave = note_to_wave(note, duration, sample_rate, wave_type)
            if use_adsr:
                note_wave = apply_adsr(note_wave, sample_rate, attack, decay, sustain_level, release)
            # Mix the note into the chord waveform
            for i in range(min(len(note_wave), chord_length)):
                chord_wave[i] += note_wave[i] / len(chord)  # Normalize by number of notes

        # Normalize chord_wave to prevent clipping within the chord
        max_amplitude = max(abs(sample) for sample in chord_wave)
        if max_amplitude > 1.0:
            chord_wave = [sample / max_amplitude for sample in chord_wave]

        # Append chord_wave to the overall samples
        samples.extend(chord_wave)

    # Final normalization to prevent clipping across the entire waveform
    overall_max = max(abs(sample) for sample in samples)
    if overall_max > 1.0:
        samples = [sample / overall_max for sample in samples]

    return samples
