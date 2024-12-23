from notes import NOTES

# Common rhythm patterns (in beats)
RHYTHM_PATTERNS = {
    'basic': [1.0, 1.0, 1.0, 1.0],
    'waltz': [1.0, 0.5, 0.5],
    'swing': [0.66, 0.33, 0.66, 0.33],
    'samba': [0.5, 0.25, 0.25, 0.5, 0.25, 0.25],
    'rock': [1.0, 0.5, 0.5, 1.0],
    'jazz': [0.75, 0.25, 0.5, 0.5],
    'funk': [0.25, 0.25, 0.5, 0.25, 0.75],
}

def apply_rhythm_pattern(melody, pattern, tempo=1.0):
    """Apply a rhythm pattern to a melody by adjusting note durations."""
    if isinstance(pattern, str):
        pattern = RHYTHM_PATTERNS.get(pattern, RHYTHM_PATTERNS['basic'])
    
    new_melody = []
    pattern_length = len(pattern)
    pattern_index = 0
    
    for note, _ in melody:  # Original duration ignored
        new_duration = pattern[pattern_index] * tempo
        new_melody.append((note, new_duration))
        pattern_index = (pattern_index + 1) % pattern_length
        
    return new_melody

def create_syncopated_rhythm(melody, syncopation_level=0.5):
    """Create syncopated version of a melody by shifting some beats."""
    new_melody = []
    for i, (note, duration) in enumerate(melody):
        if i % 2 == 1 and duration >= 0.5:  # Every other note
            # Split note into two parts with shifted timing
            new_melody.append((note, duration * syncopation_level))
            new_melody.append(("REST", duration * (1 - syncopation_level)))
        else:
            new_melody.append((note, duration))
    return new_melody

def create_polyrhythm(melody1, melody2, ratio=(3,2)):
    """Create a polyrhythm by combining two melodies with different rhythmic divisions."""
    base_duration = 1.0
    duration1 = base_duration / ratio[0]
    duration2 = base_duration / ratio[1]
    
    rhythm1 = [(note, duration1) for note, _ in melody1]
    rhythm2 = [(note, duration2) for note, _ in melody2]
    
    # Combine both rhythms
    combined = []
    t1 = t2 = 0
    while t1 < len(rhythm1) or t2 < len(rhythm2):
        if t1 < len(rhythm1):
            combined.append(rhythm1[t1])
        if t2 < len(rhythm2):
            combined.append(rhythm2[t2])
        t1 += 1
        t2 += 1
    
    return combined

# Example usage
if __name__ == "__main__":
    from wav import write_wav, melody_with_adsr
    from songs import twinkle_twinkle, ode_to_joy
    from waves import sine_wave, triangle_wave
    
    # Apply different rhythm patterns to Twinkle Twinkle
    basic_rhythm = apply_rhythm_pattern(twinkle_twinkle, 'basic')
    write_wav("./output/twinkle_basic_rhythm.wav", 
              melody_with_adsr(basic_rhythm, 44100), 44100)
    
    swing_rhythm = apply_rhythm_pattern(twinkle_twinkle, 'swing')
    write_wav("./output/twinkle_swing_rhythm.wav",
              melody_with_adsr(swing_rhythm, 44100), 44100)
    
    samba_rhythm = apply_rhythm_pattern(twinkle_twinkle, 'samba')
    write_wav("./output/twinkle_samba_rhythm.wav",
              melody_with_adsr(samba_rhythm, 44100), 44100)
    
    # Create syncopated version of Ode to Joy
    syncopated = create_syncopated_rhythm(ode_to_joy)
    write_wav("./output/ode_to_joy_syncopated.wav",
              melody_with_adsr(syncopated, 44100), 44100)
    
    # Create polyrhythm using two melodies
    simple_melody1 = [("C4", 0.5), ("E4", 0.5), ("G4", 0.5)]
    simple_melody2 = [("D4", 0.5), ("F4", 0.5)]
    
    polyrhythm = create_polyrhythm(simple_melody1, simple_melody2, (3,2))
    write_wav("./output/polyrhythm_3_2.wav",
              melody_with_adsr(polyrhythm, 44100, wave_type=triangle_wave), 44100)
