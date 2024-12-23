def low_pass_filter(samples, cutoff_frequency, sample_rate):
    """Apply a low-pass filter to the samples."""
    rc = 1.0 / (cutoff_frequency * 2 * 3.1415)
    dt = 1.0 / sample_rate
    alpha = dt / (rc + dt)
    
    filtered_samples = []
    previous_sample = samples[0]
    for sample in samples:
        filtered_sample = previous_sample + (alpha * (sample - previous_sample))
        filtered_samples.append(filtered_sample)
        previous_sample = filtered_sample
    
    return filtered_samples
