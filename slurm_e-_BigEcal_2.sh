#!/bin/bash

#SBATCH --time=0:15:00   # job time limit
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=1   # number of tasks per node
#SBATCH --cpus-per-task=1   # number of CPU cores per task
#SBATCH --partition=standard   # partition
#SBATCH -J "ddsim_e-_10GeV_BigEcal"   # job name
#SBATCH --constraint=rivanna   # cluster
#SBATCH --account=cmsexo   # allocation name

#SBATCH --output=e-_10GeV_100_BigEcal.log

cd /home/nqk9sv/gitstuff/DualTestBeam/compact

module load apptainer
export SINGCVMFS_REPOSITORIES="geant4.cern.ch,sft.cern.ch"
export SINGCMD=apptainer

~/GIT/cvmfsexec/singcvmfs exec ~/apptainer/alma9.sif ~/gitstuff/DualTestBeam/compact/LoadCont_e-_BigEcal.sh
