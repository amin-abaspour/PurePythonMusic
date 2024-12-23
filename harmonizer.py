from notes import NOTES
from midi import note_to_midi, midi_to_note
from waves import sine_wave
from wav import write_wav, chords_to_wave

def transpose_note(note, semitones):
    """Transpose a note by a given number of semitones."""
    midi_num = note_to_midi(note)
    return midi_to_note(midi_num + semitones)

def create_parallel_harmony(melody, interval):
    """Create a parallel harmony at a specified interval above the melody."""
    harmony = []
    for note, duration in melody:
        if note == "REST":
            harmony.append(("REST", duration))
        else:
            harmony_note = transpose_note(note, interval)
            harmony.append((harmony_note, duration))
    return harmony

def create_counterpoint(melody):
    """Create a simple counterpoint harmony."""
    harmony = []
    prev_interval = 0
    
    for i, (note, duration) in enumerate(melody):
        if note == "REST":
            harmony.append(("REST", duration))
            continue
            
        melody_midi = note_to_midi(note)
        
        # Choose harmony intervals based on melodic motion
        if i == 0:
            interval = -3  # Start with third below
        else:
            # Prefer contrary motion
            if melody_midi > note_to_midi(melody[i-1][0]):
                interval = -3 if prev_interval > -5 else -5
            else:
                interval = -5 if prev_interval > -5 else -3
        
        harmony_note = transpose_note(note, interval)
        harmony.append((harmony_note, duration))
        prev_interval = interval
    
    return harmony

def combine_melody_and_harmony(melody, harmony):
    """Combine melody and harmony into a sequence of chords."""
    return [[(m[0], m[1]), (h[0], h[1])] for m, h in zip(melody, harmony)]

def generate_harmony(melody, harmony_type='thirds', sample_rate=44100):
    """Generate harmonized version of a melody.
    
    harmony_type options:
    - 'thirds': Parallel harmony a third above
    - 'sixths': Parallel harmony a sixth above
    - 'counterpoint': Simple counterpoint harmony
    """
    if harmony_type == 'thirds':
        harmony = create_parallel_harmony(melody, 4)  # Major third = 4 semitones
    elif harmony_type == 'sixths':
        harmony = create_parallel_harmony(melody, 9)  # Major sixth = 9 semitones
    elif harmony_type == 'counterpoint':
        harmony = create_counterpoint(melody)
    else:
        raise ValueError("Unsupported harmony type")
        
    combined = combine_melody_and_harmony(melody, harmony)
    return chords_to_wave(combined, sample_rate, wave_type=sine_wave,
                         use_adsr=True, attack=0.05, decay=0.05,
                         sustain_level=0.7, release=0.05)

# Example usage
if __name__ == "__main__":
    # Simple melody for testing
    test_melody = [
        ("C4", 0.5), ("E4", 0.5), ("G4", 0.5), ("C5", 0.5),
        ("C5", 0.5), ("G4", 0.5), ("E4", 0.5), ("C4", 0.5)
    ]
    
    # Generate different harmony types
    thirds_harmony = generate_harmony(test_melody, 'thirds')
    write_wav("./output/harmony_thirds.wav", thirds_harmony, 44100)
    
    sixths_harmony = generate_harmony(test_melody, 'sixths')
    write_wav("./output/harmony_sixths.wav", sixths_harmony, 44100)
    
    counterpoint_harmony = generate_harmony(test_melody, 'counterpoint')
    write_wav("./output/harmony_counterpoint.wav", counterpoint_harmony, 44100)
    
    # Example with an existing melody from songs.py
    from songs import twinkle_twinkle
    
    twinkle_harmony = generate_harmony(twinkle_twinkle, 'thirds')
    write_wav("./output/twinkle_twinkle_harmony.wav", twinkle_harmony, 44100)
