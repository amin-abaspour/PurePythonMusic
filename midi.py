
NOTE_OFFSETS = {
    'C': 0, 'C#': 1, 'Db': 1,
    'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Gb': 6,
    'G': 7, 'G#': 8, 'Ab': 8,
    'A': 9, 'A#': 10, 'Bb': 10,
    'B': 11
}

def note_to_midi(note):
    """Convert a note name to its MIDI number."""
    if len(note) == 2:
        name, octave = note[0], int(note[1])
        accidental = ''
    elif len(note) == 3:
        name, accidental, octave = note[0], note[1], int(note[2])
        name += accidental
    else:
        raise ValueError("Invalid note format")
    
    semitone_offset = NOTE_OFFSETS.get(name)
    if semitone_offset is None:
        raise ValueError(f"Unknown note name: {name}")
    
    midi_number = (octave * 12) + semitone_offset
    return midi_number

def midi_to_note(midi_number):
    """Convert a MIDI number back to a note name."""
    octave = midi_number // 12
    semitone = midi_number % 12
    for note, offset in NOTE_OFFSETS.items():
        if offset == semitone and len(note) == 1:  # Prefer natural notes
            return f"{note}{octave}"
    # Fallback if no natural note found
    for note, offset in NOTE_OFFSETS.items():
        if offset == semitone:
            return f"{note}{octave}"
    raise ValueError("Invalid MIDI number")

def note_to_frequency(note):
    """Convert a note name to its corresponding frequency."""
    midi_number = note_to_midi(note)
    frequency = 440.0 * (2 ** ((midi_number - 69) / 12))
    return frequency

