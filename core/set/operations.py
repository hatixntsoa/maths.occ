"""
core/operations.py
══════════════════════════════════════════════════════════════════
Algèbre & Théorie des Ensembles — toutes les opérations

PLAN DU FICHIER :
  0. Utilitaires de parsing     (parse_input)
  1. Opérations de base          (union, intersection, différence...)
  2. Opérations avancées         (complémentaire, ensemble des parties)
  3. Ensemble par compréhension  (build_set_by_comprehension)
  4. Applications  f : A → B     (build_function, image, injectivité...)
══════════════════════════════════════════════════════════════════
"""


# ══════════════════════════════════════════════════════════════
#  0. UTILITAIRES
# ══════════════════════════════════════════════════════════════

def parse_input(raw_str: str) -> set:
    """
    Parse input by trying int first, falling back to strings.
    
    Splits by whitespace and attempts to convert each element to int.
    If an element can't be converted to int, treats all elements as strings.
    
    Examples:
        "1 2 3"     → {1, 2, 3}  (integers)
        "a b c"     → {'a', 'b', 'c'}  (strings)
        "1 a 3"     → {'1', 'a', '3'}  (mixed → all strings)
    """
    elements = raw_str.split()
    if not elements:
        return set()
    
    try:
        return set(map(int, elements))
    except ValueError:
        return set(elements)


# ══════════════════════════════════════════════════════════════
#  1. OPÉRATIONS DE BASE
# ══════════════════════════════════════════════════════════════
#
#  Rappel théorique :
#    Un ensemble est une collection d'éléments DISTINCTS et SANS ORDRE.
#    {1, 2, 3} == {3, 1, 2}  → vrai en mathématiques ET en Python.
#
#  En Python, le type `set` représente exactement un ensemble mathématique.


def union(A: set, B: set) -> set:
    """
    A ∪ B = { x | x ∈ A  OU  x ∈ B }

    Tous les éléments qui sont dans A, dans B, ou dans les deux.
    Exemple : {1,2,3} ∪ {3,4,5} = {1,2,3,4,5}
    """
    return A | B


def intersection(A: set, B: set) -> set:
    """
    A ∩ B = { x | x ∈ A  ET  x ∈ B }

    Seulement les éléments communs aux deux ensembles.
    Exemple : {1,2,3} ∩ {3,4,5} = {3}
    """
    return A & B


def difference(A: set, B: set) -> set:
    """
    A \\ B = { x | x ∈ A  ET  x ∉ B }

    Les éléments de A qui ne sont PAS dans B.
    Exemple : {1,2,3} \\ {3,4,5} = {1,2}

    ⚠️  La différence n'est PAS commutative : A\\B ≠ B\\A en général.
    """
    return A - B


def symmetric_difference(A: set, B: set) -> set:
    """
    A △ B = (A \\ B) ∪ (B \\ A)

    Les éléments qui sont dans l'un OU l'autre, mais PAS dans les deux.
    Équivalent à : (A ∪ B) \\ (A ∩ B)
    Exemple : {1,2,3} △ {3,4,5} = {1,2,4,5}
    """
    return A ^ B


def cartesian_product(A: set, B: set) -> set:
    """
    A × B = { (a, b) | a ∈ A  et  b ∈ B }

    L'ensemble de TOUTES les paires ordonnées (a, b).
    |A × B| = |A| × |B|
    Exemple : {1,2} × {a,b} = {(1,a), (1,b), (2,a), (2,b)}

    Note : (a, b) ≠ (b, a)  → l'ordre dans la paire compte !
    """
    return {(a, b) for a in A for b in B}


def cardinality(A: set) -> int:
    """
    |A| = nombre d'éléments de A

    Exemples :
      |{1, 2, 3}| = 3
      |{}|        = 0   (ensemble vide)
    """
    return len(A)


# ══════════════════════════════════════════════════════════════
#  2. OPÉRATIONS AVANCÉES
# ══════════════════════════════════════════════════════════════


def complement(A: set, E: set) -> set:
    """
    Ā = E \\ A   (complémentaire de A dans l'univers E)

    Condition nécessaire : A ⊆ E
    C'est l'ensemble de tout ce qui est dans E mais PAS dans A.

    Exemple : E = {1..10}, A = {2,4,6,8,10}
              Ā = {1,3,5,7,9}
    """
    if not A.issubset(E):
        raise ValueError(
            f"A n'est pas un sous-ensemble de E.\nÉléments hors de E : {sorted(A - E)}"
        )
    return E - A


def is_subset(A: set, B: set) -> bool:
    """
    A ⊆ B  ⟺  tout élément de A est aussi dans B.
    Équivalent à : A ∩ B == A
    """
    return A.issubset(B)


def is_disjoint(A: set, B: set) -> bool:
    """
    A et B sont disjoints  ⟺  A ∩ B = ∅
    Il n'y a aucun élément commun.
    """
    return A.isdisjoint(B)


def power_set(A: set) -> list:
    """
    P(A) = ensemble de tous les sous-ensembles de A.

    Propriété fondamentale : |P(A)| = 2^|A|
    Exemple : P({1,2}) = { ∅, {1}, {2}, {1,2} }  → 4 = 2² sous-ensembles.

    Retourne une liste de frozenset (sets non-mutables, hashables).
    ⚠️  Attention : si |A| est grand (> 20), P(A) devient énorme !
    """
    if len(A) > 20:
        raise ValueError(
            f"|A| = {len(A)} → P(A) aurait 2^{len(A)} = {2 ** len(A):,} éléments. "
            "Trop grand pour être calculé."
        )
    from itertools import combinations

    A_list = list(A)
    result = []
    for r in range(len(A_list) + 1):
        for combo in combinations(A_list, r):
            result.append(frozenset(combo))
    return result


# ══════════════════════════════════════════════════════════════
#  3. ENSEMBLE PAR COMPRÉHENSION
# ══════════════════════════════════════════════════════════════
#
#  Rappel théorique :
#    A = { x ∈ E | P(x) }
#
#  Algorithme :
#    POUR CHAQUE x dans E :
#        SI P(x) est vrai → ajouter x dans A
#
#  En Python, on peut écrire la même chose en une ligne :
#    A = {x for x in E if P(x)}
#  C'est ce qu'on appelle une "compréhension d'ensemble" — inspirée
#  directement de la notation mathématique !


def build_universe(start: int, end: int) -> set:
    """
    Crée l'univers E = { start, start+1, ..., end }

    On travaille dans un sous-ensemble fini de ℤ.
    Exemple : build_universe(-5, 5) → {-5,-4,-3,-2,-1,0,1,2,3,4,5}
    """
    if start > end:
        raise ValueError(f"Le début ({start}) doit être ≤ la fin ({end}).")
    return set(range(start, end + 1))


def build_set_by_comprehension(universe: set, predicate_str: str) -> set:
    """
    Construit A = { x ∈ universe | P(x) }

    predicate_str : expression Python valide en fonction de 'x'.
    Exemples :
        "x % 2 == 0"           → entiers pairs
        "x > 3 and x < 10"    → entiers dans ]3 ; 10[
        "x ** 2 < 50"          → x² < 50
        "x % 3 == 0"           → multiples de 3

    Sécurité : eval() est restreint — seules les opérations
    arithmétiques et logiques de base sont autorisées.
    Les fonctions dangereuses (import, open, etc.) sont bloquées.
    """
    # Fonctions mathématiques autorisées dans le prédicat
    safe_context = {
        "__builtins__": {},  # bloque toutes les fonctions Python dangereuses
        "abs": abs,
        "pow": pow,
        "min": min,
        "max": max,
    }

    result = set()
    for x in universe:
        safe_context["x"] = x
        try:
            if eval(predicate_str, safe_context):
                result.add(x)
        except Exception:
            raise ValueError(
                f"Prédicat invalide : '{predicate_str}'\n"
                "Vérifie la syntaxe. Exemple valide : x % 2 == 0"
            )
    return result


# ══════════════════════════════════════════════════════════════
#  4. APPLICATIONS  f : A → B
# ══════════════════════════════════════════════════════════════
#
#  Rappel théorique :
#    Une APPLICATION (ou fonction) f : A → B associe à CHAQUE
#    élément x ∈ A exactement UN élément f(x) ∈ B.
#
#    • A = domaine     (ensemble de départ)
#    • B = codomaine   (ensemble d'arrivée déclaré)
#    • f(A) = image    (sous-ensemble de B effectivement atteint)
#
#  On représente f en Python par un dictionnaire :
#    f = { x: f(x)  pour chaque x dans A }
#  Exemple : f = {1: 1, 2: 4, 3: 9}  pour f(x) = x²


def build_function(A: set, formula_str: str) -> dict:
    """
    Construit f : A → ℤ définie par une formule.

    formula_str : expression Python en 'x'.
    Exemples :
        "x ** 2"        → f(x) = x²
        "2 * x + 1"     → f(x) = 2x + 1
        "x % 3"         → f(x) = x mod 3
        "abs(x)"        → f(x) = |x|

    Retourne un dict { x: f(x) } pour x dans A.
    """
    safe_context = {
        "__builtins__": {},
        "abs": abs,
        "pow": pow,
        "min": min,
        "max": max,
    }

    f = {}
    for x in sorted(A):
        safe_context["x"] = x
        try:
            f[x] = eval(formula_str, safe_context)
        except Exception:
            raise ValueError(
                f"Formule invalide : '{formula_str}'\nExemple valide : x ** 2"
            )
    return f


def image_directe(f: dict, subset: set) -> set:
    """
    Image directe de S par f :
        f(S) = { f(x) | x ∈ S }

    On "envoie" chaque élément de S par f et on collecte les résultats.
    Propriété : f(S) ⊆ B  (l'image est toujours dans le codomaine)

    Exemple : f(x)=x², S={1,2,3}  →  f(S) = {1,4,9}
    """
    domain = set(f.keys())
    if not subset.issubset(domain):
        hors = sorted(subset - domain)
        raise ValueError(f"Ces éléments ne sont pas dans le domaine de f : {hors}")
    return {f[x] for x in subset}


def image_inverse(f: dict, subset: set) -> set:
    """
    Image inverse (préimage) de T par f :
        f⁻¹(T) = { x ∈ A | f(x) ∈ T }

    On cherche TOUS les antécédents des éléments de T.

    ⚠️  Important :
      f⁻¹ ici est un ENSEMBLE, pas forcément une fonction.
      Un élément de T peut avoir 0, 1 ou plusieurs antécédents.
      f⁻¹ est une vraie fonction seulement si f est bijective.

    Exemple : f(x)=x², T={4}  →  f⁻¹({4}) = {-2, 2}  (deux antécédents !)
    """
    return {x for x, y in f.items() if y in subset}


def is_injective(f: dict) -> tuple[bool, str]:
    """
    f est injective  ⟺  f(x₁) = f(x₂)  ⟹  x₁ = x₂

    Test algorithmique :
      Si toutes les valeurs de f sont distinctes → injective.
      Équivalent à : |f(A)| == |A|

    Explication intuitive :
      Pas deux éléments différents ne peuvent avoir la même image.
      Chaque valeur de B est atteinte AU PLUS une fois.
    """
    values = list(f.values())
    unique_values = set(values)

    if len(unique_values) == len(values):
        return True, "✅ Injective : aucune collision, chaque f(x) est unique."

    # Trouver les collisions pour expliquer pourquoi
    seen = {}
    collisions = []
    for x, y in f.items():
        if y in seen:
            collisions.append(f"f({seen[y]}) = f({x}) = {y}")
        else:
            seen[y] = x

    msg = "❌ Non injective — collisions : " + ", ".join(collisions[:3])
    if len(collisions) > 3:
        msg += f" (et {len(collisions) - 3} autre(s))"
    return False, msg


def is_surjective(f: dict, B: set) -> tuple[bool, str]:
    """
    f : A → B est surjective  ⟺  f(A) = B

    Test algorithmique :
      Calculer l'image f(A) = ensemble de toutes les valeurs prises par f.
      Si f(A) == B → surjective.

    Explication intuitive :
      Tout élément de B est atteint par au moins un élément de A.
      Aucun "trou" dans B.
    """
    image = set(f.values())
    missing = B - image

    if not missing:
        return True, "✅ Surjective : tout élément de B a au moins un antécédent."

    return (
        False,
        f"❌ Non surjective — éléments de B sans antécédent : {sorted(missing)}",
    )


def is_bijective(f: dict, B: set) -> tuple[bool, str]:
    """
    f est bijective  ⟺  injective  ET  surjective

    Conséquence importante : si f est bijective, alors |A| = |B|.
    Une bijection établit une "correspondance parfaite 1-1" entre A et B.

    Si f est bijective, alors f⁻¹ est aussi une vraie fonction f⁻¹ : B → A.
    """
    inj, msg_inj = is_injective(f)
    sur, msg_sur = is_surjective(f, B)

    if inj and sur:
        return True, "✅ Bijective : correspondance parfaite 1-1 entre A et B."

    parts = []
    if not inj:
        parts.append(msg_inj)
    if not sur:
        parts.append(msg_sur)
    return False, "\n".join(parts)
