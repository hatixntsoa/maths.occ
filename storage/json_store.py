"""
storage/json_store.py
─────────────────────
Persistance des données dans data.json

Structure du fichier JSON :
{
    "sets": {
        "MonEnsemble": [1, 2, 3],   ← ensembles nommés par l'utilisateur
        "Pairs":       [2, 4, 6]
    },
    "history": [
        {
            "timestamp": "2026-03-18 14:00:00",
            "operation": "union",
            "operands":  { "A": [1,2,3], "B": [3,4,5] },
            "result":    [1, 2, 3, 4, 5]
        }
    ]
}
"""

import json
from datetime import datetime

FILE = "data.json"

# ── Structure par défaut si le fichier n'existe pas ──────────
DEFAULT = {"sets": {}, "history": []}


def load() -> dict:
    """
    Charge les données depuis data.json.
    Si le fichier n'existe pas ou est vide/corrompu → retourne la structure par défaut.
    """
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
            # S'assurer que les clés obligatoires existent
            data.setdefault("sets", {})
            data.setdefault("history", [])
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        # FileNotFoundError → premier lancement
        # JSONDecodeError   → fichier vide ou corrompu
        return {"sets": {}, "history": []}


def save(data: dict) -> None:
    """Écrit toutes les données dans data.json (indent=4 pour lisibilité)."""
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ── Ensembles nommés ─────────────────────────────────────────


def save_named_set(data: dict, name: str, elements: set) -> None:
    """
    Sauvegarde un ensemble sous un nom choisi par l'utilisateur.
    Exemple : save_named_set(data, "Pairs", {2, 4, 6, 8})
    → data["sets"]["Pairs"] = [2, 4, 6, 8]
    """
    data["sets"][name] = sorted(elements)  # sorted() → liste ordonnée, plus lisible


def load_named_set(data: dict, name: str) -> set:
    """
    Charge un ensemble nommé et le retourne comme set Python.
    Lève KeyError si le nom n'existe pas.
    """
    if name not in data["sets"]:
        raise KeyError(f"Ensemble '{name}' introuvable.")
    return set(data["sets"][name])


def delete_named_set(data: dict, name: str) -> None:
    """Supprime un ensemble nommé."""
    if name in data["sets"]:
        del data["sets"][name]


def list_named_sets(data: dict) -> list[str]:
    """Retourne la liste des noms d'ensembles sauvegardés."""
    return sorted(data["sets"].keys())


# ── Historique ───────────────────────────────────────────────


def add_entry(data: dict, operation: str, A: set, B: set | None, result) -> None:
    """
    Ajoute une entrée dans l'historique.
    Sérialise proprement les types Python → JSON :
      set d'entiers  → liste triée
      set de tuples  → liste de listes  (produit cartésien)
      int            → int              (cardinalité)
    """
    if isinstance(result, set):
        sample = next(iter(result), None)
        if isinstance(sample, tuple):
            serialized = [list(pair) for pair in sorted(result)]
        else:
            serialized = sorted(result)
    else:
        serialized = result

    data["history"].append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operation": operation,
            "operands": {
                "A": sorted(A),
                "B": sorted(B) if B is not None else None,
            },
            "result": serialized,
        }
    )


def get_history(data: dict) -> list:
    return data.get("history", [])


def clear_history(data: dict) -> None:
    data["history"] = []
