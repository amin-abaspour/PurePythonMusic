from wav import write_wav, melody_with_adsr
from chords import build_chord
from waves import sine_wave, triangle_wave, square_wave, sawtooth_wave

def generate_arpeggio(chord, pattern, duration, sample_rate, wave_type=sine_wave, attack=0.1, decay=0.1, sustain_level=0.7, release=0.2, cutoff_frequency=5000):
    """Generate an arpeggio from a chord based on a given pattern."""
    arpeggio = []
    chord_notes = [note for note, _ in chord]
    note_duration = duration / len(pattern)
    
    for step in pattern:
        note = chord_notes[step % len(chord_notes)]
        arpeggio.append((note, note_duration))
    
    return melody_with_adsr(arpeggio, sample_rate, wave_type, attack, decay, sustain_level, release, cutoff_frequency)

def apply_arpeggio_to_melody(melody, chord_sequence, pattern, sample_rate, wave_type=sine_wave, attack=0.1, decay=0.1, sustain_level=0.7, release=0.2, cutoff_frequency=5000):
    """Apply arpeggio patterns to a melody based on a sequence of chords."""
    arpeggiated_melody = []
    chord_index = 0
    
    for note, duration in melody:
        if note == "REST":
            arpeggiated_melody.append(("REST", duration))
        else:
            chord = chord_sequence[chord_index % len(chord_sequence)]
            arpeggio = generate_arpeggio(chord, pattern, duration, sample_rate, wave_type, attack, decay, sustain_level, release, cutoff_frequency)
            arpeggiated_melody.extend(arpeggio)
            chord_index += 1
    
    return arpeggiated_melody

# Example usage
if __name__ == "__main__":
    from songs import twinkle_twinkle
    from chords import build_chord
    
    # Define a chord sequence for Twinkle Twinkle
    chord_sequence = [
        build_chord("C4", "major"),
        build_chord("G4", "major"),
        build_chord("A4", "minor"),
        build_chord("F4", "major"),
        build_chord("C4", "major"),
        build_chord("G4", "major"),
        build_chord("C4", "major")
    ]
    
    # Define an arpeggio pattern (up and down)
    arpeggio_pattern = [0, 1, 2, 1]
    
    # Apply arpeggio to Twinkle Twinkle melody
    arpeggiated_melody = apply_arpeggio_to_melody(twinkle_twinkle, chord_sequence, arpeggio_pattern, 44100, wave_type=triangle_wave)
    
    # Write the arpeggiated melody to a WAV file
    write_wav("./output/twinkle_twinkle_arpeggio.wav", arpeggiated_melody, 44100)
    
    print("Arpeggiated melody generated and saved as 'twinkle_twinkle_arpeggio.wav'")
