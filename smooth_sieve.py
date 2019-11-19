class SmoothResidueSieve:
    def __init__(self, n, lower_bound, upper_bound, primes):
        #self.data = [(num**2 - n) for num in range(0, bound + 1)]
        self.data = []
        number = lower_bound
        while number < upper_bound + 1:
            self.data.append(number**2 - n)
            number = number + 1
        self.max_value = upper_bound
        self.min_value = lower_bound
        self.possible_primes = []

        for prime in primes:
            # solve x^2 - n == 0 mod p
            quadratic_zeros = quadratic_zeros_mod_p(n, prime)
            if quadratic_zeros:
                self.possible_primes.append(prime)
                for quadratic_zero in quadratic_zeros:
                    self.sieve_for_zero(quadratic_zero, prime)

    def sieve_for_zero(self, quadratic_zero, prime):
        current_number = self.min_value
        current_mod = self.min_value % prime
        if current_mod <= quadratic_zero:
            current_number = current_number + quadratic_zero - current_mod
        else:
            current_number = current_number + quadratic_zero - current_mod + prime
        
        while current_number <= self.max_value:
            self.decrement_value(current_number, prime)
            current_number = current_number + prime

    def decrement_value(self, number, prime):
        index = number - self.min_value
        while self.data[index] % prime == 0 :
            self.data[index] = self.data[index] // prime

    def is_qr_smooth(self, a):
        return self.data[a - self.min_value] == 1

    
def quadratic_zeros_mod_p(n, p):
    #brute force because you assume p is small
    solutions = []
    for num in range(0, p):
        if (num**2 - n) % p == 0:
            solutions.append(num)
    
    return solutions