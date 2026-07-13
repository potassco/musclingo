from typing import Sequence
import clingo


def heuristic_type(bias: bool) -> clingo.HeuristicType:
	return clingo.HeuristicType.True_ if bias else clingo.HeuristicType.False_


def set_heuristic(ctl: clingo.Control, atoms: Sequence[int], bias: bool) -> None:
	h = heuristic_type(bias)
	with ctl.backend() as b:
		for lit in atoms:
			b.add_heuristic(lit, h, 1, 1, [])
