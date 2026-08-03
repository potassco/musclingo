"""
The implicit hitting set (IHS) algorithm for MUS enumeration.
"""

from collections.abc import Iterator

import clingo

from musclingo.heuristic_utils import set_heuristic
from musclingo.hitting_set import HittingSet


class IHS:
    """
    Enumerate MUSes and MSSes by interleaving hitting set computation with solving.

    Each step takes a minimal hitting set of the MCSes found so far as a
    candidate. If the candidate is unsatisfiable it is a MUS and gets blocked;
    otherwise the model extends to an MSS whose complement is added as a new
    MCS to hit.
    """

    def __init__(self, ctl: clingo.Control, hitting_set: HittingSet) -> None:
        """
        Set up the solver with domain heuristics over the hitting set universe.
        """
        self.ctl = ctl
        self.ctl.configuration.solver.heuristic = "Domain"  # ty: ignore[invalid-assignment]
        set_heuristic(ctl, tuple(hitting_set.universe), True)

        self.mhs = hitting_set

    def __next__(self) -> tuple[str, tuple[int, ...]] | None:
        """
        Return the next `("mus", ...)` or `("mss", ...)` pair, or `None` once no candidate is left.
        """
        candidate = self.mhs.get_mhs()
        if candidate is None:
            return None

        with self.ctl.solve(assumptions=candidate, yield_=True) as sh:
            model = sh.model()
            if model is None:
                self.mhs.block_mhs(candidate)
                return ("mus", tuple(candidate))

            mss = tuple(x for x in self.mhs.universe if model.is_true(x))
            mcs = tuple(self.mhs.universe.difference(mss))
            self.mhs.add_set(mcs)
            return ("mss", mss)

    def __iter__(self) -> Iterator[tuple[str, tuple[int, ...]]]:
        """
        Yield labelled sets until the search space is exhausted.
        """
        while val := self.__next__():
            yield val
