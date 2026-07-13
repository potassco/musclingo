from typing import Sequence, Tuple
from asp_muses.shrink.protocol import MinimizationStrategy


class LinearElimination(MinimizationStrategy):
	def shrink_known(self, core: Sequence[int]) -> Tuple[int, ...]:
		working = list(core)
		critical = []

		while working:
			ans = self.check(critical + working[1:])

			if ans.satisfiable:
				critical.append(working[0])
				working = working[1:]
			elif ans.unsatisfiable:
				assert self.core is not None, (
					"on_core() must populate self.core when unsatisfiable"
				)
				working = list(self.core.difference(critical))

		return tuple(critical)
