from math import sqrt, ceil


def ferma(number):
    p = ceil(sqrt(number))
    while (q := sqrt(p**2 - number)) < number:
        if not q % 1:
            return int(p + q), int(p - q)
        p += 1


# print(ferma(15811))
