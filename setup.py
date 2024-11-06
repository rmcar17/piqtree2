"""setup for piqtree2."""

import platform

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

LIBRARY_DIR = "src\\piqtree2\\_libiqtree"

ext_modules = [
    Pybind11Extension(
        "_piqtree2",
        ["src\\piqtree2\\_libiqtree\\_piqtree2.cpp"],
        include_dirs=["vcpkg\\installed\\x64-windows-static\\include", "iqtree2\\build", "iqtree2", "iqtree2\\yaml-cpp\\include"],
        library_dirs=[LIBRARY_DIR, "vcpkg\\installed\\x64-windows-static\\lib"],
        libraries=["iqtree2", "zlib" if platform.system() == "Windows" else "z"],
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
