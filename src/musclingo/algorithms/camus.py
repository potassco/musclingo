from typing import Iterator, Tuple
import clingo
from musclingo.hitting_set import HittingSet
from musclingo.heuristic_utils import set_heuristic


class CAMUS:
	def __init__(self, ctl: clingo.Control, hitting_set: HittingSet) -> None:
		ctl.configuration.solver.heuristic = "Domain"  # ty: ignore[invalid-assignment]
		ctl.configuration.solve.models = "0"  # ty: ignore[invalid-assignment]
		ctl.configuration.solve.enum_mode = "domRec"  # ty: ignore[invalid-assignment]
		set_heuristic(ctl, tuple(hitting_set.universe), True)

		self.hitting_set = hitting_set
		self.ctl = ctl
		self._gen = self.__iter__()

	def __iter__(self) -> Iterator[Tuple[str, Tuple[int, ...]]]:
		U = self.hitting_set.universe
		with self.ctl.solve(yield_=True) as sh:
			for model in sh:
				mss = tuple(x for x in U if model.is_true(x))
				yield ("mss", mss)

				mcs = tuple(U.difference(mss))
				self.hitting_set.add_set(mcs)

		while (mus := self.hitting_set.get_mhs()) is not None:
			self.hitting_set.block_mhs(mus)
			yield "mus", tuple(mus)

	def __next__(self) -> Tuple[str, Tuple[int, ...]]:
		return next(self._gen)
