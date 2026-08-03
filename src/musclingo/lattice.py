from collections.abc import Sequence
from typing import Protocol

import clingo
from bidict import frozenbidict

from musclingo.heuristic_utils import set_heuristic


class Lattice(Protocol):
    universe: frozenset[int]

    def set_bias(self, bias: bool) -> None: ...

    def next_seed(self) -> tuple[int, ...] | None: ...

    def block_up(self, seed: Sequence[int]) -> None: ...

    def block_down(self, seed: Sequence[int]) -> None: ...

    def force_disjoint(self, seed: Sequence[int]) -> None: ...


class AssumptionsLattice:
    def __init__(self, universe: Sequence[int], bias: bool) -> None:
        self.universe = frozenset(universe)

        ctl = clingo.Control(["--heuristic=Domain"])
        ctl.add("#show X: sel(X).")

        lookup = {}
        with ctl.backend() as b:
            for u in universe:
                sel = clingo.Function("sel", [clingo.Number(u)])
                sel_lit = b.add_atom(sel)
                b.add_rule([sel_lit], [], choice=True)
                lookup[sel_lit] = u

        ctl.ground()

        self.ctl = ctl
        self.lookup = frozenbidict(lookup)
        self.disjoint_assumptions = []

        set_heuristic(self.ctl, list(self.lookup), bias)

    def set_bias(self, bias: bool) -> None:
        set_heuristic(self.ctl, list(self.lookup), bias)

    def next_seed(self) -> tuple[int, ...] | None:
        with self.ctl.solve(yield_=True, assumptions=self.disjoint_assumptions) as sh:
            model = sh.model()

            if model is not None:
                return tuple(x.number for x in model.symbols(terms=True))

        if len(self.disjoint_assumptions) == 0:
            return None

        self.disjoint_assumptions = []
        return self.next_seed()

    def block_up(self, seed: Sequence[int]) -> None:
        clause = [self.lookup.inv[x] for x in seed]
        with self.ctl.backend() as b:
            b.add_rule([], clause)

    def block_down(self, seed: Sequence[int]) -> None:
        clause = [-self.lookup.inv[c] for c in self.universe.difference(seed)]
        with self.ctl.backend() as b:
            b.add_rule([], clause)

    def force_disjoint(self, seed: Sequence[int]) -> None:
        lits = [self.lookup.inv[s] for s in seed]
        with self.ctl.backend() as b:
            e = b.add_atom()
            b.add_rule([e], [], choice=True)
            self.disjoint_assumptions.append(e)
            for lit in lits:
                b.add_rule([], [e, lit])
