#!/bins/bash

TGT=alma8.sif
DEF=alma8.def

if [ -f $TGT ]; then
    echo $TGT exits
    echo rm $TGT \# to rebuild
    echo $0 | grep bash > /dev/null && return ; exit
fi

module load apptainer
apptainer build $TGT $DEF
ln -sf $PWD/alma8.sif ~/apptainer/


