
from wav import write_wav, melody_to_wave, melody_with_adsr, polyphony_to_wave, note_to_wave
from waves import sine_wave, square_wave, triangle_wave, sawtooth_wave

# A4 Note with different waves
# write_wav("./output/sine_wave.wav", sine_wave(440, 44100, 1), 44100)
# write_wav("./output/square_wave.wav", square_wave(440, 44100, 1), 44100)
# write_wav("./output/triangle_wave.wav", triangle_wave(440, 44100, 1), 44100)
# write_wav("./output/sawtooth_wave.wav", sawtooth_wave(440, 44100, 1), 44100)

from songs import ascending_scale, descending_scale, simple_melody, twinkle_twinkle, ode_to_joy
from chords import simple_chord, c_major_chords, d_minor_chords, seventh_chords

# write_wav("./output/ascending_scale.wav", melody_to_wave(ascending_scale, 44100), 44100)
# write_wav("./output/descending_scale.wav", melody_to_wave(descending_scale, 44100), 44100)
# write_wav("./output/simple_melody.wav", melody_to_wave(simple_melody, 44100), 44100)

# write_wav("./output/twinkle_twinkle.wav", melody_to_wave(twinkle_twinkle, 44100), 44100)
# write_wav("./output/ode_to_joy.wav", melody_to_wave(ode_to_joy, 44100), 44100)

# write_wav("./output/twinkle_twinkle_adsr.wav", melody_with_adsr(twinkle_twinkle, 44100), 44100)
# write_wav("./output/ode_to_joy_adsr.wav", melody_with_adsr(ode_to_joy, 44100), 44100)

# write_wav("./output/simple_chord.wav", polyphony_to_wave(simple_chord, 44100, wave_type=sine_wave), 44100)

# write_wav("./output/c_major_progression.wav", polyphony_to_wave(c_major_chords, 44100, wave_type=sine_wave), 44100)

# write_wav("./output/d_minor_progression.wav", polyphony_to_wave(d_minor_chords, 44100, wave_type=sine_wave), 44100)

# write_wav("./output/seventh_chords.wav", polyphony_to_wave(seventh_chords, 44100, wave_type=sine_wave), 44100)
