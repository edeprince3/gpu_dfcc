cmake_minimum_required(VERSION 3.1 FATAL_ERROR)
cmake_policy(SET CMP0048 NEW)
project(gpu_dfcc VERSION 1.0 LANGUAGES CXX CUDA)
find_package(CUDA REQUIRED)
#find_package(PythonLibs 2.7 REQUIRED)
find_package(psi4)
include_directories(${PYTHON_INCLUDE_DIRS})
set(CUDA_NVCC_FLAGS "${CUDA_NVCC_FLAGS} -Xcompiler -fopenmp")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(PN ${PROJECT_NAME})
#set(CMAKE_CXX_STANDARD_LIBRARIES ${CUDA_LIBRARIES} "-lcublas -lcudart -lcusolver")
cuda_add_library(core SHARED
  gpu_dfcc.cu
  gpuhelper.cu
  gpuhelper_driver.cc
  triples.cu
  ccsd.cu)

target_link_libraries(core
  ${PYTHON_LIBRARIES}
  cublas
  cusolver
  cudart
  psi4::core    )
include(CMakePackageConfigHelpers)
set_target_properties(core PROPERTIES PREFIX "")

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

# <<<  Install  >>>

install(TARGETS core
        EXPORT "${PN}Targets"
        LIBRARY DESTINATION ${PYMOD_INSTALL_FULLDIR})

install(FILES __init__.py pymodule.py LICENSE README.md
        DESTINATION ${PYMOD_INSTALL_FULLDIR})

install(DIRECTORY tests/
        DESTINATION ${PYMOD_INSTALL_FULLDIR}/tests
        FILES_MATCHING PATTERN "gpu_dfcc*/input.dat"
        PATTERN "old-tests" EXCLUDE)

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
