import platform
import os
import sys
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
from distutils.command.build_ext import build_ext as distutils_build_ext

LIBRARY_DIR = "src/piqtree2/_libiqtree"
MINGW_LIB = os.path.join(LIBRARY_DIR, "libiqtree2.a")  # Path to your MinGW .a file

def extract_all_a_files(library_path):
    """
    Recursively extract all object files from any nested .a archives.
    """
    files_to_extract = [library_path]

    # Keep track of the files we've already extracted
    extracted_files = set()

    while files_to_extract:
        current_file = files_to_extract.pop()

        # Only extract if it's a .a file and hasn't been processed yet
        if current_file.endswith(".a") and current_file not in extracted_files:
            print(f"Extracting {current_file}...")

            # Extract the .o files using 'ar x'
            os.system(f'ar x {current_file}')

            # Add the .o files to the list to pass to MSVC's 'lib' tool
            extracted_files.update([f for f in os.listdir('.') if f.endswith('.o')])

            # Now check if any newly extracted files are .a files (nested archives)
            nested_a_files = [f for f in os.listdir('.') if f.endswith('.a') and f not in extracted_files]
            files_to_extract.extend(nested_a_files)

            # Print the newly extracted files
            print(f"Found nested .a files: {nested_a_files}")

    return extracted_files

class CustomBuildExt(distutils_build_ext):
    def initialize_options(self):
        # Ensure the build_ext options are initialized properly
        super().initialize_options()

    def run(self):
        # If on Windows, handle the conversion of .a to .lib
        if sys.platform == 'win32':
            if os.path.exists(MINGW_LIB):
                print(f"Found {MINGW_LIB}. Converting it to .lib...")

                # Recursively extract all .o files from the .a and nested .a files
                extracted_object_files = extract_all_a_files(MINGW_LIB)

                # Ensure we have .o files before proceeding
                if not extracted_object_files:
                    print("No object files (.o) found after extraction!")
                    sys.exit(1)

                # Create the .lib file using MSVC's 'lib' tool, naming it iqtree2.lib
                print("Creating iqtree2.lib from .o files...")
                os.system(f'lib /out:{LIBRARY_DIR}/iqtree2.lib {" ".join(extracted_object_files)}')

                # Debug output for checking extracted files
                print("Outfiles", os.listdir(LIBRARY_DIR))
                print("Outfiles 1", os.listdir(LIBRARY_DIR + "/..") )
                print("Outfiles 2", os.listdir(LIBRARY_DIR + "/../..") )
                print("Outfiles 3", os.listdir(LIBRARY_DIR + "/../../..") )

                # Clean up the extracted .o files
                for obj in extracted_object_files:
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
