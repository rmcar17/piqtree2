cd iqtree2
rm -rf build
mkdir build && cd build
cmake -DBUILD_LIB=ON -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DCMAKE_C_FLAGS="$OpenMP_C_FLAGS" -DCMAKE_CXX_FLAGS="$OPENMP_CXX_FLAGS" ..
make -j
cd ../..
mv iqtree2/build/libiqtree2.a src/piqtree2/_libiqtree/