"""
The interface shared by all core shrinking strategies.
"""

from collections.abc import Iterable
from typing import Protocol

import clingo


class MinimizationStrategy(Protocol):
    """
    Base class for core shrinking strategies.

    It owns the solver, tracks the last core reported by clingo and counts the
    satisfiability checks performed. Subclasses only implement `shrink_known()`.
    """

    ctl: clingo.Control
    core: set[int] | None
    checks: int

    def __init__(self, ctl: clingo.Control) -> None:
        """
        Bind the strategy to `ctl` and reset the core and check counter.
        """
        self.ctl = ctl
        self.core = None
        self.checks = 0

    def on_core(self, core: Iterable[int]) -> None:
        """
        Record the unsatisfiable core reported by the solver.
        """
        self.core = set(core)

    def check(self, seed: Iterable[int]) -> clingo.SolveResult:
        """
        Solve under `seed` as assumptions, updating the check counter and the last core.
        """
        self.checks += 1
        ans = self.ctl.solve(on_core=self.on_core, assumptions=list(seed))
        assert not ans.unknown

        return ans

    def shrink_known(self, core: Iterable[int]) -> set[int]:
        """
        Return a MUS contained in `core`, which must be unsatisfiable.
        """
        raise NotImplementedError
