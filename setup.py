import platform
import os
import sys
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
from distutils.command.build_ext import build_ext as distutils_build_ext

LIBRARY_DIR = "src/piqtree2/_libiqtree"
MINGW_LIB = os.path.join(LIBRARY_DIR, "libiqtree2.a")  # Path to your MinGW .a file

class CustomBuildExt(distutils_build_ext):
    def initialize_options(self):
        # Ensure the build_ext options are initialized properly
        super().initialize_options()

    def run(self):
        # If on Windows, handle the conversion of .a to .lib
        if sys.platform == 'win32':
            if os.path.exists(MINGW_LIB):
                print(f"Found {MINGW_LIB}. Converting it to .lib...")

                # Extract object files from the .a file using 'ar' from MinGW
                print(f"Extracting object files from {MINGW_LIB}...")
                os.system(f'ar x {MINGW_LIB}')  # Extract the object files

                # Create the .lib file using MSVC's 'lib' tool, naming it iqtree2.lib
                print("Creating iqtree2.lib from .o files...")
                os.system(f'lib /out:{LIBRARY_DIR}/iqtree2.lib *.o')  # Specify the full path to create iqtree2.lib in LIBRARY_DIR

                print("Outfiles", os.listdir(LIBRARY_DIR))
                print("Outfiles 1", os.listdir(LIBRARY_DIR) / "..")
                print("Outfiles 2", os.listdir(LIBRARY_DIR) / "../..")
                print("Outfiles 3", os.listdir(LIBRARY_DIR) / "../../..")
                # Clean up the extracted .o files
                for obj in os.listdir('.'):
                    if obj.endswith('.o'):
                        os.remove(obj)

                # Now the build process will use the iqtree2.lib file
                # Ensure the library_dirs and libraries are updated correctly
                self.library_dirs.append(LIBRARY_DIR)
                self.libraries.append('iqtree2')

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
