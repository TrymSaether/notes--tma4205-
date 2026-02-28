# TMA4205 Numerical Linear Algebra Notes

Notes for **TMA4205 Numerical Linear Algebra (NTNU)**.
The whole point is to connect linear algebra theory with the iterative methods that actually get used in practice.

- Main reading file: [`main.pdf`](main.pdf)

## What This Covers

Main themes in the notes:

- conditioning, stability, and common numerical failure modes
- orthogonality and projections as approximation tools
- Krylov subspaces as the core idea behind modern iterative methods
- how SD, CG, FOM, and GMRES are built and how they differ
- convergence behavior and stopping criteria

## Roadmap

The material is split into three parts.

### Part I: Linear Algebra Foundations

Files:

- `chapters/partI-foundations/00_introduction.tex`
- `chapters/partI-foundations/01_preliminaries.tex`
- `chapters/partI-foundations/02_linear_systems.tex`
- `chapters/partI-foundations/03_orthogonality.tex`

Focus:

- notation and baseline definitions
- linear systems and conditioning
- geometry through orthogonality

### Part II: Projection and Krylov Foundations

Files:

- `chapters/partII-projections/04_projection_theory.tex`
- `chapters/partII-projections/05_krylov_subspaces.tex`

Focus:

- orthogonal vs oblique projection viewpoints
- subspace methods as the bridge from theory to algorithms

### Part III: Iterative Krylov Solvers

Files:

- `chapters/partIII-solvers/06_SD.tex`
- `chapters/partIII-solvers/07_CG.tex`
- `chapters/partIII-solvers/08_FOM.tex`
- `chapters/partIII-solvers/09_GMRES.tex`

Focus:

- where each algorithm comes from
- assumptions, tradeoffs, and cost
- what drives convergence in practice

## Study Flow

Simple chapter loop:

1. Read definitions and theorems.
2. Re-do key derivations from scratch.
3. Pin down the geometric idea (projection, orthogonality, subspace).
4. Write a short convergence summary.
5. Do related exercises.

For solver chapters, keep track of:

- search space
- orthogonality/constraint condition
- update rule
- stopping criterion

## Extra Material

Supplementary content lives in `backmatter/`:

- `backmatter/exercises/`: practice problems
- `backmatter/lectures/`: lecture-aligned notes
- `backmatter/exams/`: exam material and cheat sheets
- `backmatter/appendix/`: extra reference material

Suggested exam prep order:

1. quick pass over Part I fundamentals
2. side-by-side comparison of SD/CG/FOM/GMRES
3. exercises to find weak spots
4. timed work with exam files

## Build PDF

For editing/maintenance:

```bash
latexmk -pdf main.tex
```
