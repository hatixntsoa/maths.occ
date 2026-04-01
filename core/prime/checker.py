"""
core/prime/checker.py
Single-number primality test with step-by-step explanation.
"""
import math
from core.i18n import s

def is_prime(n: int) -> bool:
    """Simple trial-division primality test."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def check_prime_verbose(n: int, lang: str = "fr") -> dict:
    steps = []

    if n < 0:
        return {"n": n, "is_prime": False,
                "steps": [s("neg_not_prime", lang)],
                "verdict": s("not_prime_verdict", lang, n=n)}
    if n == 0:
        return {"n": 0, "is_prime": False,
                "steps": [s("zero_not_prime", lang)],
                "verdict": s("not_prime_verdict", lang, n=0)}
    if n == 1:
        return {"n": 1, "is_prime": False,
                "steps": [s("one_not_prime", lang)],
                "verdict": s("not_prime_verdict", lang, n=1)}
    if n == 2:
        return {"n": 2, "is_prime": True,
                "steps": [s("two_is_prime", lang)],
                "verdict": s("two_prime_verdict", lang)}

    steps.append(s("prime_test_header", lang, n=n))
    steps.append(s("sqrt_line", lang, n=n, sqrt=math.sqrt(n), isqrt=math.isqrt(n)))

    if n % 2 == 0:
        steps.append(s("div_by_2", lang, n=n, half=n//2))
        return {"n": n, "is_prime": False, "divisors_found": [2], "steps": steps,
                "verdict": s("not_prime_div2", lang, n=n)}

    steps.append(s("is_odd", lang, n=n, isqrt=math.isqrt(n)))
    divisors_found = []
    i = 3
    while i <= math.isqrt(n):
        if n % i == 0:
            steps.append(s("divisor_found", lang, n=n, i=i, quot=n//i))
            divisors_found.append(i)
            break
        else:
            steps.append(s("not_divisible", lang, n=n, i=i, rem=n%i))
        i += 2

    if divisors_found:
        return {"n": n, "is_prime": False, "divisors_found": divisors_found, "steps": steps,
                "verdict": s("not_prime_div", lang, n=n, div=divisors_found[0])}
    else:
        steps.append(s("no_divisor", lang, n=n, isqrt=math.isqrt(n)))
        return {"n": n, "is_prime": True, "divisors_found": [], "steps": steps,
                "verdict": s("is_prime_verdict", lang, n=n)}


def get_factors(n: int) -> list:
    """Return the prime factorization of n as a list of (prime, exponent) pairs."""
    if n < 2:
        return []
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return sorted(factors.items())
