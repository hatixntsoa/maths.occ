"""
ui/app.py  —  Flask web server
Replaces the Textual TUI. Same 5-tab logic, served over HTTP.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, render_template, request, jsonify

from core.set.operations import (
    union, intersection, difference, symmetric_difference,
    cartesian_product, cardinality,
    build_set_by_comprehension, build_universe,
    build_function, image_directe, image_inverse,
    is_injective, is_surjective, is_bijective,
    parse_input,
)
from storage.json_store import (
    load, save, add_entry, get_history, clear_history,
    save_named_set, load_named_set, delete_named_set, list_named_sets,
)
from core.relations.order import ORDER_RELATIONS, format_order_relation, list_order_relations
from core.relations.equivalence import EQUIVALENCE_RELATIONS, format_equivalence_relation, list_equivalence_relations, check_modulo
from core.prime.checker import check_prime_verbose, get_factors
from core.prime.range_checker import primes_in_range
from core.cryptography.base64_cipher import encode_base64, decode_base64
from core.cryptography.caesar_cipher import caesar_encode, caesar_decode, brute_force_caesar
from core.cryptography.rsa_cipher import rsa_generate_keys, rsa_encrypt, rsa_decrypt, rsa_encrypt_with_keys

DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data.json"))

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
app = Flask(__name__, template_folder=TEMPLATE_DIR)

import storage.json_store as _js

def _load():
    orig = _js.FILE; _js.FILE = DATA_FILE
    d = load(); _js.FILE = orig; return d

def _save(data):
    orig = _js.FILE; _js.FILE = DATA_FILE
    save(data); _js.FILE = orig


@app.route("/")
def index():
    return render_template("index.html")


# ── Tab 1: Operations ─────────────────────────────────────────
@app.route("/api/ops", methods=["POST"])
def api_ops():
    body  = request.get_json()
    op    = body.get("op")
    raw_a = (body.get("A") or "").strip()
    raw_b = (body.get("B") or "").strip()
    if not raw_a:
        return jsonify({"error": "L'ensemble A est vide."}), 400
    try:
        A = parse_input(raw_a)
        B = parse_input(raw_b) if raw_b else set()
        b_used = B

        if   op == "union":         res = union(A, B)
        elif op == "intersection":  res = intersection(A, B)
        elif op == "difference":    res = difference(A, B)
        elif op == "symdiff":       res = symmetric_difference(A, B)
        elif op == "product":       res = cartesian_product(A, B)
        elif op == "cardinality":   res = cardinality(A); b_used = None
        else: return jsonify({"error": "Opération inconnue"}), 400

        if isinstance(res, set):
            sample = next(iter(res), None)
            if isinstance(sample, tuple):
                res_serial = [list(p) for p in sorted(res)]
                res_str = "{ " + ", ".join(f"({a}, {b})" for a,b in sorted(res)) + " }"
            else:
                res_serial = sorted(res)
                res_str = "{ " + ", ".join(map(str, sorted(res))) + " }"
        else:
            res_serial = res
            res_str = str(res)

        data = _load()
        add_entry(data, op, A, b_used, res)
        _save(data)

        return jsonify({
            "A": sorted(A), "B": sorted(B) if b_used is not None else None,
            "op": op, "result": res_serial, "result_str": res_str,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ── Tab 2: Comprehension ──────────────────────────────────────
@app.route("/api/comprehension", methods=["POST"])
def api_comp():
    body = request.get_json()
    try:
        start = int(body.get("start", 0))
        end   = int(body.get("end", 0))
        pred  = (body.get("predicate") or "").strip()
        if not pred: return jsonify({"error": "Le prédicat est vide."}), 400
        if start > end: return jsonify({"error": "Le début doit être ≤ la fin."}), 400
        E = build_universe(start, end)
        A = build_set_by_comprehension(E, pred)
        return jsonify({
            "start": start, "end": end, "universe_size": len(E),
            "predicate": pred, "result": sorted(A), "cardinality": len(A),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ── Tab 3: Applications ───────────────────────────────────────
@app.route("/api/function", methods=["POST"])
def api_function():
    body = request.get_json()
    try:
        A       = parse_input((body.get("A") or ""))
        B       = parse_input((body.get("B") or ""))
        formula = (body.get("formula") or "").strip()
        raw_s   = (body.get("S") or "").strip()
        raw_t   = (body.get("T") or "").strip()
        if not A:       return jsonify({"error": "Le domaine A est vide."}), 400
        if not formula: return jsonify({"error": "La formule est vide."}), 400
        S = parse_input(raw_s) if raw_s else A
        T = parse_input(raw_t) if raw_t else B
        f        = build_function(A, formula)
        img_dir  = image_directe(f, S)
        img_inv  = image_inverse(f, T)
        _, msg_inj = is_injective(f)
        _, msg_sur = is_surjective(f, B)
        _, msg_bij = is_bijective(f, B)
        return jsonify({
            "formula": formula,
            "f_table": [{"x": x, "fx": y} for x, y in sorted(f.items())],
            "S": sorted(S), "image_directe": sorted(img_dir),
            "T": sorted(T), "image_inverse": sorted(img_inv),
            "injective": msg_inj, "surjective": msg_sur, "bijective": msg_bij,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ── Tab 4: Saved sets ─────────────────────────────────────────
@app.route("/api/sets", methods=["GET"])
def api_sets_list():
    data = _load()
    return jsonify([
        {"name": n, "elements": data["sets"][n], "cardinality": len(data["sets"][n])}
        for n in list_named_sets(data)
    ])

@app.route("/api/sets/save", methods=["POST"])
def api_sets_save():
    body = request.get_json()
    name = (body.get("name") or "").strip()
    raw  = (body.get("elements") or "").strip()
    if not name: return jsonify({"error": "Donne un nom à l'ensemble."}), 400
    if not raw:  return jsonify({"error": "L'ensemble est vide."}), 400
    try:
        elems = parse_input(raw); data = _load()
        save_named_set(data, name, elems); _save(data)
        return jsonify({"ok": True, "name": name, "elements": sorted(elems)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/sets/delete", methods=["POST"])
def api_sets_delete():
    name = (request.get_json().get("name") or "").strip()
    if not name: return jsonify({"error": "Nom manquant."}), 400
    data = _load(); delete_named_set(data, name); _save(data)
    return jsonify({"ok": True})

@app.route("/api/sets/load", methods=["POST"])
def api_sets_load():
    name = (request.get_json().get("name") or "").strip()
    if not name: return jsonify({"error": "Nom manquant."}), 400
    try:
        data = _load(); elems = load_named_set(data, name)
        return jsonify({"name": name, "elements": sorted(elems)})
    except KeyError as e:
        return jsonify({"error": str(e)}), 404


# ── Tab 5: History ────────────────────────────────────────────
@app.route("/api/history", methods=["GET"])
def api_history():
    data = _load()
    return jsonify(list(reversed(get_history(data))))

@app.route("/api/history/clear", methods=["POST"])
def api_history_clear():
    data = _load(); clear_history(data); _save(data)
    return jsonify({"ok": True})


def create_app():
    return app


# ── Tab 6: Relations ─────────────────────────────────────────
@app.route("/api/relations/order", methods=["POST"])
def api_relations_order():
    return jsonify({k: {
        "name": v["name"], "symbol": v["symbol"], "domain": v["domain"],
        "conditions": v["conditions"], "is_total": v["is_total"],
        "total_note": v["total_note"], "examples": v["examples"],
    } for k, v in ORDER_RELATIONS.items()})

@app.route("/api/relations/equivalence", methods=["POST"])
def api_relations_equivalence():
    return jsonify({k: {
        "name": v["name"], "symbol": v["symbol"], "domain": v["domain"],
        "conditions": v["conditions"], "classes": v["classes"], "examples": v["examples"],
    } for k, v in EQUIVALENCE_RELATIONS.items()})

@app.route("/api/relations/modulo", methods=["POST"])
def api_relations_modulo():
    body = request.get_json()
    try:
        a = int(body.get("a", 0))
        b = int(body.get("b", 0))
        n = int(body.get("n", 2))
        lang = body.get("lang", "fr")
        if n < 2:
            msg = "n doit être >= 2" if lang == "fr" else "n must be >= 2"
            return jsonify({"error": msg}), 400
        return jsonify(check_modulo(a, b, n, lang=lang))
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ── Tab 7: Prime Numbers ──────────────────────────────────────
@app.route("/api/prime/check", methods=["POST"])
def api_prime_check():
    body = request.get_json()
    try:
        n = int(body.get("n", 0))
        lang = body.get("lang", "fr")
        result = check_prime_verbose(n, lang=lang)
        factors = get_factors(n) if n >= 2 and not result["is_prime"] else []
        result["factors"] = [{"prime": p, "exp": e} for p, e in factors]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/prime/range", methods=["POST"])
def api_prime_range():
    body = request.get_json()
    try:
        a = int(body.get("a", 2))
        b = int(body.get("b", 50))
        verbose = body.get("verbose", False)
        lang = body.get("lang", "fr")
        result = primes_in_range(a, b, lang=lang)
        if "error" in result:
            return jsonify(result), 400
        if not verbose:
            for r in result.get("results", []):
                r.pop("steps", None)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ── Tab 8: Cryptography ───────────────────────────────────────
@app.route("/api/crypto/base64", methods=["POST"])
def api_crypto_base64():
    body = request.get_json()
    mode = body.get("mode", "encode")
    text = body.get("text", "")
    
    if not text:
        return jsonify({"error": "Texte vide."}), 400
    try:
        lang = body.get("lang", "fr")
        if mode == "encode":
            return jsonify(encode_base64(text, lang=lang))
        else:
            return jsonify(decode_base64(text, lang=lang))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/crypto/caesar", methods=["POST"])
def api_crypto_caesar():
    body = request.get_json()
    mode = body.get("mode", "encode")
    text = body.get("text", "")
    shift = body.get("shift", 3)
    brute = body.get("brute_force", False)

    if not text:
        return jsonify({"error": "Texte vide."}), 400
    try:
        lang = body.get("lang", "fr")
        shift = int(shift)
        if brute:
            return jsonify({"results": brute_force_caesar(text, lang)})
        if mode == "encode":
            return jsonify(caesar_encode(text, shift, lang=lang))
        else:
            return jsonify(caesar_decode(text, shift, lang=lang))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/crypto/rsa/generate", methods=["POST"])
def api_crypto_rsa_generate():
    body = request.get_json()
    bits = int(body.get("bits", 64))
    if bits < 16: bits = 16
    if bits > 256: bits = 256
    try:
        return jsonify(rsa_generate_keys(bits))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/crypto/rsa/encrypt", methods=["POST"])
def api_crypto_rsa_encrypt():
    body = request.get_json()
    message = body.get("message", "")
    if not message:
        return jsonify({"error": "Message vide."}), 400
    try:
        p = int(body.get("p", 0) or 0)
        q = int(body.get("q", 0) or 0)
        if p and q:
            return jsonify(rsa_encrypt_with_keys(message, p, q))
        e_val = int(body.get("e", 65537) or 65537)
        n_val = int(body.get("n", 0) or 0)
        if not n_val:
            return jsonify({"error": "Fournir p et q, ou e et n."}), 400
        return jsonify(rsa_encrypt(message, e_val, n_val))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/crypto/rsa/decrypt", methods=["POST"])
def api_crypto_rsa_decrypt():
    body = request.get_json()
    try:
        c = int(body.get("ciphertext", 0) or 0)
        d_val = int(body.get("d", 0) or 0)
        n_val = int(body.get("n", 0) or 0)
        if not (c and d_val and n_val):
            return jsonify({"error": "c, d et n sont requis."}), 400
        return jsonify(rsa_decrypt(c, d_val, n_val))
    except Exception as e:
        return jsonify({"error": str(e)}), 400
