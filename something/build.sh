#!/bin/bash

# Define variables
srcfolder="src"
mainfile="main.cpp"
output="main"

# Compile the C++ source file
gcc -o ${srcfolder}/$output ${srcfolder}/$mainfile

# Run the compiled program (optional)
# ./${srcfolder}/$output
