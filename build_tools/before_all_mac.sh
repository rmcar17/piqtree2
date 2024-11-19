brew update
brew install eigen boost gcc libomp

echo "Here"
echo $LDFLAGS
echo $CPPFLAGS
echo "There"

export LDFLAGS="-L/opt/homebrew/opt/libomp/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libomp/include"

bash build_tools/build_iqtree.sh