from mathematics import PI, sine

def sine_wave(frequency, sample_rate, duration):
    samples = []
    for n in range(int(sample_rate * duration)):
        t = n / sample_rate
        angle = (2 * PI * frequency * t) % (2 * PI)
        samples.append(sine(angle))
    return samples

def square_wave(frequency, sample_rate, duration):
    samples = []
    period = 1 / frequency
    for n in range(int(sample_rate * duration)):
        t = n / sample_rate
        if (t % period) < (period / 2):
            samples.append(1.0)
        else:
            samples.append(-1.0)
    return samples

def triangle_wave(frequency, sample_rate, duration):
    samples = []
    period = 1 / frequency
    for n in range(int(sample_rate * duration)):
        t = n / sample_rate
        value = 2 * (t / period - int(t / period + 0.5))
        samples.append(2 * abs(value) - 1)
    return samples

def sawtooth_wave(frequency, sample_rate, duration):
    samples = []
    period = 1 / frequency
    for n in range(int(sample_rate * duration)):
        t = n / sample_rate
        value = 2 * (t / period - int(t / period)) - 1
        samples.append(value)
    return samples