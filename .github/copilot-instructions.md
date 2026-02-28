# Copilot / AI agent instructions

Short summary
- This repository is a LuaLaTeX book of lecture notes (TMA4205). The root entrypoint is `main.tex` and the final artifact is `main.pdf`.
- The project organizes content in `chapters/` (parts with chapters), `frontmatter/`, and `backmatter/`. Styling and macros live in `preamble.tex` and files under `includes/`.

Big picture / Why
- Centralized preamble: `preamble.tex` defines fonts, theorem styles, macros and colors. Keep macro / notation changes centralized to avoid duplication.
- Content split: `chapters/part*/*` keeps logical grouping for parts & chapters to make incremental editing and compilation easy.
- Figures: `figures/` contains both lightweight `.tikz` snippets (input via `\input{...}`) and standalone `.tex` figures compiled independently (e.g., `figures/extra/*`). `.latexmkrc` includes a rule to build standalone figure `.tex` files.

Developer workflows (common tasks & commands)
- Build full book (recommended):
  - ```bash
    latexmk -pdflatex=lualatex -shell-escape -file-line-error -recorder -pdf -g main.tex
    ```
  - This is also referenced in `.latexmkrc` and `README.md`.
- Clean auxiliary files:
  - ```bash
    latexmk -C
    ```
- Quick edit / per-chapter builds (fast iteration):
  - Compile a chapter directly (uses `subfiles`):
    ```bash
    latexmk -pdflatex=lualatex -shell-escape -file-line-error -recorder -pdf chapters/partI-foundations/03_orthogonality.tex
    ```
- Build standalone figure (if wrapped in a `standalone` document):
  - ```bash
    latexmk -pdf figures/extra/lu-decomposition.tex
    ```
- Formatting: this repo uses `latexindent`. Use `latexindent -w <file>` to write formatted changes, and expect `__latexindent_temp_*` files to appear while formatting.

Conventions & Key Patterns
- Macros separation: Put formatting macros in `includes/commands.tex` and semantic/notation macros in `includes/notation.tex`.
- Theorem environments: The preamble uses `tcolorbox` theorem definitions (`definition`, `theorem`, `lemma`, `example`, `solution`, ...). Label prefixes are defined in `preamble.tex` (e.g. `thm:` for theorems, `def:` for definitions) — reuse these prefixes when adding new environments (e.g. `\label{thm:convergence}`). Use `\cref{...}` for references (cleveref is enabled).
- Figures: Prefer the `standalone` wrapper for figures you want to compile in isolation. TikZ snippets in `figures/*.tikz` at the moment are input directly; large diagrams use `standalone` `.tex` files.
- File naming: chapters are `NN_title.tex` (e.g. `01_preliminaries.tex`); keep two-digit numeric prefixes for ordering.
- Colors & styling: color tokens (like `thm-color`) and global styles are defined in `includes/colors` and `preamble.tex`. Use those tokens instead of ad hoc colors.

Useful files to check before edits
- `main.tex` — assembly of the book
- `preamble.tex` — fonts, theorem styles, macros, page layout
- `includes/commands.tex` and `includes/notation.tex` — where macros live
- `.latexmkrc` — latexmk config; includes custom rules for building figures and selecting lualatex
- `figures/` — contains `.tikz` and standalone figure `.tex` files

Documentation & Best practices for AI agents
- Preserve author style: prefer `tcolorbox` based theorems and `
ewcommand` patterns. If a new symbol is introduced, add it to `includes/notation.tex` and use `\vct{}` or `\ip{}` wrappers where appropriate.
- Keep changes minimal per PR: separate content edits (new math text) from style changes (macro rename / reflow). Formatting changes should be done in a separate commit.
- Be explicit about languages: the preamble uses `\usepackage[english]{babel}` but there are some Norwegian files (e.g., `cheat-sheet-norsk.tex`). Prefer English defaults unless the file is clearly flagged `norsk`.
- Avoid committing generated artifacts (e.g., `main.pdf`) – the `.gitignore` includes common LaTeX aux files but some authors may add `main.pdf` by mistake — do not do that.

Debugging tips & common pitfalls
- Missing fonts will break compilation (Fira Sans, Fira Math, etc.). If these fonts are missing, the build will error — install the fonts or change to fallback fonts in `preamble.tex`.
- For link/compile issues, re-run `latexmk` with no `-silent` flags or run `lualatex` directly to see clearer errors. The `-file-line-error` flag helps map errors to file/line.
- If a TikZ snippet is failing: wrap it as a standalone `.tex` with `\documentclass{standalone}` for quick debugging and compilation.

Next steps when contributing
- If adding new notation: add macro to `includes/notation.tex`.
- If adding new macro for formatting: add to `includes/commands.tex` and add a short comment.
- If adding a figure: either add `.tikz` snippet and `\input` it from a chapter, or create a `standalone` `.tex` file in `figures/` so that `.latexmkrc` can prebuild the figure PDF.

Questions for you:
- Do you want CI (GitHub Actions) to automatically run `latexmk` on PRs and attach `main.pdf` as a build artifact? (I can include a sample workflow)
- Are label prefix conventions (colon vs no-colon in `preamble.tex` definitions) intentional, or should we standardize them across theorem types?