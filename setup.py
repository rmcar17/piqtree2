"""setup for piqtree2."""

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

LIBRARY_DIR = "src/piqtree2/_libiqtree"

ext_modules = [
    Pybind11Extension(
        "_piqtree2",
        ["src/piqtree2/_libiqtree/_piqtree2.cpp"],
        library_dirs=[LIBRARY_DIR, "/opt/homebrew/opt/libomp/lib"],
        include_dirs=["/opt/homebrew/opt/libomp/include"],
        libraries=["iqtree2", "z", "libomp"],
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
