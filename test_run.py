from musclingo.algorithms import MARCO
from musclingo.lattice import AssumptionsLattice
from musclingo.shrink import LinearElimination
import sys
import clingo

def fmt_literals(literals, lookup):
	return " ".join(str(lookup[z]) for z in literals)

program = sys.argv[1]

ctl = clingo.Control()
ctl.load(program)
ctl.ground()

literals = []
lookup = dict()
for symlit in ctl.symbolic_atoms.by_signature('graph_edge', 2):
	literals.append(symlit.literal)
	lookup[symlit.literal] = symlit.symbol

literals = [symlit.literal for symlit in ctl.symbolic_atoms.by_signature('graph_edge', 2)]

lattice = AssumptionsLattice(literals, bias=True)
strategy = LinearElimination(ctl)

m = MARCO(lattice, strategy)

for type_, set_ in m:
	print(type_, fmt_literals(set_, lookup))
