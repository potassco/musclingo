from collections.abc import Sequence

import clingo


def check_minimal_unsatisfiable(ctl: clingo.Control, core: list[int]) -> None:
    ans = ctl.solve(assumptions=core)
    assert ans.unsatisfiable, "The MUS is not an unsatisfiable core..."

    for c in tuple(core):
        core.pop(0)
        ans = ctl.solve(assumptions=core)
        assert ans.satisfiable, "The MUS is not minimally unsatisfiable..."
        core.append(c)


def check_maximal_satisfiable(ctl: clingo.Control, mss: Sequence[int], mcs: Sequence[int]) -> None:
    ans = ctl.solve(assumptions=mss)
    assert ans.satisfiable, "The MSS is not a satisfiable subset..."

    base = list(mss)
    for x in mcs:
        ans = ctl.solve(assumptions=base + [x])
        assert ans.unsatisfiable, "The MSS is not maximal: adding a corrected literal stays satisfiable..."
