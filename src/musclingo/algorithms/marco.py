"""
The MARCO algorithm for MUS and MSS enumeration.
"""

from collections.abc import Iterator

from musclingo.lattice import Lattice
from musclingo.shrink import MinimizationStrategy


class MARCO:
    """
    Enumerate MUSes and MSSes by exploring the power set lattice of assumptions.

    Unexplored seeds are drawn from the lattice. A satisfiable seed is reported
    as an MSS and its down-set is blocked; an unsatisfiable seed is shrunk to a
    MUS by the minimization strategy and its up-set is blocked.
    """

    def __init__(self, lattice: Lattice, strategy: MinimizationStrategy) -> None:
        """
        Bind the seed lattice and the strategy used to shrink unsatisfiable seeds.
        """
        self.lattice = lattice
        self.minimization = strategy
        self._gen = self.__iter__()

    def __iter__(self) -> Iterator[tuple[str, tuple[int, ...]]]:
        """
        Yield `("mss", ...)` and `("mus", ...)` pairs until the lattice is fully explored.
        """
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
        """
        Return the next labelled set from the underlying generator.
        """
        return next(self._gen)
