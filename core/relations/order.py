"""
core/relations/order.py
Relations d'ordre (Order relations) — definitions, conditions, proofs, examples.
"""

ORDER_RELATIONS = {
    "<=": {
        "name": "Inégalité large (≤) sur ℤ",
        "symbol": "≤",
        "domain": "ℤ (ou ℝ, ℕ)",
        "conditions": {
            "reflexivite": {
                "label": "Réflexivité",
                "statement": "∀ a ∈ ℤ, a ≤ a",
                "proof": "a - a = 0 ≥ 0, donc a ≤ a. ✓",
            },
            "antisymetrie": {
                "label": "Antisymétrie",
                "statement": "∀ a, b ∈ ℤ, (a ≤ b ∧ b ≤ a) ⟹ a = b",
                "proof": "a ≤ b ⟹ b - a ≥ 0. b ≤ a ⟹ a - b ≥ 0.\nDonc b - a = 0, soit a = b. ✓",
            },
            "transitivite": {
                "label": "Transitivité",
                "statement": "∀ a, b, c ∈ ℤ, (a ≤ b ∧ b ≤ c) ⟹ a ≤ c",
                "proof": "b - a ≥ 0 et c - b ≥ 0. Somme : c - a ≥ 0, donc a ≤ c. ✓",
            },
        },
        "is_total": True,
        "total_note": "∀ a, b ∈ ℤ, a ≤ b ou b ≤ a → ordre total.",
        "examples": ["1 ≤ 2", "3 ≤ 3", "−5 ≤ 0"],
    },
    "<": {
        "name": "Ordre strict (<) sur ℤ",
        "symbol": "<",
        "domain": "ℤ",
        "conditions": {
            "irreflexivite": {
                "label": "Irréflexivité",
                "statement": "∀ a ∈ ℤ, ¬(a < a)",
                "proof": "a - a = 0, pas strictement positif. ✓",
            },
            "asymetrie": {
                "label": "Asymétrie",
                "statement": "∀ a, b ∈ ℤ, a < b ⟹ ¬(b < a)",
                "proof": "b - a > 0 ⟹ a - b < 0, donc b ≮ a. ✓",
            },
            "transitivite": {
                "label": "Transitivité",
                "statement": "∀ a, b, c ∈ ℤ, (a < b ∧ b < c) ⟹ a < c",
                "proof": "b - a > 0 et c - b > 0. Somme : c - a > 0. ✓",
            },
        },
        "is_total": True,
        "total_note": "Ordre strict total (trichotomie : a < b, a = b, ou b < a).",
        "examples": ["1 < 2", "−3 < 0"],
    },
    "divides": {
        "name": "Divisibilité (|) sur ℕ*",
        "symbol": "|",
        "domain": "ℕ* (entiers strictement positifs)",
        "conditions": {
            "reflexivite": {
                "label": "Réflexivité",
                "statement": "∀ a ∈ ℕ*, a | a",
                "proof": "a = 1 × a, donc a divise a. ✓",
            },
            "antisymetrie": {
                "label": "Antisymétrie",
                "statement": "∀ a, b ∈ ℕ*, (a | b ∧ b | a) ⟹ a = b",
                "proof": "a | b ⟹ b = k₁a, b | a ⟹ a = k₂b.\nDonc a = k₁k₂a, k₁k₂ = 1, k₁ = k₂ = 1, a = b. ✓",
            },
            "transitivite": {
                "label": "Transitivité",
                "statement": "∀ a, b, c ∈ ℕ*, (a | b ∧ b | c) ⟹ a | c",
                "proof": "b = k₁a et c = k₂b ⟹ c = k₂k₁a, donc a | c. ✓",
            },
        },
        "is_total": False,
        "total_note": "Ordre PARTIEL : 2 et 3 ne sont pas comparables (2∤3 et 3∤2).",
        "examples": ["2 | 6", "3 | 9", "1 | n pour tout n"],
    },
    "subset": {
        "name": "Inclusion (⊆) sur 𝒫(E)",
        "symbol": "⊆",
        "domain": "𝒫(E) — ensemble des parties d'un ensemble E",
        "conditions": {
            "reflexivite": {
                "label": "Réflexivité",
                "statement": "∀ A ∈ 𝒫(E), A ⊆ A",
                "proof": "Tout élément de A est dans A. ✓",
            },
            "antisymetrie": {
                "label": "Antisymétrie",
                "statement": "∀ A, B ∈ 𝒫(E), (A ⊆ B ∧ B ⊆ A) ⟹ A = B",
                "proof": "A ⊆ B et B ⊆ A ⟹ même éléments ⟹ A = B (double inclusion). ✓",
            },
            "transitivite": {
                "label": "Transitivité",
                "statement": "∀ A, B, C ∈ 𝒫(E), (A ⊆ B ∧ B ⊆ C) ⟹ A ⊆ C",
                "proof": "x ∈ A ⟹ x ∈ B ⟹ x ∈ C. Donc A ⊆ C. ✓",
            },
        },
        "is_total": False,
        "total_note": "Ordre PARTIEL : {1} et {2} ne sont pas comparables si E = {1,2}.",
        "examples": ["{1} ⊆ {1,2}", "∅ ⊆ A pour tout A", "{1,2} ⊆ {1,2}"],
    },
}


def get_order_relation(key: str) -> dict:
    return ORDER_RELATIONS.get(key, {})


def list_order_relations() -> list:
    return list(ORDER_RELATIONS.keys())


def format_order_relation(key: str) -> str:
    rel = ORDER_RELATIONS.get(key)
    if not rel:
        return f"Relation '{key}' introuvable."
    lines = [
        f"=== {rel['name']} ===",
        f"Symbole  : {rel['symbol']}",
        f"Domaine  : {rel['domain']}",
        "",
        "── Conditions ──",
    ]
    for cond in rel["conditions"].values():
        lines += [
            f"  [{cond['label']}]",
            f"  {cond['statement']}",
            f"  Preuve : {cond['proof']}",
            "",
        ]
    lines.append(f"Ordre total ? {'✓ Oui' if rel['is_total'] else '✗ Non'} — {rel['total_note']}")
    lines.append(f"Exemples : {', '.join(rel['examples'])}")
    return "\n".join(lines)
