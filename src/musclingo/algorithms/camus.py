"""
The CAMUS algorithm for MUS enumeration.
"""

from collections.abc import Iterator

import clingo

from musclingo.heuristic_utils import set_heuristic
from musclingo.hitting_set import HittingSet


class CAMUS:
    """
    Enumerate MUSes following the CAMUS two phase scheme.

    The first phase enumerates all MSSes of the program using domain
    heuristics and records their complements (the MCSes) in a hitting set
    solver. The second phase reads the MUSes off as the minimal hitting sets
    of the collected MCSes.
    """

    def __init__(self, ctl: clingo.Control, hitting_set: HittingSet) -> None:
        """
        Set up the solver for MSS enumeration over the hitting set universe.
        """
        ctl.configuration.solver.heuristic = "Domain"  # ty: ignore[invalid-assignment]
        ctl.configuration.solve.models = "0"  # ty: ignore[invalid-assignment]
        ctl.configuration.solve.enum_mode = "domRec"  # ty: ignore[invalid-assignment]
        set_heuristic(ctl, tuple(hitting_set.universe), True)

        self.hitting_set = hitting_set
        self.ctl = ctl
        self._gen = self.__iter__()

    def __iter__(self) -> Iterator[tuple[str, set[int]]]:
        """
        Yield all `("mss", ...)` pairs first, then all `("mus", ...)` pairs.
        """
        U = self.hitting_set.universe
        with self.ctl.solve(yield_=True) as sh:
            for model in sh:
                mss = {x for x in U if model.is_true(x)}
                yield ("mss", mss)

                mcs = tuple(U.difference(mss))
                self.hitting_set.add_set(mcs)

        while (mus := self.hitting_set.get_mhs()) is not None:
            self.hitting_set.block_mhs(mus)
            yield "mus", set(mus)

    def __next__(self) -> tuple[str, set[int]]:
        """
        Return the next labelled set from the underlying generator.
        """
        return next(self._gen)
