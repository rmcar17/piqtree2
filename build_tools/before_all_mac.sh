brew update
brew install make eigen boost libomp

LLVM_BIN=$(brew --prefix llvm)/bin
OMP_LIB=$(brew --prefix libomp)/lib
OMP_INCLUDE=$(brew --prefix libomp)/include
LLVM_LIB=$(brew --prefix llvm)/lib
LLVM_INCLUDE=$(brew --prefix libomp)/include

OMP_ROOT=$(brew --prefix libomp)

export LDFLAGS="-L$OMP_ROOT/lib"
export CPPFLAGS="-I$OMP_ROOT/include"
export CXXFLAGS="-I$OMP_ROOT/include"

bash build_tools/build_iqtree.sh
