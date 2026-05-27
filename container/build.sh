#!/bin/bash

usage()
{
cat <<!EOF!
Usage: build.sh [-hf] [target]
   -h: print this message and exit
   -f: force rebuild on contianer
   target = name of sif file to build [alma8, alma9*, alma9noX]
!EOF!
    exit
} >&2

# default build
TAINER=alma9

for arg in "$@"; do
    if [ "$arg" = "-h" ]; then
	usage
    elif [ "$arg" = "-f" ]; then
	FLAG="-F"
	echo "forcing rebuild of container"
    else
        TAINER=${arg%.*} # truncate .def if present
    fi    
done


TGT=${TAINER}.sif
DEF=${TAINER}.def

echo "=== attempting to build $DEF ==="

thishost=`hostname -a`
if [[ "$thishost" == *"hpc.virginia.edu"* ]]; then
  echo "Building for UVa HPC"
  module load apptainer
else
  echo "Using native apptainer"
fi

apptainer build $FLAG $TGT $DEF
mkdir -p ~/apptainer
ln -sf $PWD/$TGT ~/apptainer/


