"""
Strategies to shrink an unsatisfiable core down to a MUS.
"""

from collections.abc import Sequence

import clingo

from musclingo.shrink.linear_elimination import LinearElimination
from musclingo.shrink.protocol import MinimizationStrategy
from musclingo.shrink.quickxplain import QuickXPlain


def shrink(
    ctl: clingo.Control,
    core: Sequence[int],
    strategy: MinimizationStrategy | None = None,
) -> set[int] | None:
    """
    Shrink `core` to a MUS, or return `None` if `core` is satisfiable.

    Defaults to `LinearElimination` when no strategy is given.
    """
    if strategy is None:
        strategy = LinearElimination(ctl)

    ans = strategy.check(core)
    if ans.satisfiable:
        return None

    return strategy.shrink_known(core)


__all__ = [
    "LinearElimination",
    "MinimizationStrategy",
    "QuickXPlain",
    "shrink",
]
