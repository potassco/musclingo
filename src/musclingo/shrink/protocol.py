from typing import Optional, Protocol, Sequence, Set, Tuple
import clingo


class MinimizationStrategy(Protocol):
	ctl: clingo.Control
	core: Optional[Set[int]]
	checks: int

	def __init__(self, ctl: clingo.Control) -> None:
		self.ctl = ctl
		self.core = None
		self.checks = 0

	def on_core(self, core: Sequence[int]) -> None:
		self.core = set(core)

	def check(self, seed: Sequence[int]) -> clingo.SolveResult:
		self.checks += 1
		ans = self.ctl.solve(on_core=self.on_core, assumptions=seed)
		assert not ans.unknown

		return ans

	def shrink_known(self, core: Sequence[int]) -> Tuple[int, ...]:
		raise NotImplementedError
