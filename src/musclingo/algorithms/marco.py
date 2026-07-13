from typing import Iterator, Tuple
from musclingo.lattice import Lattice
from musclingo.shrink import MinimizationStrategy


class MARCO:
	def __init__(self, lattice: Lattice, strategy: MinimizationStrategy) -> None:
		self.lattice = lattice
		self.minimization = strategy
		self._gen = self.__iter__()

	def __iter__(self) -> Iterator[Tuple[str, Tuple[int, ...]]]:
		while (seed := self.lattice.next_seed()) is not None:
			ans = self.minimization.check(seed)

			if ans.satisfiable:
				yield "mss", seed
				self.lattice.block_down(seed)

			elif ans.unsatisfiable:
				core = self.minimization.shrink_known(seed)
				yield "mus", core
				self.lattice.block_up(core)

	def __next__(self) -> Tuple[str, Tuple[int, ...]]:
		return next(self._gen)
