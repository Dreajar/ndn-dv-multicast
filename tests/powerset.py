from itertools import chain, combinations

def powerset(num):
    s = range(num)
    return list(chain.from_iterable(combinations(s, r) for r in range(2, num + 1)))

def main():
    print(powerset(3))
    print(powerset(4))

if __name__ == '__main__':
    main()