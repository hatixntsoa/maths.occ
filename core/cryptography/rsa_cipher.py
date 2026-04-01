"""
core/cryptography/rsa_cipher.py
RSA encoder/decoder — educational implementation with full verbose output.
Miller-Rabin primality, Extended Euclidean for modular inverse.
"""
import random
import math


# ── Primality ────────────────────────────────────────────────────────────────

def _miller_rabin_witness(n: int, a: int) -> tuple[bool, list]:
    """Single Miller-Rabin round. Returns (passed, steps)."""
    steps = []
    # Write n-1 = 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    steps.append(f"    n-1 = {n-1} = 2^{r} × {d}")

    x = pow(a, d, n)
    steps.append(f"    a={a}, x = a^d mod n = {a}^{d} mod {n} = {x}")

    if x == 1 or x == n - 1:
        steps.append(f"    x ∈ {{1, n-1}} → témoin valide pour a={a}")
        return True, steps

    for i in range(r - 1):
        x = pow(x, 2, n)
        steps.append(f"    carré #{i+1}: x = {x}")
        if x == n - 1:
            steps.append(f"    x = n-1 → témoin valide pour a={a}")
            return True, steps

    steps.append(f"    Aucune condition remplie → {n} est COMPOSÉ (témoin a={a})")
    return False, steps


def is_prime_miller_rabin(n: int, k: int = 5, verbose: bool = False) -> tuple[bool, list]:
    """
    Miller-Rabin probabilistic primality test.
    Returns (is_prime, steps).
    """
    steps = []
    if n <= 1:
        return False, [f"{n} ≤ 1, non premier."]
    if n <= 3:
        return True, [f"{n} ≤ 3, premier."]
    if n % 2 == 0:
        return False, [f"{n} pair, non premier."]
    if n % 3 == 0 and n != 3:
        return False, [f"{n} divisible par 3, non premier."]

    steps.append(f"Test de Miller-Rabin pour n = {n}, {k} témoins aléatoires.")

    for _ in range(k):
        a = random.randrange(2, n - 1)
        passed, sub = _miller_rabin_witness(n, a)
        if verbose:
            steps.extend(sub)
        if not passed:
            steps.append(f"  → {n} est COMPOSÉ.")
            return False, steps

    steps.append(f"  → {n} est probablement PREMIER (confiance ≥ 1 - 4^(-{k})).")
    return True, steps


def generate_prime(bit_length: int = 64) -> tuple[int, list]:
    """
    Generate a random prime of the given bit length.
    Returns (prime, generation_steps).
    """
    steps = [f"Génération d'un nombre premier de {bit_length} bits..."]
    attempts = 0
    while True:
        attempts += 1
        candidate = random.getrandbits(bit_length) | (1 << (bit_length - 1)) | 1
        steps.append(f"  Tentative #{attempts} : candidat = {candidate}")
        prime, test_steps = is_prime_miller_rabin(candidate, k=5, verbose=False)
        if prime:
            steps.append(f"  ✓ {candidate} est premier après {attempts} tentative(s).")
            return candidate, steps


# ── Math helpers ──────────────────────────────────────────────────────────────

def _egcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean algorithm. Returns (gcd, x, y) such that ax + by = gcd."""
    if a == 0:
        return b, 0, 1
    g, y, x = _egcd(b % a, a)
    return g, x - (b // a) * y, y


def mod_inverse(a: int, m: int) -> tuple[int, list]:
    """
    Compute modular inverse of a mod m using Extended Euclidean Algorithm.
    Returns (inverse, steps).
    """
    steps = [f"Calcul de l'inverse modulaire de {a} modulo {m} (Algorithme d'Euclide étendu)"]
    g, x, _ = _egcd(a, m)
    if g != 1:
        steps.append(f"  gcd({a}, {m}) = {g} ≠ 1 → pas d'inverse!")
        raise ValueError(f"Pas d'inverse modulaire pour {a} mod {m}")
    inv = x % m
    steps.append(f"  gcd({a}, {m}) = 1 → inverse = {a} × {inv} ≡ 1 (mod {m})")
    steps.append(f"  d = {inv}")
    return inv, steps


# ── RSA Core ─────────────────────────────────────────────────────────────────

def rsa_generate_keys(bit_length: int = 64) -> dict:
    """
    Generate RSA key pair with full verbose output.
    Returns {p, q, n, phi, e, d, steps}.
    """
    steps = ["=== Génération des clés RSA ===", ""]

    # Step 1: Generate two distinct primes
    steps.append("── Étape 1 : Génération de deux premiers p et q ──")
    p, p_steps = generate_prime(bit_length)
    steps.extend(p_steps)
    steps.append("")

    q, q_steps = generate_prime(bit_length)
    while q == p:
        q, q_steps = generate_prime(bit_length)
    steps.extend(q_steps)
    steps.append(f"  p = {p}")
    steps.append(f"  q = {q}")
    steps.append("")

    # Step 2: Compute n = p*q
    n = p * q
    steps.append("── Étape 2 : Calcul de n = p × q ──")
    steps.append(f"  n = {p} × {q} = {n}")
    steps.append("")

    # Step 3: Compute phi(n)
    phi = (p - 1) * (q - 1)
    steps.append("── Étape 3 : Calcul de φ(n) = (p-1)(q-1) ──")
    steps.append(f"  φ({n}) = ({p}-1)({q}-1) = {p-1} × {q-1} = {phi}")
    steps.append("")

    # Step 4: Choose e
    e = 65537
    steps.append("── Étape 4 : Choix de l'exposant public e ──")
    steps.append(f"  e = 65537 (standard RSA, premier de Fermat F4)")
    steps.append(f"  Vérification : gcd({e}, {phi}) = {math.gcd(e, phi)}")
    if math.gcd(e, phi) != 1:
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2
        steps.append(f"  65537 ne convient pas → nouvel e = {e}")
    else:
        steps.append(f"  gcd = 1 ✓, e = {e} est valide")
    steps.append("")

    # Step 5: Compute d
    steps.append("── Étape 5 : Calcul de la clé privée d = e⁻¹ mod φ(n) ──")
    d, inv_steps = mod_inverse(e, phi)
    steps.extend(inv_steps)
    steps.append("")

    steps.append("── Clés générées ──")
    steps.append(f"  Clé publique  : (e={e}, n={n})")
    steps.append(f"  Clé privée    : (d={d}, n={n})")
    steps.append(f"  (p={p}, q={q} — SECRETS, ne jamais partager)")

    return {
        "p": p, "q": q, "n": n,
        "phi": phi, "e": e, "d": d,
        "steps": steps,
    }


def rsa_encrypt(message: str, e: int, n: int) -> dict:
    """
    Encrypt a UTF-8 string with RSA public key (e, n).
    Returns {ciphertext, steps}.
    """
    steps = ["=== RSA Chiffrement ===", ""]
    m_bytes = message.encode("utf-8")
    m = int.from_bytes(m_bytes, byteorder="big")

    steps.append(f"① Message  : '{message}'")
    steps.append(f"② Bytes UTF-8 : {list(m_bytes)}")
    steps.append(f"③ Entier m  : {m}")
    steps.append(f"④ Vérification : m ({m}) < n ({n}) ? {'✓' if m < n else '✗ ERREUR : message trop grand'}")

    if m >= n:
        return {"error": "Message trop grand pour ces clés. Utilisez des clés plus grandes.", "steps": steps}

    c = pow(m, e, n)
    steps.append(f"⑤ Chiffrement : c = m^e mod n = {m}^{e} mod {n}")
    steps.append(f"   c = {c}")
    steps.append(f"   (hex: {hex(c)[2:].upper()})")

    return {
        "input": message,
        "m": m,
        "e": e,
        "n": n,
        "ciphertext": c,
        "ciphertext_hex": hex(c)[2:].upper(),
        "steps": steps,
    }


def rsa_decrypt(ciphertext: int, d: int, n: int) -> dict:
    """
    Decrypt RSA ciphertext with private key (d, n).
    Returns {plaintext, steps}.
    """
    steps = ["=== RSA Déchiffrement ===", ""]
    steps.append(f"① Chiffré c : {ciphertext}")
    steps.append(f"② Clé privée : d = {d}, n = {n}")
    steps.append(f"③ Déchiffrement : m = c^d mod n = {ciphertext}^{d} mod {n}")

    m = pow(ciphertext, d, n)
    steps.append(f"   m = {m}")

    try:
        plaintext_bytes = m.to_bytes((m.bit_length() + 7) // 8, byteorder="big")
        plaintext = plaintext_bytes.decode("utf-8")
        steps.append(f"④ Bytes : {list(plaintext_bytes)}")
        steps.append(f"⑤ Texte UTF-8 : '{plaintext}'")
        return {
            "ciphertext": ciphertext,
            "m": m,
            "d": d,
            "n": n,
            "plaintext": plaintext,
            "steps": steps,
        }
    except (UnicodeDecodeError, OverflowError) as ex:
        steps.append(f"④ m = {m} (impossible à décoder en UTF-8 : {ex})")
        return {
            "ciphertext": ciphertext,
            "m": m,
            "d": d,
            "n": n,
            "plaintext": None,
            "plaintext_int": m,
            "steps": steps,
        }


def rsa_encrypt_with_keys(message: str, p: int, q: int) -> dict:
    """Generate keys from p, q then encrypt."""
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if math.gcd(e, phi) != 1:
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2
    d, _ = mod_inverse(e, phi)
    enc = rsa_encrypt(message, e, n)
    enc["d"] = d
    enc["p"] = p
    enc["q"] = q
    return enc
