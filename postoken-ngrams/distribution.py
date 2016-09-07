import bisect
import random

class Distribution:

    def __init__(self, statistics):
        self.values = list(statistics.keys())
        self.weights = list(statistics.values())
        # Cumulate weights
        for i in range(1, len(self.weights)):
            self.weights[i] += self.weights[i - 1]

    def choice(self):
        rnd = random.randrange(self.weights[-1])
        index = bisect.bisect_right(self.weights, rnd)
        return self.values[index]

if __name__ == '__main__':
    import collections
    stats = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5}
    dist = Distribution(stats)
    results = collections.Counter()
    for test in range(1500000):
        results[dist.choice()] += 1
    print(results)
