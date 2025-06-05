#!/bin/bash

usage()
{
cat <<!EOF!
Usage: build.sh [-hf] [target]
   -h: print this message and exit
   -f: force rebuild on contianer
   target = name of sif file to build [alma8*, alma9]
!EOF!
    exit
} >&2

TAINER=alma8

for arg in "$@"; do
    if [ "$arg" = "-h" ]; then
	usage
    elif [ "$arg" = "-f" ]; then
	FLAG="-F"
	echo "forcing rebuild of container"
    else
        TAINER=$arg
    fi    
done


TGT=${TAINER}.sif
DEF=${TAINER}.def

echo "=== attempting to build $DEF ==="

module load apptainer
apptainer build $FLAG $TGT $DEF 
mkdir -p ~/apptainer
ln -sf $PWD/$TGT ~/apptainer/


