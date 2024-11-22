brew update
brew install eigen boost llvm gcc libomp cmake

LLVM_BIN=$(brew --prefix llvm)/bin
OMP_LIB=$(brew --prefix libomp)/lib
OMP_INCLUDE=$(brew --prefix libomp)/include

export CC=$LLVM_BIN/clang
export CXX=$LLVM_BIN/clang++
export LDFLAGS="-L$OMP_LIB"
export CPPFLAGS="-I$OMP_INCLUDE"
export OpenMP_C_FLAGS="-fopenmp -L$OMP_LIB -I$OMP_INCLUDE"
export OpenMP_CXX_FLAGS="-fopenmp -L$OMP_LIB -I$OMP_INCLUDE"
export OpenMP_C_LIB_NAMES="libomp"
export OpenMP_CXX_LIB_NAMES="libomp"
export OpenMP_libomp_LIBRARY="$OMP_LIB"

bash build_tools/build_iqtree.sh
