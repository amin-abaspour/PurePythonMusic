
from wav import write_wav, melody_to_wave, melody_with_adsr, polyphony_to_wave, note_to_wave
from waves import sine_wave, square_wave, triangle_wave, sawtooth_wave

# A4 Note with different waves
# write_wav("./output/sine_wave.wav", sine_wave(440, 44100, 1), 44100)
# write_wav("./output/square_wave.wav", square_wave(440, 44100, 1), 44100)
# write_wav("./output/triangle_wave.wav", triangle_wave(440, 44100, 1), 44100)
# write_wav("./output/sawtooth_wave.wav", sawtooth_wave(440, 44100, 1), 44100)

from songs import ascending_scale, descending_scale, simple_melody, twinkle_twinkle, ode_to_joy

# write_wav("./output/ascending_scale.wav", melody_to_wave(ascending_scale, 44100), 44100)
# write_wav("./output/descending_scale.wav", melody_to_wave(descending_scale, 44100), 44100)
# write_wav("./output/simple_melody.wav", melody_to_wave(simple_melody, 44100), 44100)

# write_wav("./output/twinkle_twinkle.wav", melody_to_wave(twinkle_twinkle, 44100), 44100)
# write_wav("./output/ode_to_joy.wav", melody_to_wave(ode_to_joy, 44100), 44100)

# write_wav("./output/twinkle_twinkle_adsr.wav", melody_with_adsr(twinkle_twinkle, 44100), 44100)
# write_wav("./output/ode_to_joy_adsr.wav", melody_with_adsr(ode_to_joy, 44100), 44100)

from chords import simple_chord, c_major_chords, d_minor_chords, seventh_chords

# write_wav("./output/simple_chord.wav", polyphony_to_wave(simple_chord, 44100, wave_type=sine_wave), 44100)
# write_wav("./output/c_major_progression.wav", polyphony_to_wave(c_major_chords, 44100, wave_type=sine_wave), 44100)
# write_wav("./output/d_minor_progression.wav", polyphony_to_wave(d_minor_chords, 44100, wave_type=sine_wave), 44100)
# write_wav("./output/seventh_chords.wav", polyphony_to_wave(seventh_chords, 44100, wave_type=sine_wave), 44100)

from chords import build_chord

# write_wav("./output/chord_C_major.wav", polyphony_to_wave([build_chord("C4", "major")], 44100, wave_type=sine_wave), 44100)  # C Major
# write_wav("./output/chord_A_minor.wav", polyphony_to_wave([build_chord("A3", "minor")], 44100, wave_type=sine_wave), 44100)
# write_wav("./output/chord_G7.wav", polyphony_to_wave([build_chord("G3", "dominant7")], 44100, wave_type=sine_wave), 44100)  # G Dominant 7th
# write_wav("./output/chord_Cmaj7.wav", polyphony_to_wave([build_chord("C4", "major7")], 44100, wave_type=sine_wave), 44100)  # C Major 7th
# write_wav("./output/chord_Em7.wav", polyphony_to_wave([build_chord("E4", "minor7")], 44100, wave_type=sine_wave), 44100)  # E Minor 7th
# write_wav("./output/chord_D_minor.wav", polyphony_to_wave([build_chord("D4", "minor")], 44100, wave_type=sine_wave), 44100)  # D Minor
# write_wav("./output/chord_F_major.wav", polyphony_to_wave([build_chord("F4", "major")], 44100, wave_type=sine_wave), 44100)  # F Major
# write_wav("./output/chord_Bdim7.wav", polyphony_to_wave([build_chord("B3", "diminished7")], 44100, wave_type=sine_wave), 44100)  # B Diminished 7th
# write_wav("./output/chord_C#m7.wav", polyphony_to_wave([build_chord("C#4", "minor7")], 44100, wave_type=sine_wave), 44100)  # C# Minor 7th
# write_wav("./output/chord_A7.wav", polyphony_to_wave([build_chord("A3", "dominant7")], 44100, wave_type=sine_wave), 44100)  # A Dominant 7th


# This has a bug, just plays a single chord, probably the last chord

# write_wav("./output/c_major_chords.wav", 
#           polyphony_to_wave([
#               build_chord("C4", "major"),      # C Major
#               build_chord("D4", "minor"),      # D Minor
#               build_chord("E4", "minor"),      # E Minor
#               build_chord("F4", "major"),      # F Major
#               build_chord("G4", "major"),      # G Major
#           ], 44100, wave_type=sine_wave), 44100)

# # Twinkle, Twinkle, Little Star with chords
# write_wav(
#     "./output/twinkle_twinkle_with_chords.wav",
#     polyphony_to_wave([
#         build_chord("C4", "major"), build_chord("C4", "major"),
#         build_chord("G4", "major"), build_chord("G4", "major"),
#         build_chord("A4", "minor"), build_chord("A4", "minor"),
#         build_chord("G4", "major"),
#         build_chord("F4", "major"), build_chord("F4", "major"),
#         build_chord("E4", "minor"), build_chord("E4", "minor"),
#         build_chord("D4", "minor"), build_chord("D4", "minor"),
#         build_chord("C4", "major")
#     ],
#     44100,
#     wave_type=sine_wave
#     ),
#     44100
# )  # Twinkle Twinkle, Little Star with C, G, A minor, F, E minor, D minor chords

# # Ode to Joy with chords
# write_wav(
#     "./output/ode_to_joy_with_chords.wav",
#     polyphony_to_wave([
#         build_chord("C4", "major"), build_chord("C4", "major"),
#         build_chord("D4", "major"), build_chord("D4", "major"),
#         build_chord("E4", "major"), build_chord("E4", "major"),
#         build_chord("D4", "major"), build_chord("D4", "major"),
#         build_chord("C4", "major"), build_chord("C4", "major"),
#         build_chord("G4", "major"), build_chord("G4", "major"),
#         build_chord("A4", "major"), build_chord("A4", "major"),
#         build_chord("G4", "major"),
#         build_chord("F4", "major"), build_chord("F4", "major"),
#         build_chord("E4", "major"), build_chord("E4", "major"),
#         build_chord("D4", "major"), build_chord("D4", "major"),
#         build_chord("C4", "major"), build_chord("C4", "major"),
#         build_chord("G4", "major"), build_chord("G4", "major"),
#         build_chord("F4", "major"), build_chord("F4", "major"),
#         build_chord("E4", "major"), build_chord("E4", "major"),
#         build_chord("D4", "major"), build_chord("D4", "major"),
#         build_chord("C4", "major")
#     ],
#     44100,
#     wave_type=sine_wave
#     ),
#     44100
# )  # Ode to Joy with C, D, E, G, A, F major chords

# Alternative function which works.
from wav import chords_to_wave

# # Twinkle, Twinkle, Little Star with chords
# twinkle_chords = [
#     build_chord("C4", "major"), build_chord("C4", "major"),
#     build_chord("G4", "major"), build_chord("G4", "major"),
#     build_chord("A4", "minor"), build_chord("A4", "minor"),
#     build_chord("G4", "major"),
#     build_chord("F4", "major"), build_chord("F4", "major"),
#     build_chord("E4", "minor"), build_chord("E4", "minor"),
#     build_chord("D4", "minor"), build_chord("D4", "minor"),
#     build_chord("C4", "major")
# ]

# write_wav(
#     "./output/twinkle_twinkle_with_chords.wav",
#     chords_to_wave(
#         twinkle_chords,
#         44100,
#         wave_type=sine_wave,
#         use_adsr=True,
#         attack=0.05,
#         decay=0.05,
#         sustain_level=0.7,
#         release=0.05
#     ),
#     44100
# )

# # Ode to Joy with chords
# ode_to_joy_chords = [
#     build_chord("C4", "major"), build_chord("C4", "major"),
#     build_chord("D4", "major"), build_chord("D4", "major"),
#     build_chord("E4", "major"), build_chord("E4", "major"),
#     build_chord("D4", "major"), build_chord("D4", "major"),
#     build_chord("C4", "major"), build_chord("C4", "major"),
#     build_chord("G4", "major"), build_chord("G4", "major"),
#     build_chord("A4", "major"), build_chord("A4", "major"),
#     build_chord("G4", "major"),
#     build_chord("F4", "major"), build_chord("F4", "major"),
#     build_chord("E4", "major"), build_chord("E4", "major"),
#     build_chord("D4", "major"), build_chord("D4", "major"),
#     build_chord("C4", "major"), build_chord("C4", "major"),
#     build_chord("G4", "major"), build_chord("G4", "major"),
#     build_chord("F4", "major"), build_chord("F4", "major"),
#     build_chord("E4", "major"), build_chord("E4", "major"),
#     build_chord("D4", "major"), build_chord("D4", "major"),
#     build_chord("C4", "major")
# ]

# write_wav(
#     "./output/ode_to_joy_with_chords.wav",
#     chords_to_wave(
#         ode_to_joy_chords,
#         44100,
#         wave_type=sine_wave,
#         use_adsr=True,
#         attack=0.05,
#         decay=0.05,
#         sustain_level=0.7,
#         release=0.05
#     ),
#     44100
# )

write_wav(
    "./output/c_major_chords.wav",
    chords_to_wave([
        build_chord("C4", "major", duration=1.0),   # C Major for 1 second
        build_chord("D4", "minor", duration=1.0),   # D Minor for 1 second
        build_chord("E4", "minor", duration=1.0),   # E Minor for 1 second
        build_chord("F4", "major", duration=1.0),   # F Major for 1 second
        build_chord("G4", "major", duration=1.0),   # G Major for 1 second
    ], sample_rate=44100, wave_type=sine_wave),
    sample_rate=44100
)

write_wav("./output/d_minor_chords.wav", 
          chords_to_wave([
              build_chord("D4", "minor"),      # D Minor
              build_chord("E4", "minor"),      # E Minor
              build_chord("F4", "major"),      # F Major
              build_chord("G4", "major"),      # G Major
          ], 44100, wave_type=sine_wave), 44100)

write_wav("./output/seventh_chords.wav", 
          chords_to_wave([
              build_chord("C3", "major7"),     # Cmaj7
              build_chord("D3", "minor7"),     # Dm7
              build_chord("E3", "minor7"),     # Em7
              build_chord("G3", "dominant7"),  # G7
              build_chord("A3", "minor7"),     # Am7
          ], 44100, wave_type=sine_wave), 44100)

write_wav(
    "./output/c_major_with_melody.wav",
    chords_to_wave([
        build_chord("C4", "major"),      # C Major
        build_chord("D4", "minor"),      # D Minor
        build_chord("E4", "minor"),      # E Minor
        build_chord("F4", "major"),      # F Major
        build_chord("G4", "major"),      # G Major
    ], 44100, wave_type=sine_wave) +
    chords_to_wave([
        build_chord("E5", "major"),      # Melody Note 1
        build_chord("F5", "major"),      # Melody Note 2
        build_chord("G5", "major"),      # Melody Note 3
        build_chord("A5", "major"),      # Melody Note 4
        build_chord("G5", "major"),      # Melody Note 5
    ], 44100, wave_type=sine_wave),
    44100
)

write_wav(
    "./output/seventh_chords_with_melody.wav",
    chords_to_wave([
        build_chord("C3", "major7"),     # Cmaj7
        build_chord("D3", "minor7"),     # Dm7
        build_chord("E3", "minor7"),     # Em7
        build_chord("G3", "dominant7"),  # G7
        build_chord("A3", "minor7"),     # Am7
    ], 44100, wave_type=sine_wave) +
    chords_to_wave([
        build_chord("G4", "major"),      # Melody Note 1
        build_chord("A4", "major"),      # Melody Note 2
        build_chord("B4", "major"),      # Melody Note 3
        build_chord("D5", "major"),      # Melody Note 4
        build_chord("C5", "major"),      # Melody Note 5
    ], 44100, wave_type=sine_wave),
    44100
)

