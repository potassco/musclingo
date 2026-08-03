"""
Minimal hitting set computation over a universe of assumption literals.
"""

from collections.abc import Sequence
from typing import Protocol

from musclingo.lattice import AssumptionsLattice


class HittingSet(Protocol):
    """
    Incremental minimal hitting set solver over a fixed universe of literals.
    """

    universe: frozenset[int]

    def add_set(self, mcs: Sequence[int]) -> None:
        """
        Add a set that every future hitting set must intersect.
        """
        ...

    def block_mhs(self, mhs: Sequence[int]) -> None:
        """
        Exclude `mhs` and all of its supersets from future results.
        """
        ...

    def get_mhs(self) -> Sequence[int] | None:
        """
        Return a minimal hitting set of the collected sets, or `None` if none is left.
        """
        ...


class LatticeHittingSet:
    """
    A `HittingSet` backed by an `AssumptionsLattice`, biased towards small sets.
    """

    def __init__(self, universe: Sequence[int]) -> None:
        """
        Create the underlying lattice over `universe`.
        """
        self._lattice = AssumptionsLattice(universe, bias=False)

    @property
    def universe(self) -> frozenset[int]:
        """
        The set of literals hitting sets are drawn from.
        """
        return self._lattice.universe

    def get_mhs(self) -> Sequence[int] | None:
        """
        Return the next unexplored minimal hitting set, or `None` if none is left.
        """
        return self._lattice.next_seed()

    def add_set(self, mcs: Sequence[int]) -> None:
        """
        Require every future hitting set to contain at least one literal of `mcs`.
        """
        clause = [-self._lattice.lookup.inv[c] for c in mcs]
        with self._lattice.ctl.backend() as b:
            b.add_rule([], clause)

    def block_mhs(self, mhs: Sequence[int]) -> None:
        """
        Exclude `mhs` and all of its supersets from future results.
        """
        self._lattice.block_up(mhs)
