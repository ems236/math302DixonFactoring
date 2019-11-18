class SmoothResidueSieve:
    def __init__(self, n, primes):
        self.data = [(num**2 - n) for num in range(0, n + 1)]
        self.max_value = n


        for prime in primes:
            # solve x^2 - n == 0 mod p
            quadratic_zeros = quadratic_zeros_mod_p(n, prime)
            if len(quadratic_zeros) == 2:
                for quadratic_zero in quadratic_zeros:
                    current_index = quadratic_zero
                    while current_index >= self.max_value:
                        self.decrement_value(current_index, prime)
                        current_index = current_index + prime

    def decrement_value(self, index, prime):
        if self.data[index] % prime == 0:
            self.data[index] = self.data[index] // prime

    def is_qr_smooth(self, a):
        return self.data[a] == 1

    @staticmethod
    def quadratic_zeros_mod_p(n, p):
        #brute force because you assume p is small
        solutions = []
        for num in range(0, p):
            if (num**2 - n) % p == 0:
                solutions.append(num)
        
        return solutions