brew update
brew install eigen boost gcc libomp cmake

echo "Here"
echo $LDFLAGS
echo $CPPFLAGS
ls /opt/homebrew/lib/libomp*
ls /opt/homebrew/opt/libomp/lib
echo "There"

export LDFLAGS="-L/opt/homebrew/opt/libomp/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libomp/include"

bash build_tools/build_iqtree.sh