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

