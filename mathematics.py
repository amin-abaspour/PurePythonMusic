
PI = 3.1415

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def sine(x, terms=10):
    x %= 2 * PI  # Reduce to within 0 to 2π
    result = 0
    for n in range(terms):
        coef = (-1) ** n  # Alternate between addition and subtraction
        power = 2 * n + 1
        result += coef * (x ** power) / factorial(power)
    return result


# Clamp function to restrict values within a range
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

