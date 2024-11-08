# Setup directories

cd iqtree2
rm -rf build
mkdir build && cd build

# echo "hello"
# echo $BOOST_ROOT
# echo $ZLIB_ROOT
# ls $ZLIB_ROOT\\include
# ls $ZLIB_ROOT\\lib

# Initialise cmake

cmake_cmd="cmake -DIQTREE_FLAGS='single' -DBUILD_LIB=ON .."

if [[ "$RUNNER_OS" == "Windows" ]]; then
  cmake_cmd="cmake -G 'MinGW Makefiles' \
    -DBoost_INCLUDE_DIR='$BOOST_ROOT/include' \
    -DBoost_LIBRARY_DIRS='$BOOST_ROOT/lib' \
    -DIQTREE_FLAGS='single' -DBUILD_LIB=ON .."
fi
    # -DCMAKE_TOOLCHAIN_FILE='$VCPKG_ROOT\\scripts\\buildsystems\\vcpkg.cmake' \
    # -DZLIB_INCLUDE_DIR='$ZLIB_ROOT\\include' \
    # -DZLIB_LIBRARY='$ZLIB_ROOT\\lib' \

eval $cmake_cmd

# Build IQ

if [[ "$RUNNER_OS" == "Windows" ]]; then
  cmake --build . --config Release   
else
  make -j
fi

ls

# Move to piqtree2 directory

cd ../..
mv iqtree2/build/libiqtree2.a src/piqtree2/_libiqtree/