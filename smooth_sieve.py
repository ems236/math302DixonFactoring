class SmoothResidueSieve:
    def __init__(self, n, bound, primes):
        self.data = [(num**2 - n) for num in range(0, bound + 1)]
        self.max_value = bound

        for prime in primes:
            # solve x^2 - n == 0 mod p
            quadratic_zeros = quadratic_zeros_mod_p(n, prime)
            if quadratic_zeros:
                for quadratic_zero in quadratic_zeros:
                    self.sieve_for_zero(quadratic_zero, prime)

    def sieve_for_zero(self, quadratic_zero, prime):
        current_index = quadratic_zero
        while current_index <= self.max_value:
            self.decrement_value(current_index, prime)
            current_index = current_index + prime

    def decrement_value(self, index, prime):
        print(f"decrementing {index} for prime {prime}, value is {self.data[index]}")
        while self.data[index] > 0 and self.data[index] % prime == 0 :
            self.data[index] = self.data[index] // prime
        print(f"value is now {self.data[index]} \n")

    def is_qr_smooth(self, a):
        return self.data[a] == 1

    
def quadratic_zeros_mod_p(n, p):
        #brute force because you assume p is small
        solutions = []
        for num in range(0, p):
            if (num**2 - n) % p == 0:
                solutions.append(num)
        
        return solutions