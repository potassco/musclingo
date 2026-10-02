# Examples

## Original program

Consider the following encoding `gc.lp`, which models 2-colorability of an input graph. Any odd cycle in the input graph makes it unsatisfiable.

```clingo
color(r; b).
node(X;Y) :- edge(X,Y).
{ assign(X,C): color(C) } = 1 :- node(X).
:- assign(X,C), assign(Y,C), edge(X,Y).
```

As input graph, we use the following `instance.lp`.

```clingo
edge(0,1). edge(1,2). edge(0,2).
edge(2,3). edge(3,4). edge(2,4).
edge(3,5). edge(4,5).
```

```text
0     3---5
|\   /|  /
| \ / | /
1--2--4
```

The graph has three triangles and no other odd cycle, so we expect exactly three MUSes (minimal unsatisfiable subsets), one per triangle.

## Tagging the logic program

MUSes are computed with respect to a set of _objective atoms_; we refer to Alviano et al.[^1] for the formal definitions. To get MUSes over the edges, we guard each edge with a fresh atom `o(i)` and leave the `o(i)` open with a choice rule. We save the result as `tagged.lp`.

```clingo
edge(0,1) :- o(1).
edge(1,2) :- o(2).
edge(0,2) :- o(3).
edge(2,3) :- o(4).
edge(3,4) :- o(5).
edge(2,4) :- o(6).
edge(3,5) :- o(7).
edge(4,5) :- o(8).
{ o(X) } :- X=1..8.
```

!!! note

    When the objectives are input facts, the fresh atoms are not needed: the facts themselves can be put in a choice rule.

## Computing MUSes

Once the logic program is tagged, we can compute MUSes as follows.

```python
import clingo
from musclingo.algorithms import MARCO
from musclingo.lattice import AssumptionsLattice
from musclingo.shrink import LinearElimination, shrink

ctl = clingo.Control()
ctl.load("gc.lp")
ctl.load("tagged.lp")
ctl.ground()

# Define a mapping between objective atoms' literals and symbols
lookup = {x.literal: x.symbol for x in ctl.symbolic_atoms.by_signature("o", 1)}


def show(lits):
    return " ".join(str(lookup[lit]) for lit in sorted(lits))


# Compute a single MUS
mus = shrink(ctl, list(lookup))
assert mus is not None, "the program is satisfiable"
print("single MUS", show(mus))

# Enumerate all MUSes and MSSes (maximal satisfiable subsets).
# bias=True makes the lattice propose large seeds first, which is
# what makes every satisfiable seed an MSS.
lattice = AssumptionsLattice(lookup, bias=True)
for kind, subset in MARCO(lattice, LinearElimination(ctl)):
    print(kind.upper(), show(subset))
```

Output:

```text
single MUS o(4) o(5) o(6)
MUS o(4) o(5) o(6)
MUS o(5) o(7) o(8)
MUS o(1) o(2) o(3)
MSS o(1) o(2) o(4) o(6) o(7) o(8)
...
```

Each MUS is the edge set of one triangle, e.g. `o(4) o(5) o(6)` is triangle `2-3-4`. The remaining 14 MSSes follow.

[^1]: M. Alviano, C. Dodaro, S. Fiorentino, A. Previti, F. Ricca. [ASP and subset minimality: Enumeration, cautious reasoning and MUSes](https://doi.org/10.1016/j.artint.2023.103931). Artificial Intelligence 320, 103931 (2023).
