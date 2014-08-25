import psi4
import re
import os
import math
import warnings
from driver import *
from wrappers import *
from molutil import *
from p4util import *

def run_gpu_dfcc(name, **kwargs):
    """Function encoding sequence of PSI module calls for
    a GPU-accelerated DF-CCSD(T) computation.

    >>> energy('df-ccsd(t)')

    """
    lowername = name.lower()
    kwargs = kwargs_lower(kwargs)

    # stash user options
    optstash = OptionsState(
        ['GPU_DFCC','COMPUTE_TRIPLES'],
        ['GPU_DFCC','DFCC'],
        ['GPU_DFCC','NAT_ORBS'],
        ['GPU_DFCC','RUN_CEPA'],
        ['SCF','DF_INTS_IO'],
        ['SCF','SCF_TYPE'])

    psi4.set_local_option('SCF','DF_INTS_IO', 'SAVE')
    psi4.set_local_option('GPU_DFCC','DFCC', True)
    psi4.set_local_option('GPU_DFCC','RUN_CEPA', False)

    # throw an exception for open-shells
    if (psi4.get_option('SCF','REFERENCE') != 'RHF' ):
        raise ValidationError("Error: %s requires \"reference rhf\"." % lowername)

    # override symmetry:
    molecule = psi4.get_active_molecule()
    molecule.update_geometry()
    molecule.reset_point_group('c1')
    molecule.fix_orientation(1)
    molecule.update_geometry()

    # triples?
    if (lowername == 'gpu-df-ccsd'):
        psi4.set_local_option('GPU_DFCC','COMPUTE_TRIPLES', False)
    if (lowername == 'gpu-df-ccsd(t)'):
        psi4.set_local_option('GPU_DFCC','COMPUTE_TRIPLES', True)
    #if (lowername == 'fno-df-ccsd'):
    #    psi4.set_local_option('GPU_DFCC','COMPUTE_TRIPLES', False)
    #    psi4.set_local_option('GPU_DFCC','NAT_ORBS', True)
    #if (lowername == 'fno-df-ccsd(t)'):
    #    psi4.set_local_option('GPU_DFCC','COMPUTE_TRIPLES', True)
    #    psi4.set_local_option('GPU_DFCC','NAT_ORBS', True)

    # set scf-type to df unless the user wants something else
    if psi4.has_option_changed('SCF','SCF_TYPE') == False:
       psi4.set_local_option('SCF','SCF_TYPE', 'DF')

    if psi4.get_option('GPU_DFCC','DF_BASIS_CC') == '':
       basis   = psi4.get_global_option('BASIS')
       dfbasis = corresponding_rifit(basis)
       psi4.set_local_option('GPU_DFCC','DF_BASIS_CC',dfbasis)

    scf_helper(name,**kwargs)
    psi4.plugin('gpu_dfcc.so')

    # restore options
    optstash.restore()

    return psi4.get_variable("CURRENT ENERGY")

# Integration with driver routines
procedures['energy']['gpu-df-ccsd(t)'] = run_gpu_dfcc
procedures['energy']['gpu-df-ccsd']    = run_gpu_dfcc


def exampleFN():
    # Your Python code goes here
    pass
