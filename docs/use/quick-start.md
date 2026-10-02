---
icon: "material/rocket-launch"
---

# Quick Start Guide

`musclingo` finds minimal unsatisfiable subsets (MUSes) and maximal satisfiable subsets (MSSes) of ASP programs, using the [clingo](https://potassco.org/clingo/) API.

To use it, choose which parts of your program may be blamed for unsatisfiability. These _objective atoms_ are passed to the library as program literals; you can map the returned literals back to symbols yourself. See the [worked example](../examples/index.md) for how to tag a program and build that mapping.

## Choose a minimization strategy

Use a minimization strategy to shrink an unsatisfiable set of objective literals to one MUS:

- [`LinearElimination`](../reference/api/shrink.md): removes literals one at a time, reusing solver cores.
- [`QuickXPlain`](../reference/api/shrink.md): splits the set recursively (divide and conquer).

## Choose an extraction algorithm

Use an extraction algorithm to enumerate MUSes and MSSes:

- [`MARCO`](../reference/api/algorithms.md): explores candidate subsets and can enumerate MUSes and MSSes.
- [`CAMUS`](../reference/api/algorithms.md): finds correction sets first, then computes MUSes using hitting-set duality.
- [`IHS`](../reference/api/algorithms.md): interleaves correction-set and hitting-set computation.

See the [worked example](../examples/index.md) for a complete run, or browse the [minimization API](../reference/api/shrink.md) and [extraction API](../reference/api/algorithms.md).
