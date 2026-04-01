"""
core/relations/equivalence.py
Relations d'équivalence — definitions, conditions, proofs, full catalogue.
"""
from core.i18n import s

EQUIVALENCE_RELATIONS = {
    "equality": {
        "name": "Égalité (=)",
        "symbol": "=",
        "domain": "Tout ensemble E",
        "conditions": {
            "reflexivite": {
                "label": "Réflexivité",
                "statement": "∀ a ∈ E, a = a",
                "proof": "L'égalité est définie de sorte que a = a toujours. ✓",
            },
            "symetrie": {
                "label": "Symétrie",
                "statement": "∀ a, b ∈ E, a = b ⟹ b = a",
                "proof": "Par définition de l'égalité, si a et b désignent la même chose, b = a. ✓",
            },
            "transitivite": {
                "label": "Transitivité",
                "statement": "∀ a, b, c ∈ E, (a = b ∧ b = c) ⟹ a = c",
                "proof": "Si a et b sont identiques, et b et c sont identiques, alors a et c le sont. ✓",
            },
        },
        "classes": "Chaque classe d'équivalence est un singleton {a}.",
        "examples": ["2 = 2", "π = π"],
    },
    "modulo": {
        "name": "Congruence modulo n (≡ mod n)",
        "symbol": "≡ (mod n)",
        "domain": "ℤ, pour un entier n ≥ 2 fixé",
        "conditions": {
            "reflexivite": {
                "label": "Réflexivité",
                "statement": "∀ a ∈ ℤ, a ≡ a (mod n)",
                "proof": "a - a = 0 = 0 × n, donc n | (a - a). ✓",
            },
            "symetrie": {
                "label": "Symétrie",
                "statement": "∀ a, b ∈ ℤ, a ≡ b (mod n) ⟹ b ≡ a (mod n)",
                "proof": "n | (a - b) ⟹ n | (-(a - b)) = b - a. ✓",
            },
            "transitivite": {
                "label": "Transitivité",
                "statement": "∀ a, b, c ∈ ℤ, (a ≡ b ∧ b ≡ c) ⟹ a ≡ c (mod n)",
                "proof": "a - b = k₁n et b - c = k₂n ⟹ a - c = (k₁+k₂)n, donc n | (a-c). ✓",
            },
        },
        "classes": "Les classes d'équivalence sont {0̄, 1̄, …, n̄-1} = ℤ/nℤ.",
        "examples": ["7 ≡ 1 (mod 3)", "10 ≡ 0 (mod 5)", "−1 ≡ 2 (mod 3)"],
    },
    "same_parity": {
        "name": "Même parité",
        "symbol": "~_pair",
        "domain": "ℤ",
        "conditions": {
            "reflexivite": {
                "label": "Réflexivité",
                "statement": "∀ a ∈ ℤ, a a la même parité que a",
                "proof": "Trivial : a et a ont exactement la même parité. ✓",
            },
            "symetrie": {
                "label": "Symétrie",
                "statement": "∀ a, b ∈ ℤ, a ~ b ⟹ b ~ a",
                "proof": "Si a et b ont même parité, alors b et a ont même parité. ✓",
            },
            "transitivite": {
                "label": "Transitivité",
                "statement": "∀ a, b, c ∈ ℤ, (a ~ b ∧ b ~ c) ⟹ a ~ c",
                "proof": "Si a ≡ b (mod 2) et b ≡ c (mod 2), alors a ≡ c (mod 2). ✓",
            },
        },
        "classes": "Deux classes : pairs {…,−2, 0, 2,…} et impairs {…,−1, 1, 3,…}.",
        "examples": ["2 ~ 4 (même parité)", "3 ~ 7 (tous deux impairs)"],
    },
    "same_sign": {
        "name": "Même signe (sur ℝ*)",
        "symbol": "~_sgn",
        "domain": "ℝ* (réels non nuls)",
        "conditions": {
            "reflexivite": {
                "label": "Réflexivité",
                "statement": "∀ a ∈ ℝ*, a a le même signe que a",
                "proof": "Évident. ✓",
            },
            "symetrie": {
                "label": "Symétrie",
                "statement": "a ~ b ⟹ b ~ a",
                "proof": "Si a et b ont même signe, b et a aussi. ✓",
            },
            "transitivite": {
                "label": "Transitivité",
                "statement": "(a ~ b ∧ b ~ c) ⟹ a ~ c",
                "proof": "Si a, b même signe et b, c même signe ⟹ a, c même signe. ✓",
            },
        },
        "classes": "Deux classes : ℝ₋* (négatifs) et ℝ₊* (positifs).",
        "examples": ["3 ~ 7 (positifs)", "−2 ~ −5 (négatifs)"],
    },
    "parallel_lines": {
        "name": "Parallélisme de droites du plan",
        "symbol": "∥",
        "domain": "Ensemble des droites du plan euclidien",
        "conditions": {
            "reflexivite": {
                "label": "Réflexivité",
                "statement": "∀ droite d, d ∥ d",
                "proof": "Une droite est parallèle à elle-même (convention). ✓",
            },
            "symetrie": {
                "label": "Symétrie",
                "statement": "d₁ ∥ d₂ ⟹ d₂ ∥ d₁",
                "proof": "Le parallélisme est une propriété symétrique. ✓",
            },
            "transitivite": {
                "label": "Transitivité",
                "statement": "(d₁ ∥ d₂ ∧ d₂ ∥ d₃) ⟹ d₁ ∥ d₃",
                "proof": "Si d₁ et d₂ ont même direction, et d₂ et d₃ aussi, alors d₁ et d₃ aussi. ✓",
            },
        },
        "classes": "Les classes sont les faisceaux de droites de même direction (même vecteur directeur).",
        "examples": ["Deux droites horizontales", "Deux droites verticales"],
    },
    "equipotent": {
        "name": "Équipotence (même cardinal)",
        "symbol": "~",
        "domain": "Ensemble de tous les ensembles",
        "conditions": {
            "reflexivite": {
                "label": "Réflexivité",
                "statement": "∀ A, A ~ A",
                "proof": "La fonction identité id_A : A → A est une bijection. ✓",
            },
            "symetrie": {
                "label": "Symétrie",
                "statement": "A ~ B ⟹ B ~ A",
                "proof": "Si f : A → B est une bijection, f⁻¹ : B → A l'est aussi. ✓",
            },
            "transitivite": {
                "label": "Transitivité",
                "statement": "(A ~ B ∧ B ~ C) ⟹ A ~ C",
                "proof": "Si f : A→B et g : B→C sont des bijections, g∘f : A→C l'est aussi. ✓",
            },
        },
        "classes": "Les classes sont les cardinaux : |A| = 0, 1, 2, …, ℵ₀, …",
        "examples": ["{1,2,3} ~ {a,b,c}", "ℤ ~ ℕ (Cantor)"],
    },
}


def get_equivalence_relation(key: str) -> dict:
    return EQUIVALENCE_RELATIONS.get(key, {})


def list_equivalence_relations() -> list:
    return list(EQUIVALENCE_RELATIONS.keys())


def check_modulo(a: int, b: int, n: int, lang: str = "fr") -> dict:
    diff = a - b
    remainder = diff % n
    is_congruent = remainder == 0
    verdict = s("modulo_congruent" if is_congruent else "modulo_not_congruent",
                lang, a=a, b=b, n=n, rem=remainder)
    return {
        "a": a, "b": b, "n": n, "diff": diff,
        "quotient": diff // n, "remainder": remainder,
        "is_congruent": is_congruent,
        "explanation": f"{a} - {b} = {diff} = {diff // n} × {n} + {remainder}\n{verdict}",
    }


def format_equivalence_relation(key: str) -> str:
    rel = EQUIVALENCE_RELATIONS.get(key)
    if not rel:
        return f"Relation '{key}' introuvable."
    lines = [
        f"=== {rel['name']} ===",
        f"Symbole  : {rel['symbol']}",
        f"Domaine  : {rel['domain']}",
        "",
        "── Conditions d'équivalence ──",
    ]
    for cond in rel["conditions"].values():
        lines += [
            f"  [{cond['label']}]",
            f"  {cond['statement']}",
            f"  Preuve : {cond['proof']}",
            "",
        ]
    lines.append(f"Classes d'équivalence : {rel['classes']}")
    lines.append(f"Exemples : {', '.join(rel['examples'])}")
    return "\n".join(lines)
