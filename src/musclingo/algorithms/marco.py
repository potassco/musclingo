from collections.abc import Iterator

from musclingo.lattice import Lattice
from musclingo.shrink import MinimizationStrategy


class MARCO:
    def __init__(self, lattice: Lattice, strategy: MinimizationStrategy) -> None:
        self.lattice = lattice
        self.minimization = strategy
        self._gen = self.__iter__()

    def __iter__(self) -> Iterator[tuple[str, tuple[int, ...]]]:
        while (seed := self.lattice.next_seed()) is not None:
            ans = self.minimization.check(seed)

            if ans.satisfiable:
                yield "mss", seed
                self.lattice.block_down(seed)

            elif ans.unsatisfiable:
                core = self.minimization.shrink_known(seed)
                yield "mus", core
                self.lattice.block_up(core)

    def __next__(self) -> tuple[str, tuple[int, ...]]:
        return next(self._gen)
