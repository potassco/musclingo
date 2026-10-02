---
hide:
  - navigation
  - toc
---

# musclingo

This Python library implements algorithms for computing *minimal unsatisfiable subsets*
(MUSes) and *maximal satisfiable subsets* (MSSes) of unsatisfiable ASP programs, built on
top of the [clingo](https://potassco.org/clingo/) API.

When an ASP program has no answer set, a MUS pins down a smallest set of
assumptions that cannot hold together. *musclingo* lets you choose which
assumptions may be blamed, and then finds one or all such sets.

<div class="grid cards" markdown>

-   :material-rocket-launch: __Getting Started__

    ---

    Install *musclingo* and compute your first MUS in a few lines of Python.

    [:octicons-arrow-right-24: Quick Start Guide](use/quick-start.md)

-   :material-code-braces: __Examples__

    ---

    A worked example showing how to enumerate MUSes and MSSes.

    [:octicons-arrow-right-24: See Examples](examples/index.md)

-   :material-book-open-variant: __Reference__

    ---

    An overview of the implemented algorithms and the full API documentation.

    [:octicons-arrow-right-24: Reference](reference/index.md)

</div>

## What's inside

-   **Minimization strategies** shrink an unsatisfiable set of assumption literals
    to a MUS, using `LinearElimination` or `QuickXPlain`.
    See [`musclingo.shrink`](reference/api/shrink.md).

-   **Extraction algorithms** enumerate all MUSes and MSSes of a program with
    `MARCO`, `CAMUS` or `IHS`.
    See [`musclingo.algorithms`](reference/api/algorithms.md).

-   **Lattices** keep track of the subsets that have already
    been explored and propose the next candidate.
    See `musclingo.lattice`.


## Similar projects

- [clingo-explaid](https://potassco.org/clingo-explaid/) This library collects tools for explaining why an ASP program is unsatisfiable. The API to offers support for preprocessing, subset computation, and constraint analysis helpers for building
explanation systems.

- [asplain](https://potassco.org/asplain/) A library for explaining why an ASP program is unsatisfiable, focusing on providing human-readable explanations. Includes a command line and web interface for contrasting explanations.

!!! info
    *musclingo* is part of the [Potassco](https://potassco.org) suite.
