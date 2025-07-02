#!/bin/bash

source /cvmfs/sft.cern.ch/lcg/views/LCG_107/x86_64-el9-gcc14-opt/setup.sh
cd ~/gitstuff/DualTestBeam
source ./install/bin/thisDualTestBeam.sh
cd compact

time ddsim --compactFile=DRBigEcal1.xml --runType=batch -G --steeringFile SCEPCALsteering.py --outputFile=e-_10GeV_100_BigEcal.root --part.userParticleHandler= -G --gun.position="0. 0. -1*cm" --gun.direction "0. 0. 1." --gun.energy "10*GeV" --gun.particle="e-" --outputFile=e-_10GeV_100_BigEcal.root -v VERBOSE -N 1 
