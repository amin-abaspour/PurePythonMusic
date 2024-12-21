
from midi import note_to_midi, midi_to_note

# Define chord types with their corresponding semitone intervals
CHORD_TYPES = {
    'major': [0, 4, 7],
    'minor': [0, 3, 7],
    'diminished': [0, 3, 6],
    'augmented': [0, 4, 8],
    'major7': [0, 4, 7, 11],
    'minor7': [0, 3, 7, 10],
    'dominant7': [0, 4, 7, 10],
    'half-diminished7': [0, 3, 6, 10],
    'diminished7': [0, 3, 6, 9],
    'augmented7': [0, 4, 8, 10],
    # Add more chord types as needed
}

def build_chord(root, chord_type='major', duration=0.5):
    """Build a chord based on the root note and chord type."""
    if chord_type not in CHORD_TYPES:
        raise ValueError(f"Unsupported chord type: {chord_type}")
    
    intervals = CHORD_TYPES[chord_type]
    root_midi = note_to_midi(root)
    chord = []
    for interval in intervals:
        midi_note = root_midi + interval
        note_name = midi_to_note(midi_note)
        chord.append((note_name, duration))  # Assuming a default duration of 0.5 seconds
    return chord

Exmaple_CHORDS = [
    {"name": "C Major", "root": "C4", "type": "major"},
    {"name": "C# Major", "root": "C#4", "type": "major"},
    {"name": "D Major", "root": "D4", "type": "major"},
    {"name": "D# Major", "root": "D#4", "type": "major"},
    {"name": "E Major", "root": "E4", "type": "major"},
    {"name": "F Major", "root": "F4", "type": "major"},
    {"name": "F# Major", "root": "F#4", "type": "major"},
    {"name": "G Major", "root": "G4", "type": "major"},
    {"name": "G# Major", "root": "G#4", "type": "major"},
    {"name": "A Major", "root": "A4", "type": "major"},
    {"name": "A# Major", "root": "A#4", "type": "major"},
    {"name": "B Major", "root": "B4", "type": "major"},
    {"name": "C Minor", "root": "C4", "type": "minor"},
    {"name": "C# Minor", "root": "C#4", "type": "minor"},
    {"name": "D Minor", "root": "D4", "type": "minor"},
    {"name": "D# Minor", "root": "D#4", "type": "minor"},
    {"name": "E Minor", "root": "E4", "type": "minor"},
    {"name": "F Minor", "root": "F4", "type": "minor"},
    {"name": "F# Minor", "root": "F#4", "type": "minor"},
    {"name": "G Minor", "root": "G4", "type": "minor"},
    {"name": "G# Minor", "root": "G#4", "type": "minor"},
    {"name": "A Minor", "root": "A4", "type": "minor"},
    {"name": "A# Minor", "root": "A#4", "type": "minor"},
    {"name": "B Minor", "root": "B4", "type": "minor"},
    {"name": "C7", "root": "C4", "type": "dominant7"},
    {"name": "Cmaj7", "root": "C4", "type": "major7"},
    {"name": "Cm7", "root": "C4", "type": "minor7"},
    {"name": "Cdim7", "root": "C4", "type": "diminished7"},
    {"name": "C#7", "root": "C#4", "type": "dominant7"},
    {"name": "C#maj7", "root": "C#4", "type": "major7"},
    {"name": "C#m7", "root": "C#4", "type": "minor7"},
    {"name": "C#dim7", "root": "C#4", "type": "diminished7"},
    {"name": "Cdim", "root": "C4", "type": "diminished"},
    {"name": "C#dim", "root": "C#4", "type": "diminished"},
    {"name": "Caug", "root": "C4", "type": "augmented"},
    {"name": "C#aug", "root": "C#4", "type": "augmented"},
]

simple_chord = [
    [("C4", 0.5), ("E4", 0.5), ("G4", 0.5)],  # C Major
    [("D4", 0.5), ("F4", 0.5), ("A4", 0.5)],  # D Minor
    [("E4", 0.5), ("G4", 0.5), ("B4", 0.5)],  # E Minor
]

c_major_chords = [
    [("C4", 0.5), ("E4", 0.5), ("G4", 0.5)],  # C Major
    [("D4", 0.5), ("F4", 0.5), ("A4", 0.5)],  # D Minor
    [("E4", 0.5), ("G4", 0.5), ("B4", 0.5)],  # E Minor
    [("F4", 0.5), ("A4", 0.5), ("C5", 0.5)],  # F Major
    [("G4", 0.5), ("B4", 0.5), ("D5", 0.5)]   # G Major
]

d_minor_chords = [
    [("D4", 1.0), ("F4", 1.0), ("A4", 1.0)],  # D Minor
    [("E4", 1.5), ("G4", 1.5), ("B4", 1.5)],  # E Minor
    [("F4", 2.0), ("A4", 2.0), ("C5", 2.0)],  # F Major
    [("G4", 2.5), ("B4", 2.5), ("D5", 2.5)]   # G Major
]

seventh_chords = [
    [("C3", 0.5), ("E3", 0.5), ("G4", 0.5), ("B4", 0.5)],  # Cmaj7
    [("D3", 0.5), ("F3", 0.5), ("A4", 0.5), ("C5", 0.5)],  # Dm7
    [("E3", 0.5), ("G3", 0.5), ("B4", 0.5), ("D5", 0.5)],  # Em7
    [("G3", 1.0), ("B3", 1.0), ("D4", 1.0), ("F4", 1.0)],  # G7
    [("A3", 1.0), ("C4", 1.0), ("E4", 1.0), ("G4", 1.0)]   # Am7
]


