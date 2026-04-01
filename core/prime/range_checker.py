"""
core/prime/range_checker.py
Check primes in a range using GCD-based method (trial division via gcd).
"""
import math
from .checker import is_prime
from core.i18n import s


def gcd(a: int, b: int) -> int:
    """Euclidean GCD."""
    while b:
        a, b = b, a % b
    return a


def is_prime_via_gcd(n: int, lang: str = "fr") -> tuple[bool, list]:
    if n < 2:
        return False, [s("less_than_2", lang, n=n)]
    if n == 2:
        return True, [s("n_eq_2", lang)]
    steps = []
    limit = math.isqrt(n)
    steps.append(s("gcd_method_header", lang, n=n, limit=limit))
    for k in range(2, limit + 1):
        g = gcd(n, k)
        steps.append(s("gcd_line", lang, n=n, k=k, g=g))
        if g > 1:
            steps.append(s("gcd_gt1", lang, n=n, k=k))
            return False, steps
    steps.append(s("gcd_ok", lang, n=n, limit=limit))
    return True, steps

def primes_in_range(a: int, b: int, lang: str = "fr") -> dict:
    if a > b:
        return {"error": s("range_error_order", lang)}
    if b - a > 10_000:
        return {"error": s("range_error_size", lang)}
    results, primes, composites = [], [], []
    for n in range(max(2, a), b + 1):
        prime, steps = is_prime_via_gcd(n, lang)
        results.append({"n": n, "is_prime": prime, "steps": steps})
        (primes if prime else composites).append(n)
    return {"range": [a, b], "count": len(primes), "primes": primes,
            "composites": composites, "results": results}


def primes_sieve(limit: int) -> list:
    """Sieve of Eratosthenes up to limit."""
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, math.isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, v in enumerate(sieve) if v]
