"""
Enumerate the MUSes and MSSes of an unsatisfiable graph colouring instance.

Run with:

    uv run python docs/examples/example.py
"""

import clingo

from musclingo.algorithms import MARCO
from musclingo.lattice import AssumptionsLattice
from musclingo.shrink import LinearElimination

PROGRAM = """
edge(0,1). edge(0,2). edge(0,3). edge(1,2). edge(1,3). edge(2,3).
color(r; g; b).

{ graph_edge(X,Y) } :- edge(X,Y).

node(X;Y) :- graph_edge(X,Y).
{ assign(X,C): color(C) } = 1 :- node(X).
:- assign(X,C), assign(Y,C), graph_edge(X,Y).
"""


def main() -> None:
    ctl = clingo.Control()
    ctl.add(PROGRAM)
    ctl.ground()

    # The MUS universe: one assumption literal per soft atom.
    lookup = {a.literal: a.symbol for a in ctl.symbolic_atoms.by_signature("graph_edge", 2)}

    lattice = AssumptionsLattice(lookup, bias=True)
    strategy = LinearElimination(ctl)

    for kind, subset in MARCO(lattice, strategy):
        print(kind.upper(), " ".join(str(lookup[z]) for z in sorted(subset)))


if __name__ == "__main__":
    main()
