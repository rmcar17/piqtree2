cd iqtree2
rm -rf build
mkdir build && cd build

cmake_cmd="cmake -DIQTREE_FLAGS='single' -DBUILD_LIB=ON .."

if [[ "$RUNNER_OS" == "Windows" ]]; then
  cmake_cmd="cmake -G 'MinGW Makefiles' \
    -DBoost_INCLUDE_DIR='$BOOST_ROOT/include' \
    -DBoost_LIBRARY_DIRS='$BOOST_ROOT/lib' \
    -DIQTREE_FLAGS='single' -DBUILD_LIB=ON .."
fi

eval $cmake_cmd

make -j
cd ../..
mv iqtree2/build/libiqtree2.a src/piqtree2/_libiqtree/