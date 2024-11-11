import os
import subprocess


while len(a_files := list(filter(lambda x: x.endswith(".a"),os.listdir()))) > 0: 
    print(a_files)
    for file in a_files:
        subprocess.check_output(["ar", "x", file])
        os.remove(file)