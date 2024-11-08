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
    Recursively extract all object files from any nested .a archives and return
    a list of all the .obj files found in the process.
    """
    files_to_extract = [library_path]  # Start with the given .a file

    # Keep track of the files we've already extracted to prevent processing the same .a file
    extracted_files = set()
    extracted_obj_files = []  # List to store all extracted .obj files

    while files_to_extract:
        current_file = files_to_extract.pop()

        # Only extract if it's a .a file and hasn't been processed yet
        if current_file.endswith(".a") and current_file not in extracted_files:
            print(f"Extracting {current_file}...")

            # Add this .a file to the set to prevent processing it again
            extracted_files.add(current_file)

            # Extract the .obj files using 'ar x' command (this modifies the current directory)
            os.system(f'ar x {current_file}')

            # Add all .obj files in the current directory to the list
            extracted_obj_files.extend([f for f in os.listdir('.') if f.endswith('.obj') or f.endswith(".o")])

            # Now check if any newly extracted files are .a files (nested archives)
            nested_a_files = [f for f in os.listdir('.') if f.endswith('.a') and f not in extracted_files]
            files_to_extract.extend(nested_a_files)

            # Print the newly extracted files for debugging
            print(f"Found nested .a files: {nested_a_files}")

    # Return the list of all extracted .obj files
    return extracted_obj_files



class CustomBuildExt(distutils_build_ext):
    def initialize_options(self):
        # Ensure the build_ext options are initialized properly
        super().initialize_options()

    def run(self):
        # If on Windows, handle the conversion of .a to .lib
        if sys.platform == 'win32':
            if os.path.exists(MINGW_LIB):
                print(f"Found {MINGW_LIB}. Converting it to .lib...")

                # Recursively extract all .obj files from the .a and nested .a files
                extracted_obj_files = extract_all_a_files(MINGW_LIB)

                # Ensure we have .obj files before proceeding
                if not extracted_obj_files:
                    print("No object files (.obj) found after extraction!")
                    sys.exit(1)

                # Create the .lib file using MSVC's 'lib' tool, naming it iqtree2.lib
                print("Creating iqtree2.lib from .obj files...")
                os.system(f'lib /out:{LIBRARY_DIR}/iqtree2.lib {" ".join(extracted_obj_files)}')

                # Debug output for checking extracted files
                print("Outfiles:", os.listdir(LIBRARY_DIR))
                print("Outfiles 1:", os.listdir(LIBRARY_DIR + "/.."))
                print("Outfiles 2:", os.listdir(LIBRARY_DIR + "/../.."))
                print("Outfiles 3:", os.listdir(LIBRARY_DIR + "/../../.."))

                # Clean up the extracted .obj files
                for obj in extracted_obj_files:
                    if os.path.exists(obj):
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
