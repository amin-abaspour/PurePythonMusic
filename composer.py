from random import choice, random
from waves import sine_wave, triangle_wave, sawtooth_wave
from wav import write_wav, chords_to_wave
from chords import build_chord
from harmonizer import create_parallel_harmony
from rhythm import apply_rhythm_pattern
from midi import note_to_midi, midi_to_note

# Musical scales and their intervals
SCALES = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'pentatonic': [0, 2, 4, 7, 9],
    'blues': [0, 3, 5, 6, 7, 10],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10]
}

# Chord progressions by scale degree (using Roman numerals)
PROGRESSIONS = {
    'major': [
        ['I', 'IV', 'V', 'I'],
        ['I', 'vi', 'IV', 'V'],
        ['ii', 'V', 'I', 'vi'],
        ['I', 'V', 'vi', 'IV']
    ],
    'minor': [
        ['i', 'iv', 'V', 'i'],
        ['i', 'VI', 'III', 'VII'],
        ['i', 'iv', 'v', 'i'],
        ['i', 'VII', 'VI', 'V']
    ]
}

def generate_scale(root, scale_type='major'):
    """Generate notes of a scale from root note."""
    root_midi = note_to_midi(root)
    scale_notes = []
    for interval in SCALES[scale_type]:
        note = midi_to_note(root_midi + interval)
        scale_notes.append(note)
    return scale_notes

def create_melody_pattern(scale_notes, pattern_length=8):
    """Create a melodic pattern using notes from the scale."""
    pattern = []
    current_direction = 1  # 1 for ascending, -1 for descending
    
    for i in range(pattern_length):
        if random() < 0.2:  # 20% chance to change direction
            current_direction *= -1
            
        note = choice(scale_notes)
        duration = choice([0.25, 0.5, 1.0])  # Varying note lengths
        pattern.append((note, duration))
        
    return pattern

class MusicComposer:
    def __init__(self, root_note="C4", scale_type="major", tempo=120):
        self.root_note = root_note
        self.scale_type = scale_type
        self.tempo = tempo
        self.scale_notes = generate_scale(root_note, scale_type)
        
    def generate_chord_progression(self, length=4):
        """Generate a chord progression based on scale type."""
        progression = choice(PROGRESSIONS[self.scale_type])
        chords = []
        
        for chord_numeral in progression:
            # Convert Roman numeral to chord
            degree = self._numeral_to_degree(chord_numeral)
            root = self.scale_notes[degree]
            
            # Determine chord type based on scale degree
            if chord_numeral.isupper():
                chord_type = "major"
            else:
                chord_type = "minor"
                
            # Add seventh chords occasionally
            if random() < 0.3:
                chord_type += "7"
                
            chords.append(build_chord(root, chord_type, duration=1.0))
            
        return chords
    
    def generate_composition(self, num_bars=8):
        """Generate a complete musical composition."""
        # Generate main melody
        melody = create_melody_pattern(self.scale_notes, num_bars * 2)
        
        # Create harmony
        harmony = create_parallel_harmony(melody, interval=4)  # Parallel thirds
        
        # Generate chord progression
        chords = self.generate_chord_progression(num_bars)
        
        # Apply rhythm patterns
        rhythm_patterns = ['swing', 'samba', 'rock']
        melody = apply_rhythm_pattern(melody, choice(rhythm_patterns))
        harmony = apply_rhythm_pattern(harmony, choice(rhythm_patterns))
        
        return melody, harmony, chords
    
    def render_composition(self, sample_rate=44100):
        """Render the composition to audio samples."""
        melody, harmony, chords = self.generate_composition()
        
        # Render chord progression (background)
        chord_wave = chords_to_wave(chords, sample_rate, wave_type=sine_wave,
                                  attack=0.1, decay=0.1, sustain_level=0.5)
        
        # Render melody (foreground)
        melody_wave = chords_to_wave([[note] for note in melody], sample_rate,
                                   wave_type=triangle_wave, attack=0.05,
                                   sustain_level=0.8)
        
        # Render harmony (middle ground)
        harmony_wave = chords_to_wave([[note] for note in harmony], sample_rate,
                                    wave_type=sawtooth_wave, attack=0.05,
                                    sustain_level=0.4)
        
        # Mix all parts together
        max_length = max(len(chord_wave), len(melody_wave), len(harmony_wave))
        mixed_wave = [0] * max_length
        
        for i in range(max_length):
            sample = 0
            if i < len(chord_wave):
                sample += chord_wave[i] * 0.4  # Chords at 40% volume
            if i < len(melody_wave):
                sample += melody_wave[i] * 0.8  # Melody at 80% volume
            if i < len(harmony_wave):
                sample += harmony_wave[i] * 0.3  # Harmony at 30% volume
            mixed_wave[i] = sample
            
        # Normalize
        max_amplitude = max(abs(min(mixed_wave)), abs(max(mixed_wave)))
        if max_amplitude > 1.0:
            mixed_wave = [sample / max_amplitude for sample in mixed_wave]
            
        return mixed_wave
    
    def _numeral_to_degree(self, numeral):
        """Convert Roman numeral to scale degree (0-based index)."""
        numerals = {
            'I': 0, 'II': 1, 'III': 2, 'IV': 3, 'V': 4, 'VI': 5, 'VII': 6,
            'i': 0, 'ii': 1, 'iii': 2, 'iv': 3, 'v': 4, 'vi': 5, 'vii': 6
        }
        return numerals[numeral.upper()]

# Example usage
if __name__ == "__main__":
    # Create composers in different keys and modes
    composers = [
        MusicComposer("C4", "major", 120),    # C Major
        MusicComposer("A4", "minor", 110),    # A Minor
        # MusicComposer("G4", "mixolydian", 125),  # G Mixolydian
        # MusicComposer("D4", "dorian", 115)    # D Dorian
    ]
    
    # Generate compositions in different styles
    for i, composer in enumerate(composers):
        samples = composer.render_composition()
        write_wav(f"./output/composition_{i+1}.wav", samples, 44100)
