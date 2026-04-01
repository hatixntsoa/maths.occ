"""
core/cryptography/base64_cipher.py
Base64 encoder/decoder with verbose step-by-step operations.
"""
import base64
from core.i18n import s

def encode_base64(text: str, lang: str = "fr") -> dict:
    steps = []
    try:
        raw_bytes = text.encode("utf-8")
        steps.append(s("b64_step1", lang, bytes=list(raw_bytes)))
        binary_parts = [format(b, "08b") for b in raw_bytes]
        steps.append(s("b64_step2", lang))
        steps.append("   " + " ".join(binary_parts))
        all_bits = "".join(binary_parts)
        padded = all_bits + "0" * ((6 - len(all_bits) % 6) % 6)
        chunks_6 = [padded[i:i+6] for i in range(0, len(padded), 6)]
        steps.append(s("b64_step3", lang, chunks=chunks_6))
        indices = [int(c, 2) for c in chunks_6]
        steps.append(s("b64_step4", lang, indices=indices))
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        chars = [alphabet[i] for i in indices]
        steps.append(s("b64_step5", lang, chars="".join(chars)))
        encoded = base64.b64encode(raw_bytes).decode("utf-8")
        steps.append(s("b64_step6", lang, encoded=encoded))
        return {"input": text, "encoded": encoded, "steps": steps,
                "byte_count": len(raw_bytes), "output_length": len(encoded)}
    except Exception as e:
        return {"error": str(e), "steps": steps}

def decode_base64(b64_text: str, lang: str = "fr") -> dict:
    steps = []
    try:
        b64_clean = b64_text.strip()
        steps.append(s("b64d_step1", lang, input=b64_clean))
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        chars_no_pad = b64_clean.rstrip("=")
        indices = [alphabet.index(c) for c in chars_no_pad if c in alphabet]
        steps.append(s("b64d_step2", lang, indices=indices))
        bits = "".join(format(i, "06b") for i in indices)
        steps.append(s("b64d_step3", lang, bits=bits[:48] + ("..." if len(bits) > 48 else "")))
        n_bytes = len(chars_no_pad) * 6 // 8
        byte_bits = [bits[i:i+8] for i in range(0, n_bytes * 8, 8)]
        byte_values = [int(b, 2) for b in byte_bits]
        steps.append(s("b64d_step4", lang, bytes=byte_values))
        decoded = base64.b64decode(b64_clean).decode("utf-8")
        steps.append(s("b64d_step5", lang, decoded=decoded))
        return {"input": b64_text, "decoded": decoded, "steps": steps}
    except UnicodeDecodeError:
        return {"error": s("b64_utf8_error", lang), "steps": steps}
    except Exception as e:
        return {"error": str(e), "steps": steps}
