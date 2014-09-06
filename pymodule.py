#
#@BEGIN LICENSE
#
# GPU-accelerated density-fitted coupled-cluster, a plugin to:
#
# PSI4: an ab initio quantum chemistry software package
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#@END LICENSE
#

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
        ['SCF','DF_INTS_IO'],
        ['SCF','SCF_TYPE'])

    psi4.set_local_option('SCF','DF_INTS_IO', 'SAVE')
    psi4.set_local_option('GPU_DFCC','DFCC', True)

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
