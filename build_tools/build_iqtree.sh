cd iqtree2
rm -rf build
mkdir build && cd build
echo $CC
echo $CXX
cmake -DBUILD_LIB=ON -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DOpenMP_C_FLAGS="$OpenMP_C_FLAGS" -DOpenMP_CXX_FLAGS="$OpenMP_CXX_FLAGS" -DOpenMP_C_LIB_NAMES="$OpenMP_C_LIB_NAMES" -DOpenMP_CXX_LIB_NAMES="$OpenMP_CXX_LIB_NAMES" -DOpenMP_libomp_LIBRARY="$OpenMP_libomp_LIBRARY" -DCMAKE_C_FLAGS="$OpenMP_C_FLAGS" -DCMAKE_CXX_FLAGS="$OPENMP_CXX_FLAGS" ..
make -j
cd ../..
mv iqtree2/build/libiqtree2.a src/piqtree2/_libiqtree/