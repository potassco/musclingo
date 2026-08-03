from collections.abc import Sequence
from typing import Protocol

from musclingo.lattice import AssumptionsLattice


class HittingSet(Protocol):
    universe: frozenset[int]

    def add_set(self, mcs: Sequence[int]) -> None: ...

    def block_mhs(self, mhs: Sequence[int]) -> None: ...

    def get_mhs(self) -> Sequence[int] | None: ...


class LatticeHittingSet:
    def __init__(self, universe: Sequence[int]) -> None:
        self._lattice = AssumptionsLattice(universe, bias=False)

    @property
    def universe(self) -> frozenset[int]:
        return self._lattice.universe

    def get_mhs(self) -> Sequence[int] | None:
        return self._lattice.next_seed()

    def add_set(self, mcs: Sequence[int]) -> None:
        clause = [-self._lattice.lookup.inv[c] for c in mcs]
        with self._lattice.ctl.backend() as b:
            b.add_rule([], clause)

    def block_mhs(self, mhs: Sequence[int]) -> None:
        self._lattice.block_up(mhs)
