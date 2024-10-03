echo $BOOST_ROOT
echo $RUNNER_OS

choco install -y llvm --version=14.0.6 --allow-downgrade
choco install -y eigen

bash build_tools/build_iqtree.sh