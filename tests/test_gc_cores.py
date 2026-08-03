from collections.abc import Mapping, Sequence
from pathlib import Path

import clingo

from musclingo.algorithms import MARCO
from musclingo.algorithms.checkers import check_maximal_satisfiable, check_minimal_unsatisfiable
from musclingo.lattice import AssumptionsLattice
from musclingo.shrink import LinearElimination


def fmt_literals(literals: Sequence[int], lookup: Mapping[int, clingo.Symbol]) -> str:
    return " ".join(str(lookup[z]) for z in literals)


def test_cores() -> None:
    program = Path(__file__).parent / "gc_cores.lp"

    ctl = clingo.Control()
    ctl.load(program.as_posix())
    ctl.ground()

    literals = []
    lookup = {}
    for symlit in ctl.symbolic_atoms.by_signature("graph_edge", 2):
        literals.append(symlit.literal)
        lookup[symlit.literal] = symlit.symbol

    literals = [symlit.literal for symlit in ctl.symbolic_atoms.by_signature("graph_edge", 2)]

    lattice = AssumptionsLattice(literals, bias=True)
    strategy = LinearElimination(ctl)

    m = MARCO(lattice, strategy)

    values = set(lookup)

    for type_, set_ in m:
        if type_ == "mus":
            # asserts internally
            check_minimal_unsatisfiable(ctl, list(set_))
        if type_ == "mss":
            mss = list(set_)
            # asserts internally
            check_maximal_satisfiable(ctl, mss, list(values.difference(mss)))
