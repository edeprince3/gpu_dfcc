import pytest

import gpu_dfcc


hardware_nvidia_gpu = pytest.mark.skipif(gpu_dfcc.cudaGetDeviceCount() == 0,
                                reason='Not detecting Nvidia GPU via `nvidia-smi`. Install one')


@pytest.mark.quick
@hardware_nvidia_gpu
def test_gpudfcc1():
    """gpu_dfcc/tests/gpu_dfcc1"""
    #! cc-pvdz (H2O)2 Test DF-CCSD vs GPU-DF-CCSD

    import psi4

    H20 = psi4.geometry("""
               O          0.000000000000     0.000000000000    -0.068516219310   
               H          0.000000000000    -0.790689573744     0.543701060724   
               H          0.000000000000     0.790689573744     0.543701060724   
    """)

    psi4.set_memory(32000000000)
    psi4.set_options({
      'cc_timings': False,
      'num_gpus': 1,
      'cc_type': 'df',
      'df_basis_cc':  'aug-cc-pvdz-ri',
      'df_basis_scf': 'aug-cc-pvdz-jkfit',
      'basis':        'aug-cc-pvdz',
      'freeze_core': 'true',
      'e_convergence': 1e-8,
      'd_convergence': 1e-8,
      'r_convergence': 1e-8,
      'scf_type': 'df',
      'maxiter': 30})
    psi4.set_num_threads(2)
    en_dfcc     = psi4.energy('ccsd', molecule=H20)
    en_gpu_dfcc = psi4.energy('gpu-df-ccsd', molecule=H20)

    assert psi4.compare_values(en_gpu_dfcc, en_dfcc, 8, "CCSD total energy")


@hardware_nvidia_gpu
def test_gpudfcc2():
    """gpu_dfcc/tests/gpu_dfcc2"""
    #! aug-cc-pvdz (H2O) Test DF-CCSD(T) vs GPU-DF-CCSD(T)

    import psi4

    H20 = psi4.geometry("""
               O          0.000000000000     0.000000000000    -0.068516219310   
               H          0.000000000000    -0.790689573744     0.543701060724   
               H          0.000000000000     0.790689573744     0.543701060724   
    """)

    psi4.set_memory(32000000000)
    psi4.set_options({
      'cc_type': 'df',
      'basis':        'aug-cc-pvdz',
      'freeze_core': 'true',
      'e_convergence': 1e-8,
      'd_convergence': 1e-8,
      'r_convergence': 1e-8,
      'scf_type': 'df',
      'maxiter': 30})
    
    psi4.set_num_threads(2)
    
    en_dfcc     = psi4.energy('ccsd(t)')
    en_gpu_dfcc = psi4.energy('gpu-df-ccsd(t)')
    
    assert psi4.compare_values(en_gpu_dfcc, en_dfcc, 8, "CCSD total energy")
