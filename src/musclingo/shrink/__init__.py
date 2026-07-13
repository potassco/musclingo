from typing import Optional, Sequence, Tuple
import clingo

from asp_muses.shrink.protocol import MinimizationStrategy
from asp_muses.shrink.linear_elimination import LinearElimination
from asp_muses.shrink.quickxplain import QuickXPlain


def shrink(
	ctl: clingo.Control,
	core: Sequence[int],
	strategy: Optional[MinimizationStrategy] = None,
) -> Optional[Tuple[int, ...]]:
	if strategy is None:
		strategy = LinearElimination(ctl)

	ans = strategy.check(core)
	if ans.satisfiable:
		return None

	return strategy.shrink_known(core)


__all__ = [
	"MinimizationStrategy",
	"LinearElimination",
	"QuickXPlain",
	"shrink",
]
