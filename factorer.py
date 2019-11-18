from smooth_sieve import SmoothResidueSieve
from prime_sieve import PrimeSieve
import sys
import math

SMOOTHNESS_CONSTANT = 0.01

def factor(number):
    #pick a value (B) for smoothness
    smoothness, selection_bound = smoothness_parameters(number)
    #find the primes up to B and check than none of them divide number
    primegenerator = PrimeSieve(smoothness)
    primes = primegenerator.primes_at_or_below(smoothness)
    has_factor, a, b = any_divide(number, primes)
    if has_factor:
        return a, b
    
    #generate pi(B) random smooth residues numbers in the correct range
    smooth_sieve = SmoothResidueSieve(number, selection_bound, primes)
    #do guassian elimination on the factor exponent vectors to get another square
    #solve x^2 == y^2 mod n
    #find gcd(x-y, n)
    #try again if it makes trivial factors
    pass

def smoothness_parameters(number):
    logn = math.log(number)
    logsn = logn * math.log(logn)
    
    constant_term = 0.5 + SMOOTHNESS_CONSTANT

    smoothness_b = math.ceil(math.exp(constant_term * (logn ** 0.5)))
    selection_boundary = math.ceil(number ** constant_term)

    return smoothness_b, selection_boundary

def any_divide(number, primes):
    for prime in primes:
        if number % prime == 0:
            return True, prime, number // prime
    return False, 0, 0

def smooth_residues(number, selection_bound, primes):
    smooth_sieve = SmoothResidueSieve(number, selection_bound, primes)
    smooth_residue_set = set()

    while len(smooth_residue_set) < len(primes) + 1:
        


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

if __name__ == "__main__":
    if sys.argv > 1:
        num = 0
        try:
            num = int(sys.argv[1])
            if num > 0:
                x, y = factor(num)
                print(f"{num} can be factored as {x} * {y}")
            else:
                print(f"{num} is negative and will not be factored.")
        except:
            print(f"Please supply a number as the first argument")
    else:
        print(f"Please supply a number as the first argument")
