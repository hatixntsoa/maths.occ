"""
core/cryptography/caesar_cipher.py
Caesar (shift) cipher encoder/decoder with verbose steps.
"""
from core.i18n import s

def _shift_char(char, shift, mode="encode", lang="fr"):
    if char.isupper():
        offset, name = 65, s("caesar_uppercase", lang)
    elif char.islower():
        offset, name = 97, s("caesar_lowercase", lang)
    else:
        return char, s("caesar_non_alpha", lang, c=char)
    orig = ord(char) - offset
    direction = 1 if mode == "encode" else -1
    new = (orig + direction * shift) % 26
    result = chr(new + offset)
    action = s("caesar_encoded" if mode == "encode" else "caesar_decoded", lang)
    sign = "+" if direction == 1 else "-"
    expl = s("caesar_char_line", lang, c=char, name=name, orig=orig,
             sign=sign, shift=shift, new=new, r=result, action=action)
    return result, expl

def caesar_encode(text: str, shift: int, lang: str = "fr") -> dict:
    shift = shift % 26
    steps = [s("caesar_enc_header", lang), s("caesar_shift_line", lang, shift=shift),
             s("caesar_orig_line", lang, text=text), s("caesar_char_by_char", lang)]
    result_chars = []
    for char in text:
        r, expl = _shift_char(char, shift, "encode", lang)
        result_chars.append(r)
        steps.append(expl)
    encoded = "".join(result_chars)
    steps += [s("caesar_result_sep", lang), s("caesar_ciphertext", lang, text=encoded)]
    return {"mode": "encode", "input": text, "shift": shift, "output": encoded, "steps": steps}

def caesar_decode(text: str, shift: int, lang: str = "fr") -> dict:
    shift = shift % 26
    steps = [s("caesar_dec_header", lang), s("caesar_shift_line", lang, shift=shift),
             s("caesar_enc_line", lang, text=text), s("caesar_char_by_char", lang)]
    result_chars = []
    for char in text:
        r, expl = _shift_char(char, shift, "decode", lang)
        result_chars.append(r)
        steps.append(expl)
    decoded = "".join(result_chars)
    steps += [s("caesar_result_sep", lang), s("caesar_plaintext", lang, text=decoded)]
    return {"mode": "decode", "input": text, "shift": shift, "output": decoded, "steps": steps}


def brute_force_caesar(ciphertext: str, lang: str = "fr") -> list:
    """Try all 25 shifts and return all possible decodings."""
    results = []
    for shift in range(1, 26):
        decoded = ""
        for char in ciphertext:
            r, _ = _shift_char(char, shift, "decode", lang)
            decoded += r
        results.append({"shift": shift, "decoded": decoded})
    return results
