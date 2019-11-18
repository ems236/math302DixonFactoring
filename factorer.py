from smooth_sieve import SmoothResidueSieve
from prime_sieve import PrimeSieve
import sys
import math
import random
from itertools import combinations

SELECTION_BOUND_CONSTANT = 0.45

def factor(number):
    #pick a value (B) for smoothness
    smoothness, selection_bound = smoothness_parameters(number)
    #find the primes up to B and check than none of them divide number
    primegenerator = PrimeSieve(number)
    if primegenerator.is_prime(number):
        return False, 0, 0

    primes = primegenerator.primes_at_or_below(smoothness)
    has_factor, a, b = any_divide(number, primes)
    if has_factor:
        return True, a, b
    
    #find a case of x^2 == y^2 mod n
    attempts = 0

    while attempts < 50: 
        first_root, second_root = roots_of_congruent_squares(number, selection_bound, primes)
        if first_root % number not in [second_root % number, (-1 * second_root) % number]:
            #find gcd(x-y, n)
            greater_root, lesser_root = max(first_root, second_root), min(second_root, first_root)
            factor_guess = math.gcd(greater_root - lesser_root, number)
            if factor_guess > 1:
                return True, factor_guess, number // factor_guess
            #try again if it makes trivial factors
        attempts = attempts + 1
    return False, 0, 0

def smoothness_parameters(number):
    logn = math.log(number)
    logsn = logn * math.log(logn)
    
    constant_term = 0.5 + SELECTION_BOUND_CONSTANT

    smoothness_b = math.ceil(math.exp(constant_term * (logn ** 0.5)))
    selection_boundary = math.ceil(number ** constant_term)

    return smoothness_b, selection_boundary

def any_divide(number, primes):
    for prime in primes:
        if number % prime == 0:
            return True, prime, number // prime
    return False, 0, 0

def roots_of_congruent_squares(number, selection_bound, primes):
    #generate pi(B) random smooth residues numbers in the correct range
    smooth_residue_list, source_list, possible_primes = smooth_residues(number, selection_bound, primes)
    #do guassian elimination on the factor exponent vectors to get another square
    residue_vectors = [smooth_number_prime_exponents(residue, possible_primes) for residue in smooth_residue_list]
    binary_residue_vectors = [to_binary_exponent_vector(vector) for vector in residue_vectors]
    perfect_square_indeces = subset_product_square_indeces(binary_residue_vectors)

    #solve x^2 == y^2 mod n
    return roots_for(source_list, residue_vectors, perfect_square_indeces, possible_primes)

def smooth_residues(number, selection_bound, primes):
    smooth_sieve = SmoothResidueSieve(number, selection_bound, primes)
    smooth_residue_list = []    
    generator_list = []

    lower_bound = math.ceil(number ** 0.5)

    found = 0
    iterations = 0
    while found < len(smooth_sieve.possible_primes) + 1:
        test = random.randint(lower_bound, selection_bound)
        if test not in generator_list and smooth_sieve.is_qr_smooth(test):
            smooth_residue_list.append(test ** 2 - number)
            generator_list.append(test)
            found = found + 1
        
        if iterations > number:
            raise RuntimeError("Couldn't find enough smooth numbers")
        iterations = iterations + 1

    return smooth_residue_list, generator_list, smooth_sieve.possible_primes

def exponent_divide(number, divisor):
    count = 0
    adjusted_number = number
    while adjusted_number % divisor == 0:
        count = count + 1
        adjusted_number = adjusted_number // divisor
    return count


def smooth_number_prime_exponents(number, primes):
    return [exponent_divide(number, prime) for prime in primes]

def to_binary_exponent_vector(vector):
    return [exponent % 2 for exponent in vector]

def subset_product_square_indeces(binary_residues):
    #this should use guassian elimination but it doesn't
    #brute force is good too

    for combination_size in range(2, len(binary_residues)):
        for combination in combinations(range(0, len(binary_residues)), combination_size):
            sum = [val for val in binary_residues[combination[0]]]
            for combination_index in range(1, combination_size):
                for item_index in range(0, len(binary_residues[0])):
                    sum[item_index] = (sum[item_index] + binary_residues[combination[combination_index]][item_index]) % 2
            if all(val == 0 for val in sum):
                return combination
    return None


    

def roots_for(source_list, residue_vectors, selected_indeces, primes):
    first_root = 1
    second_root = 1
    second_primes_exponents = [0 for _ in primes]

    for index in selected_indeces:
        first_root = first_root * source_list[index]
        for prime_index in range(0, len(primes)):
            second_primes_exponents[prime_index] = second_primes_exponents[prime_index] + residue_vectors[index][prime_index]

    for prime_index in range(0, len(primes)):
        second_root = second_root * (primes[prime_index] ** (second_primes_exponents[prime_index] // 2))
    
    return first_root, second_root


if __name__ == "__main__":
    if len(sys.argv) > 1:
        num = 0
        try:
            num = int(sys.argv[1])
        except:
            print(f"Please supply a number as the first argument")

        if num > 0:
            couldFactor, x, y = factor(num)
            if couldFactor:
                print(f"{num} can be factored as {x} * {y}")
            else:
                print(f"Could not factor {num}.  It is most likely prime")
        else:
            print(f"{num} is negative and will not be factored.")
    else:
        print(f"Please supply a number as the first argument")
