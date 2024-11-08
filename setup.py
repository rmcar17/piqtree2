import platform
import os
import sys
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
from distutils.command.build_ext import build_ext as distutils_build_ext

LIBRARY_DIR = "src/piqtree2/_libiqtree"
MINGW_LIB = os.path.join(LIBRARY_DIR, "libiqtree2.a")  # Path to your MinGW .a file

class CustomBuildExt(distutils_build_ext):
    def run(self):
        if sys.platform == 'win32':
            # If using MinGW on Windows, handle the .a to .lib conversion
            if os.path.exists(MINGW_LIB):
                # Extract object files from the .a file
                if not os.path.exists("libiqtree2.o"):
                    print(f"Extracting object files from {MINGW_LIB}...")
                    os.system(f'ar x {MINGW_LIB}')  # Use 'ar' from MinGW to extract .o files
                
                # Convert the extracted .o files into a .lib file using MSVC's 'lib' tool
                print("Creating libiqtree2.lib from .o files...")
                os.system('lib /out:libiqtree2.lib *.o')

                # Clean up the extracted .o files
                for obj in os.listdir('.'):
                    if obj.endswith('.o'):
                        os.remove(obj)

                # Now the build process will use the libiqtree2.lib file
                self.compiler.library_dirs.append(LIBRARY_DIR)
                self.compiler.libraries.append('iqtree2')

        # Continue with the standard build process
        super().run()

# Define the extension with pybind11
ext_modules = [
    Pybind11Extension(
        "_piqtree2",
        ["src/piqtree2/_libiqtree/_piqtree2.cpp"],
        library_dirs=[LIBRARY_DIR],
        libraries=["iqtree2"] + ([] if platform.system() != "Windows" else ["z"]),
    ),
]

# Setup call
setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": CustomBuildExt},  # Use our custom build_ext class
    zip_safe=False,
)
