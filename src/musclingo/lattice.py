"""
Power set lattices over assumption literals, used to drive seed enumeration.
"""

from collections.abc import Sequence
from typing import Protocol

import clingo
from bidict import frozenbidict

from musclingo.heuristic_utils import set_heuristic


class Lattice(Protocol):
    """
    The power set lattice of a universe of literals, with explored regions blocked off.
    """

    universe: frozenset[int]

    def set_bias(self, bias: bool) -> None:
        """
        Prefer large seeds when `bias` is set, small ones otherwise.
        """
        ...

    def next_seed(self) -> tuple[int, ...] | None:
        """
        Return an unexplored subset of the universe, or `None` if none is left.
        """
        ...

    def block_up(self, seed: Sequence[int]) -> None:
        """
        Mark `seed` and all of its supersets as explored.
        """
        ...

    def block_down(self, seed: Sequence[int]) -> None:
        """
        Mark `seed` and all of its subsets as explored.
        """
        ...

    def force_disjoint(self, seed: Sequence[int]) -> None:
        """
        Temporarily restrict seeds to those disjoint from `seed`.
        """
        ...


class AssumptionsLattice:
    """
    A `Lattice` encoded as an ASP choice over one `sel/1` atom per universe literal.

    Blocking a region amounts to adding an integrity constraint to the internal
    control object, so the search space shrinks monotonically as seeds are consumed.
    """

    def __init__(self, universe: Sequence[int], bias: bool) -> None:
        """
        Build and ground the choice program over `universe` with the given seed size bias.
        """
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
        """
        Prefer large seeds when `bias` is set, small ones otherwise.
        """
        set_heuristic(self.ctl, list(self.lookup), bias)

    def next_seed(self) -> tuple[int, ...] | None:
        """
        Return an unexplored subset of the universe, or `None` if none is left.

        Any active disjointness restriction is dropped and the search retried
        once before reporting exhaustion.
        """
        with self.ctl.solve(yield_=True, assumptions=self.disjoint_assumptions) as sh:
            model = sh.model()

            if model is not None:
                return tuple(x.number for x in model.symbols(terms=True))

        if len(self.disjoint_assumptions) == 0:
            return None

        self.disjoint_assumptions = []
        return self.next_seed()

    def block_up(self, seed: Sequence[int]) -> None:
        """
        Mark `seed` and all of its supersets as explored.
        """
        clause = [self.lookup.inv[x] for x in seed]
        with self.ctl.backend() as b:
            b.add_rule([], clause)

    def block_down(self, seed: Sequence[int]) -> None:
        """
        Mark `seed` and all of its subsets as explored.
        """
        clause = [-self.lookup.inv[c] for c in self.universe.difference(seed)]
        with self.ctl.backend() as b:
            b.add_rule([], clause)

    def force_disjoint(self, seed: Sequence[int]) -> None:
        """
        Restrict subsequent seeds to those disjoint from `seed`.

        The restriction is guarded by a fresh assumption literal, so it stays in
        effect only until `next_seed()` runs out of disjoint candidates.
        """
        lits = [self.lookup.inv[s] for s in seed]
        with self.ctl.backend() as b:
            e = b.add_atom()
            b.add_rule([e], [], choice=True)
            self.disjoint_assumptions.append(e)
            for lit in lits:
                b.add_rule([], [e, lit])
