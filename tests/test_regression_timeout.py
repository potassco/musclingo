"""
Regression test for the timeout check of linear elimination.
"""

import clingo

from musclingo.shrink import LinearElimination


def test_timeout() -> None:
    """
    Check that a generous timeout does not interrupt the shrinking of a trivial core.
    """
    ctl = clingo.Control()
    ctl.add("base", [], "{a; b}. :- a, b.")
    ctl.ground()
    atoms = [ctl.symbolic_atoms[clingo.Function(c)] for c in "ab"]
    core = [sym.literal for sym in atoms if sym is not None]

    assert LinearElimination(ctl).shrink_known(core, timeout=60.0) == (set(core), False)
