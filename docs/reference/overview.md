---
icon: "material/map-outline"
---

# Overview

`musclingo` is a Python package that provides algorithms for computing minimal unsatisfiable subsets (MUSes) of ASP programs, and related objects such as maximal satisfiable subsets (MSSes). The implementation follows Alviano et al., [ASP and subset minimality: Enumeration, cautious reasoning and MUSes](https://doi.org/10.1016/j.artint.2023.103931). The library exposes _minimization strategies_ and _extraction algorithms_ separately, which handle the solving-under-assumptions plumbing required to minimize and extract unsatisfiable cores.

The user is responsible for choosing the _objective atoms_ and for tagging the input logic program accordingly. Objective atoms are handled at the literal level: sets of objective atoms are passed and returned as sets of program literals, and mapping them back to symbols is left to the user.

!!! note "Objective atoms"

    Intuitively, _objective atoms_ are the parts of the program that can be blamed for unsatisfiability. Each of them acts as a switch for a piece of the program, typically a fact or a rule, while everything else is fixed background.
The [usage example](../examples/usage-example.md) clarifies how to tag a program and how to build this mapping.

## Minimization strategies

A minimization strategy shrinks an unsatisfiable set of objective atoms to a single MUS.

| Strategy | Idea | Reference |
|---|---|---|
| `LinearElimination` | Removes one atom at a time, reusing the cores reported by the solver | |
| `QuickXPlain` | Splits the set in halves, divide and conquer | [Understanding the QuickXPlain Algorithm: Simple Explanation and Formal Proof](https://arxiv.org/abs/2001.01835) |

## Extraction algorithms

An extraction algorithm enumerates the MUSes and MSSes of the program.

| Algorithm | Idea | Reference |
|---|---|---|
| `MARCO` | Explores the subsets of the objective atoms, shrinking the unsatisfiable ones to MUSes. It can also enumerate MSSes/MCSes | [Fast, flexible MUS enumeration](https://doi.org/10.1007/s10601-015-9183-0) |
| `CAMUS` | Enumerates all MCSes (complements of MSSes) first, then computes MUSes by hitting set duality | [Algorithms for Computing Minimal Unsatisfiable Subsets of Constraints](https://doi.org/10.1007/s10817-007-9084-z) |
| `IHS` | As in CAMUS, but interleaves MCS computation with hitting set computation | [Implicit Hitting Set Algorithms for Reasoning Beyond NP](https://dl.acm.org/doi/10.5555/3032027.3032040) |

The implementations of `MARCO`, `CAMUS` and `IHS` follow the sketch given by [Alviano et al.](https://doi.org/10.1016/j.artint.2023.103931).
