# Use LuaLaTeX by default
$pdf_mode = 1;                                  # build pdf
$pdflatex = 'lualatex -file-line-error -interaction=nonstopmode -recorder -shell-escape %O %S';
$latex    = $pdflatex;

# Prefer biber where available
if (-e 'refs.bib' || -e 'tex/refs.bib') {
    $bibtex = 'biber %O %S';
} else {
    $bibtex = 'bibtex %O %S';
}

# Keep default file (the main entrypoint)
$default_files = 'main.tex';

# Allow up to 5 runs to resolve cross-references
$max_repeat = 5;

# Extra cleanup
push @generated_exts, qw(synctex.gz bbl bcf run.xml fls fdb_latexmk aux.lock xdv out lg idx ind ilg);
$clean_full_ext = "synctex.gz xdv run.xml out fls fdb_latexmk aux.lock";

# Custom rule: compile standalone figures in figures/ using lualatex
# This will let latexmk build changed standalone figures like 'figures/xxx.tex' -> 'figures/xxx.pdf'
add_cus_dep('tex','pdf',0,'lualatex_fig');
sub lualatex_fig {
    my ($base, $path) = @_;
    return 0 if ($path !~ m{^figures/});        # only care for files under figures/
    my $outdir = '.';
    if ($path =~ m{^(.*/)}s) { $outdir = $1; }
    my $cmd = "lualatex -file-line-error -interaction=nonstopmode -recorder -shell-escape -output-directory=$outdir $path";
    print "latexmk: compiling standalone figure: $cmd\n";
    system($cmd) == 0 or return 1;
    return 0;
}

# Optional: Print the command to use
END {
    print "Use: latexmk -pdf -silent main.tex  (or see README.md for: latexmk -pdflatex=lualatex -shell-escape -file-line-error -recorder -pdf -g main.tex)\n";
}
