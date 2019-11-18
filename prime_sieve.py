
class PrimeSieve:
    def __init__(self, maxValue):
        self.maxValue = maxValue
        self.__populate_data()
        

    def __populate_data(self):
        self.data = [True for _ in range(0, self.maxValue + 1)]
        for prime in range(2, self.maxValue // 2):
            if self.data[prime]:
                current_multiple = 2 * prime
                while current_multiple <= self.maxValue:
                    self.data[current_multiple] = False
                    current_multiple = current_multiple + prime
    
    def is_prime(self, number):
        if number > self.maxValue:
            self.maxValue = number
            self.__populate_data()
        
        return self.data[number]

    def first_n_primes(self, count):
        selected_primes = []
        for i in range(2, self.maxValue):
            if self.data[i]:
                selected_primes.append(i)
                if len(selected_primes) == count:
                    return selected_primes
        return None
    
    def primes_at_or_below(self, max_val):
        selected_primes = []
        for i in range(2, min(self.maxValue, max) + 1):
            if self.data[i]:
                selected_primes.append(i)
        return selected_primes