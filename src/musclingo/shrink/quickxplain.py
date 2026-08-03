"""
Core shrinking with the QuickXPlain divide and conquer algorithm.
"""

from collections.abc import Sequence

from musclingo.shrink.protocol import MinimizationStrategy


class QuickXPlain(MinimizationStrategy):
    """
    Shrink a core by recursively splitting it in half.

    Each half is tested against the accumulated background, which needs
    logarithmically many solver calls in the best case instead of one call per
    literal. Cores reported by the solver are reused to trim candidates early.
    """

    def _trim(self, A: list[int], B: list[int], combined: set[int] | None = None) -> list[int]:
        """
        Drop the literals of `A` that the last reported core shows to be irrelevant.

        The core is only usable for trimming if it is contained in the union of
        `A` and `B`, which the caller may pass precomputed as `combined`.
        """
        if combined is None:
            combined = set(A) | set(B)

        if self.core is not None and self.core.issubset(combined):
            return [x for x in A if x in self.core]

        return A

    def __qx__(self, A: list[int], B: list[int]) -> list[int]:
        """
        Entry point of the recursion: return the literals of `A` needed for unsatisfiability, given `B`.

        The union of `A` and `B` has to be unsatisfiable.
        """
        combined = set(A) | set(B)
        if self.core is None or not self.core.issubset(combined):
            ans = self.check(A + B)
            assert ans.unsatisfiable, "__qx__() requires the supplied core to be unsatisfiable"

        assert self.core is not None, "on_core() must populate self.core when unsatisfiable"

        if len(A) == 0:
            return []

        A = self._trim(A, B, combined)
        if len(A) == 0:
            return []

        return self.__qx_prime__(B, A, B)

    def __qx_prime__(self, C: list[int], A: list[int], B: list[int]) -> list[int]:
        """
        Recursive step: return the part of `A` that is needed on top of background `B`.

        `C` holds the literals most recently added to `B`; when it is non empty
        and `B` alone is already unsatisfiable, nothing from `A` is needed.
        """
        if len(C) > 0:
            ans = self.check(B)
            if ans.unsatisfiable:
                return []

        A = self._trim(A, B)
        if len(A) == 0:
            return []

        if len(A) == 1:
            return A

        k = len(A) // 2
        A_1 = A[:k]
        A_2 = A[k:]

        X_2 = self.__qx_prime__(A_1, A_2, B + A_1)
        X_1 = self.__qx_prime__(X_2, A_1, B + X_2)

        return X_1 + X_2

    def shrink_known(self, core: Sequence[int]) -> tuple[int, ...]:
        """
        Return a MUS contained in `core`, which must be unsatisfiable.
        """
        return tuple(self.__qx__(list(core), []))
