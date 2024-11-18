cd iqtree2
git apply ../openmp.patch
rm -rf build
mkdir build && cd build
cmake -DBUILD_LIB=ON ..
make -j
cd ../..
mv iqtree2/build/libiqtree2.a src/piqtree2/_libiqtree/