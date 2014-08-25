GPU DF-CC plugin in PSI4
===

OVERVIEW
---

This plugin to Psi4[1] performs GPU-accelerated density-fitted (DF)
singles and doubles coupled cluster (CCSD)[2] computations.  The
perturbative triples contribution to the correlation energy (T) is also
implemented, but the performace of (T) in the present plugin is not much
better than that of the DF-CCSD(T)[3,4] implementation in the current
release of Psi4.

INSTALLATION
---

To run the psi4 plugin gpu_dfcc:

* Download and install psi4public from github.com:
https://github.com/psi4/psi4public.  You can obtain the source using git:

    > git clone git@github.com:psi4/psi4public.git

    Install psi4 as described on http://www.psicode.org/.

* Configure gpu_dfcc by editing the configure file in the gpu_dfcc/
directory.  Specify the location of psi4 and your cublas library and run
the configure script:

    > ./configure

    Make sure that your LD_LIBRARY_PATH contains the location of your
    cublas library.

* Compile the plugin:

    > make

* Run the test in this directory:

    > psi4 input.dat -n 2

    Note that plugin gpu_dfcc requires psi4 be run with at least two threads.
    In general, the code requires that you use one more thread than the number
    of GPUs on your system.

INPUT OPTIONS
---

* **NUM_GPUS** (int):

    the number of GPUs on your system.  The code will automatically
    determine the resources available, so this keyword is useful if you
    want to use fewer GPUs than are available.  This may be the case if
    you have a GPU to drive your monitor in addition to a compute-oriented
    card.

* **MAX_MAPPED_MEMORY** (int): 

    the maximum amount of pinned CPU memory.  This
    code will pin an amount of CPU memory that is equivalent to the amount of
    GPU memory, up to this maximum value.  The value is given in mb.

* **CC_TIMINGS** (bool): 

    do time each CC diagram?

* **E_CONVERGENCE** (double): 

    energy convergence for the CCSD energy. 

* **R_CONVERGENCE** (double): 

    amplitude convergence for the CCSD energy. 

* **MAXITER** (int): 

    the maximum number of CCSD iterations.

* **DIIS_MAX_VECS** (int): 

    the maximum number of DIIS vectors stored on disk.

* **NAT_ORBS** (bool): 

    do truncate the virtual space using MP2 natural orbitals?

* **OCC_TOLERANCE** (double): 

    occupation tolerance for neglecting MP2 natural
    virtual orbitals.

* **DF_BASIS_CC** (str): 

    auxiliary basis set for DF-CCSD(T).

* **CHOLESKY_TOLERANCE** (double): 

    tolerance for Cholesky decomposition of the
    ERI tensor (only used if DF_BASIS_CC=cholesky or SCF_TYPE=cd).


KNOWN ISSUES
---
The program tends to exit with an innocuous segfault.


REFERENCES
---
[1] J. M. Turney, A. C. Simmonett, R. M. Parrish, E. G. Hohenstein, F. A. Evangelista, J. T. Fermann, B. J.  Mintz, L. A. Burns, J. J. Wilke, M. L. Abrams, N. J. Russ, M. L. Leininger, C. L. Janssen, E. T. Seidl, W. D. Allen, H. F. Schaefer, R. A. King, E. F. Valeev, C. D. Sherrill, and T. D. Crawford, *WIREs: Comp. Molec. Sci.* **2**, 556 (2012). "Psi4: an open-source ab initio electronic structure program"

[2] A. E. DePrince III, M. R. Kennedy, B. G. Sumpter, and C. D. Sherrill, *Mol. Phys.* **112**, 844 (2014). "Density-fitted singles and doubles coupled cluster on graphics processing units"

[3] A. E. DePrince III and C. D. Sherrill, *J. Chem. Theory Comput.* **9**, 2687 (2013).
"Accuracy and efficiency of coupled-cluster theory using density fitting / Cholesky decomposition, frozen natural orbitals, and a t1-transformed Hamiltonian"

[4] A. E. DePrince III and C. David Sherrill, *J. Chem. Theory Comput.* **9**, 293 (2013).
"Accurate noncovalent interaction energies using truncated basis sets based on frozen natural orbitals"

