# Numerical Linear Algebra Notes (TMA4205)

These notes are a compact study compendium for **TMA4205 Numerical Linear Algebra**.  
The goal is to connect theory, geometry, and algorithms so you can move from definitions to practical iterative solvers.

## What You Will Learn

By working through the notes, you should be able to:

- explain conditioning, stability, and why numerical methods can fail
- use orthogonality and projections to formulate approximation problems
- understand Krylov subspaces as the basis for modern iterative solvers
- compare Steepest Descent, Conjugate Gradient, FOM, and GMRES
- reason about convergence behavior and stopping criteria in practice

## Content Roadmap

### Part I: Foundations

Core linear algebra and numerical analysis tools used throughout:

- preliminaries and notation
- linear systems and conditioning
- orthogonality and related geometric insight

### Part II: Projections and Krylov Ideas

Conceptual bridge from theory to algorithms:

- projection theory (orthogonal/oblique viewpoints)
- Krylov subspaces
- projection-based derivation of iterative methods

### Part III: Iterative Solvers

Method-focused chapters with intuition and derivations:

- Steepest Descent (SD)
- Conjugate Gradient (CG)
- Full Orthogonalization Method (FOM)
- GMRES

## How To Study These Notes

- Start with Part I unless you are already confident on conditioning and orthogonality.
- For each method, track three things: search space, orthogonality condition, and update rule.
- Reproduce key derivations by hand before reading the final formulas.
- Use the exercises to test conceptual understanding, not just symbolic manipulation.
- Use the lecture and exam material in `backmatter/` for revision and exam prep.

## Companion Material

- `backmatter/exercises`: additional problems
- `backmatter/exams`: exam-related material and cheat sheets
- `backmatter/lectures`: lecture-specific note files
- `examples/gmres_demo.py`: small computational demo connected to GMRES ideas

## Minimal Build Note

The compiled compendium is `main.pdf`. If needed, build with:

```bash
latexmk -pdf main.tex
```
