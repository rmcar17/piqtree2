cd iqtree2
git apply ../openmp.patch
rm -rf build
mkdir build && cd build
cmake -DBUILD_LIB=ON -DOpenMP_CXX_FLAG="-Xclang -fopenmp" -DOpenMP_CXX_INCLUDE_DIR=/opt/homebrew/opt/libomp/include -DOpenMP_CXX_LIB_NAMES=libomp -DOpenMP_C_FLAG="-Xclang -fopenmp" -DOpenMP_C_INCLUDE_DIR=/opt/homebrew/opt/libomp/include -DOpenMP_C_LIB_NAMES=libomp -DOpenMP_libomp_LIBRARY=/opt/homebrew/opt/libomp/lib/libomp.dylib
 ..
make -j
cd ../..
mv iqtree2/build/libiqtree2.a src/piqtree2/_libiqtree/