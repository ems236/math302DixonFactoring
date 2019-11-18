from smooth_sieve import SmoothResidueSieve
from prime_sieve import PrimeSieve

""""""

def exponent_divide(number, divisor):
    count = 0
    adjusted_number = number
    while adjusted_number % divisor == 0:
        count = count + 1
        adjusted_number = adjusted_number // divisor
    return count


def smooth_number_prime_exponents(number, primes):
    return [exponent_divide(number, prime) for prime in primes]


def factor_exponents_to_binary(exponents):
    return [exponent % 2 for exponent in exponents]
