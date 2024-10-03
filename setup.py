"""setup for piqtree2."""

import pathlib
import platform

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

LIBRARY_DIR = "src/piqtree2/_libiqtree"

if platform.system() == "Windows":
    src = pathlib.Path(LIBRARY_DIR) / "libiqtree2.a"
    dest = pathlib.Path(LIBRARY_DIR) / "iqtree.lib"
    if src.exists():
        src.rename(dest)

ext_modules = [
    Pybind11Extension(
        "_piqtree2",
        ["src/piqtree2/_libiqtree/_piqtree2.cpp"],
        library_dirs=[LIBRARY_DIR],
        libraries=["iqtree2", "z"],
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
