cd iqtree2
rm -rf build
mkdir build && cd build
echo $CC
echo $CXX

if [[ "$(uname)" == "Darwin" ]]; then
    C_COMPILER="clang"
    CXX_COMPILER="clang++"
else
    C_COMPILER="gcc"
    CXX_COMPILER="g++"
fi

cmake -DBUILD_LIB=ON \
      -DCMAKE_C_COMPILER="$C_COMPILER" \
      -DCMAKE_CXX_COMPILER="$CXX_COMPILER" \
      ..

make -j
cd ../..
mv iqtree2/build/libiqtree2.a src/piqtree2/_libiqtree/