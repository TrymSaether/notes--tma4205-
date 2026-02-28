"""
Educational GMRES implementation (learning style) with a restarted wrapper
and a runnable example that plots residual histories.

Requires: numpy, scipy, matplotlib

Run example:

    python3 examples/gmres_demo.py

The script builds a simple nonsymmetric sparse test matrix, runs the
educational GMRES and SciPy's GMRES for comparison, and plots residuals.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
from typing import Callable, List, Optional, Tuple


# ------------------------- Linear algebra helpers -------------------------

def givens_rotation(a: float, b: float) -> Tuple[float, float]:
    """Compute Givens rotation coefficients (c, s) to eliminate b.

    Returns c, s such that
        [[c, s], [-s, c]] @ [a, b] = [r, 0]
    """
    if b == 0.0:
        return 1.0, 0.0
    if abs(b) > abs(a):
        tau = -a / b
        s = 1.0 / np.sqrt(1.0 + tau * tau)
        c = s * tau
    else:
        tau = -b / a
        c = 1.0 / np.sqrt(1.0 + tau * tau)
        s = c * tau
    return c, s


# ------------------------------ GMRES core --------------------------------

def gmres(
    A,
    b: np.ndarray,
    x0: Optional[np.ndarray] = None,
    tol: float = 1e-8,
    maxiter: Optional[int] = None,
) -> Tuple[np.ndarray, List[float]]:
    """
    Basic, instructive GMRES implementation (no preconditioner, no restarts).

    Parameters
    - A: array-like, sparse matrix, or LinearOperator supporting .dot(x)
    - b: right-hand side vector
    - x0: initial guess (defaults to zero)
    - tol: stopping tolerance on residual norm
    - maxiter: maximum number of Arnoldi steps (defaults to len(b))

    Returns
    - x: approximate solution
    - resvec: list of residual norms at each iteration (including initial)

    Notes
    - This implementation uses Modified Gram--Schmidt for orthogonalization
      and Givens rotations to update the small least-squares problem.
    - It is written for clarity and learning; it is not optimized for
      production-scale problems.
    """
    n = b.shape[0]
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()

    if maxiter is None:
        maxiter = n

    # Make A into a linear operator for uniform access
    Aop = spla.aslinearoperator(A)

    r0 = b - Aop.matvec(x)
    beta = np.linalg.norm(r0)
    if beta == 0.0:
        return x, [0.0]

    # Storage for Arnoldi basis and Hessenberg matrix
    V = np.zeros((n, maxiter + 1), dtype=float)
    H = np.zeros((maxiter + 1, maxiter), dtype=float)

    V[:, 0] = r0 / beta

    # Givens rotation storage
    cs = np.zeros(maxiter)
    sn = np.zeros(maxiter)

    # rhs for the (rotated) least-squares problem
    g = np.zeros(maxiter + 1, dtype=float)
    g[0] = beta

    resvec: List[float] = [beta]

    for j in range(maxiter):
        # Arnoldi: w = A * v_j
        w = Aop.matvec(V[:, j])

        # Modified Gram--Schmidt
        for i in range(j + 1):
            H[i, j] = np.dot(V[:, i], w)
            w = w - H[i, j] * V[:, i]

        H[j + 1, j] = np.linalg.norm(w)
        if H[j + 1, j] != 0.0:
            V[:, j + 1] = w / H[j + 1, j]

        # Apply previous Givens rotations to the new column H[:, j]
        for i in range(j):
            temp = cs[i] * H[i, j] + sn[i] * H[i + 1, j]
            H[i + 1, j] = -sn[i] * H[i, j] + cs[i] * H[i + 1, j]
            H[i, j] = temp

        # Compute i-th rotation to eliminate H[j+1, j]
        c, s = givens_rotation(H[j, j], H[j + 1, j])
        cs[j] = c
        sn[j] = s

        # Apply rotation
        H[j, j] = c * H[j, j] + s * H[j + 1, j]
        H[j + 1, j] = 0.0

        # Update g (right-hand side)
        temp = c * g[j] + s * g[j + 1]
        g[j + 1] = -s * g[j] + c * g[j + 1]
        g[j] = temp

        # residual norm is |g[j+1]|
        res_norm = abs(g[j + 1])
        resvec.append(res_norm)

        if res_norm <= tol:
            # Solve upper triangular system H[0:j+1, 0:j+1] * y = g[0:j+1]
            y = np.linalg.solve(H[: j + 1, : j + 1], g[: j + 1])
            x = x + V[:, : j + 1].dot(y)
            return x, resvec

    # End loop: form solution with full maxiter
    y = np.linalg.lstsq(H[:maxiter, :maxiter], g[:maxiter], rcond=None)[0]
    x = x + V[:, :maxiter].dot(y)
    return x, resvec


# --------------------------- Restarted GMRES ------------------------------

def gmres_restart(
    A,
    b: np.ndarray,
    x0: Optional[np.ndarray] = None,
    m: int = 50,
    tol: float = 1e-8,
    maxcycles: int = 20,
) -> Tuple[np.ndarray, List[float]]:
    """Simple restarted GMRES(m) wrapper.

    Runs GMRES for at most `m` inner iterations, then restarts using the
    current solution as initial guess. Collects residual history across cycles.
    """
    if x0 is None:
        x = np.zeros_like(b)
    else:
        x = x0.copy()

    residuals: List[float] = []
    for cycle in range(maxcycles):
        x, rvec = gmres(A, b, x0=x, tol=tol, maxiter=m)
        # rvec includes the initial residual at the start of the inner solve,
        # so skip its first entry when concatenating after the first cycle.
        if cycle == 0:
            residuals.extend(rvec)
        else:
            residuals.extend(rvec[1:])

        if residuals[-1] <= tol:
            break

    return x, residuals


# ------------------------------- Example ----------------------------------

def build_test_matrix(n: int = 200) -> sp.csr_matrix:
    """Build a simple nonsymmetric sparse test matrix.

    Start from a standard tridiagonal Poisson-like matrix and add some
    nonsymmetric random upper-triangular perturbations to make it
    nonsymmetric while keeping it reasonably well-conditioned.
    """
    main_diag = 2.0 * np.ones(n)
    off_diag = -1.0 * np.ones(n - 1)
    A = sp.diags([off_diag, main_diag, off_diag], offsets=[-1, 0, 1], format="csr")

    # Add a small random sparse upper triangular part to introduce nonsymmetry
    rng = np.random.default_rng(42)
    R = sp.random(n, n, density=0.01, format="csr", random_state=rng)
    R = sp.triu(R) * 0.5
    A = A + R
    return A


def example_plot():
    n = 400
    A = build_test_matrix(n)
    b = np.ones(n)

    # Run our educational GMRES (no restart)
    x_gmres, res_gmres = gmres(A, b, tol=1e-8, maxiter=200)
    iters_gmres = list(range(len(res_gmres)))

    # Run restarted GMRES with m=50
    x_rgmres, res_rgmres = gmres_restart(A, b, m=50, tol=1e-8, maxcycles=10)
    iters_rgmres = list(range(len(res_rgmres)))

    # Run SciPy's GMRES for comparison, collecting residuals via callback
    scipy_res = []

    def callback_scipy(resid):
        scipy_res.append(resid)

    # Use a wrapper to create a fresh initial guess
    x0 = np.zeros(n)
    spla.gmres(A, b, x0=x0, tol=1e-8, restart=50, maxiter=5, callback=callback_scipy)

    if len(scipy_res) == 0:
        # SciPy sometimes reports only the final residual via callback semantics.
        # As fallback, compute the residual history by incremental solves.
        scipy_res = [np.linalg.norm(b - A.dot(x0))]

    its_scipy = list(range(len(scipy_res)))

    # Plotting
    plt.figure(figsize=(8, 5))
    plt.semilogy(iters_gmres, res_gmres, label="GMRES (educational)")
    plt.semilogy(iters_rgmres, res_rgmres, label=f"GMRES({50}) restarted")
    plt.semilogy(its_scipy, scipy_res, label="SciPy gmres (callback)")
    plt.xlabel("Iteration")
    plt.ylabel("Residual norm (2-norm)")
    plt.title("GMRES residual history — educational example")
    plt.legend()
    plt.grid(True, which="both")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    example_plot()
