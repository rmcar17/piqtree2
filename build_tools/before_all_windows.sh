choco install -y llvm --version=14.0.6 --allow-downgrade
choco install -y eigen
choco install -y make

# bash build_tools/build_iqtree.sh
cd iqtree2
rm -rf build
mkdir build && cd build
cmake -G "MinGW Makefiles" -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_FLAGS=--target=x86_64-pc-windows-gnu -DCMAKE_CXX_FLAGS=--target=x86_64-pc-windows-gnu -DCMAKE_MAKE_PROGRAM=mingw32-make -DIQTREE_FLAGS="single" -DBUILD_LIB=ON ..
make -j
cd ../..
mv iqtree2/build/libiqtree2.a src/piqtree2/_libiqtree/