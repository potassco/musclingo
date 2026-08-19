"""
Core shrinking by linear elimination of literals.
"""

import time
from collections.abc import Iterable

from musclingo.shrink.protocol import MinimizationStrategy


class LinearElimination(MinimizationStrategy):
    """
    Shrink a core by testing its literals one at a time.

    A literal whose removal makes the core satisfiable is critical and kept;
    otherwise the solver's own core is used to discard several literals at once.
    """

    def shrink_known(self, core: Iterable[int], timeout: float | None = None) -> tuple[set[int], bool]:
        """
        Find a MUS contained in `core`, which must be unsatisfiable.

        Parameters
        ----------
        core : Iterable[int]
            literals of the (unminimized) core
        timeout : float | None
            If specified sets a timeout in seconds, that if exceeded stops the linear elimination and returns the
            already found mus literals

        Returns
        -------
        mus : set[int]
            literals of the mus
        interrupted : bool
            Indicates whether the linear elimination was interrupted after a timeout before all assumptions were covered
        """
        working = list(core)
        critical = []

        t_start = time.perf_counter()
        interrupted = False
        while working:
            ans = self.check(critical + working[1:])

            if ans.satisfiable:
                critical.append(working[0])
                working = working[1:]
            elif ans.unsatisfiable:
                assert self.core is not None, "on_core() must populate self.core when unsatisfiable"
                working = list(self.core.difference(critical))

            if timeout is not None and t_start + time.perf_counter() > timeout:
                interrupted = True
                break

        return set(critical), interrupted
