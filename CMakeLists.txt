cmake_minimum_required(VERSION 2.8)
project(gpu_dfcc LANGUAGES CXX CUDA)
find_package(CUDA)
find_package(PythonLibs 2.7 REQUIRED)
find_package(psi4)
include_directories(${PYTHON_INCLUDE_DIRS})
set(CUDA_NVCC_FLAGS "${CUDA_NVCC_FLAGS} -Xcompiler -fopenmp")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
#set(CMAKE_CXX_STANDARD_LIBRARIES ${CUDA_LIBRARIES} "-lcublas -lcudart -lcusolver")
cuda_add_library(gpu_dfcc SHARED
  gpu_dfcc.cu
  gpuhelper.cu
  gpuhelper_driver.cc
  triples.cu
  ccsd.cu)

target_link_libraries(gpu_dfcc
  ${PYTHON_LIBRARIES}
  cublas
  cusolver
  cudart
  psi4::core	)

set_target_properties(gpu_dfcc PROPERTIES PREFIX "")

install(TARGETS gpu_dfcc
        EXPORT "${PN}Targets"
        LIBRARY DESTINATION ${PYMOD_INSTALL_FULLDIR})

install(FILES __init__.py pymodule.py LICENSE README.md
        DESTINATION ${PYMOD_INSTALL_FULLDIR})

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
