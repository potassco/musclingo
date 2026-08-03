"""
Core shrinking by linear elimination of literals.
"""

from collections.abc import Sequence

from musclingo.shrink.protocol import MinimizationStrategy


class LinearElimination(MinimizationStrategy):
    """
    Shrink a core by testing its literals one at a time.

    A literal whose removal makes the core satisfiable is critical and kept;
    otherwise the solver's own core is used to discard several literals at once.
    """

    def shrink_known(self, core: Sequence[int]) -> tuple[int, ...]:
        """
        Return a MUS contained in `core`, which must be unsatisfiable.
        """
        working = list(core)
        critical = []

        while working:
            ans = self.check(critical + working[1:])

            if ans.satisfiable:
                critical.append(working[0])
                working = working[1:]
            elif ans.unsatisfiable:
                assert self.core is not None, "on_core() must populate self.core when unsatisfiable"
                working = list(self.core.difference(critical))

        return tuple(critical)
