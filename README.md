GPU DF-CC plugin in PSI4
===

OVERVIEW
---
This plugin to Psi4 performs GPU-accelerated density-fitted (DF) singles and doubles coupled cluster (CCSD)
computations.  The perturbative triples contribution to the correlation energy (T) is also implemented, but
the performace of (T) in the present plugin is not much better than that of the DF-CCSD(T) implementation in the
current release of Psi4.

INSTALLATION
---

To run the psi4 plugin gpu_dfcc:

1.  Download and install psi4public from github.com:
https://github.com/psi4/psi4public.  You can obtain the source using git:

> git clone git@github.com:psi4/psi4public.git

Install psi4 as described on http://www.psicode.org/.


2.  Configure gpu_dfcc by editing the configure file in this directory.
Specify the location of psi4 and your cublas library.  

> ./configure

Make sure that your LD_LIBRARY_PATH contains the location of your
cublas library.

3.  Compile the plugin.

> make

4.  Make sure the test included in this directory passes.

> psi4 input.dat -n 2

Note that plugin gpu_dfcc requires psi4 be run with at least two threads.
