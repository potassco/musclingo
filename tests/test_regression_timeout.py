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
    a, b = [ctl.symbolic_atoms[clingo.Function(c)].literal for c in "ab"]

    assert LinearElimination(ctl).shrink_known([a, b], timeout=60.0) == ({a, b}, False)
