# Numerical Linear Algebra Notes (TMA4205)

A LuaLaTeX compendium for the NTNU course **TMA4205 Numerical Linear Algebra**. The project gathers lecture notes, worked examples, and appendices into a single book-style document (`main.pdf`).

## Requirements

- TeX distribution with LuaLaTeX support (TeX Live 2023+ or MiKTeX with equivalent packages)
- `latexmk` for automated builds
- OpenType fonts used in the preamble: Fira Sans, IBM Plex Sans Condensed, Fira Code, Fira Math (bundled with recent TeX Live installations)
- Common LaTeX packages already referenced in `tex/preamble.tex` (e.g. `unicode-math`, `tcolorbox`, `algorithm`, `siunitx`, `hyperref`)

## Build

```bash
latexmk -pdflatex=lualatex -shell-escape -file-line-error -recorder -pdf -g main.tex
```
This produces `main.pdf` in the project root. `latexmk -C` cleans auxiliary files.

## Project Layout

```
main.tex                    Entry point that stitches the book together
frontmatter/                Title page and front matter assets
chapters/                   Course content split into themed parts
  partI-foundations/        Fundamentals: preliminaries, linear systems, preconditioning
  partII-projections/       Projection methods: Krylov spaces, Arnoldi, iterative solvers
backmatter/                 Lecture summaries and appendices (exercises, diverse notes)
tex/                        Shared preamble, macros, colors, and bibliography (`refs.bib`)
figures/                    Placeholder for figures used across the notes
```

`main.tex` uses `\includeonly{...}` to focus on specific sections during development—uncomment entries there to limit compilation scope while editing.

## Tips
- Keep shared commands and theorem styles in `tex/macros.tex` and `tex/preamble.tex` to avoid duplication.

_No license has been specified; treat the material as personal course notes unless stated otherwise._
