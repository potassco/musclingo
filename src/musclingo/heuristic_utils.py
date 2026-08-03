"""
Helpers to bias the solver's domain heuristic towards or away from a set of atoms.
"""

from collections.abc import Sequence

import clingo


def heuristic_type(bias: bool) -> clingo.HeuristicType:
    """
    Return the `True_` heuristic type if `bias` is set, otherwise `False_`.
    """
    return clingo.HeuristicType.True_ if bias else clingo.HeuristicType.False_


def set_heuristic(ctl: clingo.Control, atoms: Sequence[int], bias: bool) -> None:
    """
    Add a sign heuristic on every atom in `atoms`.

    The solver then prefers to include them when `bias` is set and to exclude
    them otherwise.
    """
    h = heuristic_type(bias)
    with ctl.backend() as b:
        for lit in atoms:
            b.add_heuristic(lit, h, 1, 1, [])
