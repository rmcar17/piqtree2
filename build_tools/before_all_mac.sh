brew update
brew install eigen boost gcc libomp cmake

GCC_BIN=$(brew --prefix gcc)/bin/gcc-14
GPP_BIN=$(brew --prefix gcc)/bin/g++-14
OMP_LIB=$(brew --prefix libomp)/lib
OMP_INCLUDE=$(brew --prefix libomp)/include

export CC=$GCC_BIN
export CXX=$GPP_BIN
export LDFLAGS="-L$OMP_LIB"
export CPPFLAGS="-I$OMP_INCLUDE"
export OPENMP_C_FLAGS="-fopenmp -L$OMP_LIB -I$OMP_INCLUDE"
export OPENMP_CXX_FLAGS="-Xclang -fopenmp -L$OMP_LIB -I$OMP_INCLUDE"

bash build_tools/build_iqtree.sh