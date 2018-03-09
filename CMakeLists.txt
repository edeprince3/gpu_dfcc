cmake_policy(SET CMP0048 NEW)  # project_VERSION* variables populated from project(... VERSION x.x.x) string
project(gpu_dfcc 
        VERSION 0.1
        LANGUAGES CXX CUDA)
set(gpudfcc_AUTHORS      "A. Eugene DePrince III")
set(gpudfcc_DESCRIPTION  "GPU DF-CC")
#set(gpudfcc_URL          "github.com/edeprince3/gpu_dfcc")
set(gpudfcc_LICENSE      "GPL 2+")

cmake_minimum_required(VERSION 3.1 FATAL_ERROR)
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

find_package(psi4 1.0 REQUIRED)

# <<<  Options  >>>

set(CUDA_NVCC_FLAGS "${CUDA_NVCC_FLAGS} -dynamic -shared -Xcompiler --compiler-options -fopenmp '-fPIC' -O2 ${OpenMP_CXX_FLAGS}")
set(CMAKE_CXX_STANDARD_LIBRARIES ${CUDA_LIBRARIES} "-lcublas -lcudart -lcusolver")
include(psi4OptionsTools)

option_with_print(ENABLE_OPENMP "Enable threadsafe linking to OpenMP parallelized programs." ON)
option_with_print(ENABLE_GENERIC "Enable mostly static linking in shared library" OFF)
if (APPLE AND (CMAKE_CXX_COMPILER_ID MATCHES GNU))
    option_with_flags(ENABLE_XHOST "Enable processor-specific optimization" OFF)
else ()
    option_with_flags(ENABLE_XHOST "Enable processor-specific optimization" ON
                      "-xHost" "-march=native")
endif()

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

set(PN ${PROJECT_NAME})

# PYMOD_INSTALL_LIBDIR If set, installs python modules to
#                      ${CMAKE_INSTALL_LIBDIR}${PYMOD_INSTALL_LIBDIR}/v2rdm_casscf rather than
#                      the default read off parent Psi4

#   install alongside psi4 module by default, but overrideable
get_filename_component(psi4_CMAKE_INSTALL_PREFIX ${psi4_INCLUDE_DIR} DIRECTORY)
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX ${psi4_CMAKE_INSTALL_PREFIX} CACHE PATH "Install path" FORCE)
endif()
message(STATUS "Plugin install prefix: ${CMAKE_INSTALL_PREFIX}")

if(PYMOD_INSTALL_LIBDIR)
    set(PYMOD_INSTALL_FULLDIR "${CMAKE_INSTALL_LIBDIR}${PYMOD_INSTALL_LIBDIR}/${PN}")
else()
    file(RELATIVE_PATH _tmp ${psi4_CMAKE_INSTALL_PREFIX} ${psi4_LIBRARY})
    #   e.g., _tmp = lib/psi4/core.so
    get_filename_component(_tmp2 ${_tmp} DIRECTORY)
    get_filename_component(_tmp3 ${_tmp2} DIRECTORY)
    set(PYMOD_INSTALL_FULLDIR "${_tmp3}/${PN}")
endif()
message(STATUS "Plugin module install: ${PYMOD_INSTALL_FULLDIR}")


include(custom_cxxstandard)
include(autocmake_omp)
include(custom_static_library)

# <<<  Build  >>>

if (CMAKE_Fortran_COMPILER_ID MATCHES Intel)
    set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -heap-arrays")
endif()

# old way of listing files
file(GLOB SOURCES "*.cc" "*.F90" "*.cu")
add_psi4_plugin(gpu_dfcc 
        ${SOURCES})

#add_psi4_plugin(gpu_dfcc
#)

target_link_libraries(gpu_dfcc PRIVATE ${LIBC_INTERJECT})

# <<<  Install  >>>

install(TARGETS gpu_dfcc
        EXPORT "${PN}Targets"
        LIBRARY DESTINATION ${PYMOD_INSTALL_FULLDIR})

install(FILES __init__.py pymodule.py LICENSE README.md
        DESTINATION ${PYMOD_INSTALL_FULLDIR})

#install(DIRECTORY tests/
#        DESTINATION ${PYMOD_INSTALL_FULLDIR}/tests
#        FILES_MATCHING PATTERN "gpu_dfcc*/input.dat"
#        PATTERN "old-tests" EXCLUDE)

# <<< Export Config >>>

# GNUInstallDirs "DATADIR" wrong here; CMake search path wants "share".
set(CMAKECONFIG_INSTALL_DIR "share/cmake/${PN}")
configure_package_config_file(cmake/${PN}Config.cmake.in
                              "${CMAKE_CURRENT_BINARY_DIR}/${PN}Config.cmake"
                              INSTALL_DESTINATION ${CMAKECONFIG_INSTALL_DIR})
write_basic_package_version_file(${CMAKE_CURRENT_BINARY_DIR}/${PN}ConfigVersion.cmake
                                 VERSION ${${PN}_VERSION}
                                 COMPATIBILITY AnyNewerVersion)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${PN}Config.cmake
              ${CMAKE_CURRENT_BINARY_DIR}/${PN}ConfigVersion.cmake
        DESTINATION ${CMAKECONFIG_INSTALL_DIR})
install(EXPORT "${PN}Targets"
        NAMESPACE "${PN}::"
        DESTINATION ${CMAKECONFIG_INSTALL_DIR})



# old stuff

#target_compile_definitions(gpu_dfcc PRIVATE _OPENMP)

