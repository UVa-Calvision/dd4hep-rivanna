#!/usr/bin/env python3

from array import *
import argparse, sys, os
from pathlib import Path

# local definitions
container='~/apptainer/alma9.sif'
homeDir = os.path.expanduser( '~' )
gitDir = f'{homeDir}/GIT'
dd4Dir = f'{gitDir}/DualTestBeam'
xmlDir = f'{dd4Dir}/compact'
jobDir = f'{homeDir}/slurm'
outDir = f'{homeDir}/ddsimout'
lcgRelease='/cvmfs/sft.cern.ch/lcg/views/LCG_107/x86_64-el9-gcc14-opt/setup.sh'
steeringFile='SCEPCALsteering.py'

argParser = argparse.ArgumentParser(
    description='slurm file generator for Rivanna',
    epilog='Example usage:./runjobs.py -g DRBigEcal2.xml')
argParser.add_argument("-g", "--geometry", type=str, help="geometry code (required)")
argParser.add_argument("-N", "--nevt", type=int, default=10, help="number of events [10]")
argParser.add_argument("-j", "--njobs", type=int, default=1, help="number or jobs [1]")
argParser.add_argument("-d", "--direction", default=0, help='beam direction [0="0.0 0.0 1.0"]')
argParser.add_argument("-o", "--origin", default=0, help='beam origin [0="0.*cm 0.*cm -1*cm"]')
argParser.add_argument("-p", "--particle", default='e-', help='particle type [e-]')
argParser.add_argument('-E','--elist', nargs='*', default=[10], help='list of energies to run in GeV, usage eg. -E 10 20 30')
argParser.add_argument('-r','--runname', default=None, help='optional run name for file names')
argParser.add_argument('-R','--reponame', default=None, help='use alternate GIT repo for dd4sim')

args = argParser.parse_args()
print("args=%s" % args)

if args.geometry == None:
    print("Geometry file missing")
    sys.exit(1)

if args.reponame:
    dd4Dir = f'{gitDir}/{args.reponame}'
    if not os.path.exists(dd4Dir):
        print(f'{dd4Dir} does not exist')
        sys.exit(1)

print(f'Using DualTestBeam repo: {dd4Dir}')
    
# beam direction (improve these settings)
beamDir="0. 0. 1." # default
if args.direction=="1" :
    beamDir="0. 0.05 0.99875" # fiber angle
    
# beam origin (improve these settings)
beamOrigin="0. 0.*mm -1*cm" #default
if args.origin=="1" :
    beamOrigin="0.,-7*mm,-1*mm"
if args.origin=="2" :
    beamOrigin="0. 0.*mm -80*cm"
    
    
geofile=Path(args.geometry).with_suffix('')
print("Running geometry:",geofile)
# geo definition for all jobs
compactFile=f'{geofile}.xml'

if not os.path.exists(jobDir):
    print("Creating job def directory",jobDir)
    os.mkdir(jobDir)

if not os.path.isdir(outDir):
    print("Creating output directory",outDir)
    os.mkdir(outDir)



os.chdir(xmlDir)
if not os.path.exists(compactFile) or not os.path.exists(steeringFile):
    print("geometry or steering file is missing")
    sys.exit(1)
    
for e in args.elist:
    print(f'building job for E = {e} GeV {args.particle}')
    for n in range(args.njobs):
        jobName=f'{geofile}_{e}_GeV_{args.particle}_{args.nevt}_evt_job{n:02d}'
        if args.runname: jobName=f'{jobName}-{args.runname}'
        outFile=f'{outDir}/{jobName}.root'
        print(f'replica {n}, job name: {jobName}')
        slurmJob=f'{jobDir}/{jobName}_slurm.sh'
        ddsimJob=f'{jobDir}/{jobName}.sh'

        # build scripts like a bash Here Documents        
        slurmCmd=f'''#!/bin/bash
#SBATCH --time=3:00:00   # job time limit
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=1   # number of tasks per node
#SBATCH --cpus-per-task=1   # number of CPU cores per task
#SBATCH --partition=standard   # partition
#SBATCH -J "{jobName}"   # job name
#SBATCH --constraint=rivanna   # cluster
#SBATCH -o "{outDir}/{jobName}.log"
#SBATCH --account=cmsexo   # allocation name
#SBATCH --mem=8G 

echo $PWD
module load apptainer
export SINGCVMFS_REPOSITORIES="geant4.cern.ch,sft.cern.ch"
export SINGCMD=apptainer
chmod +x {ddsimJob}
~/GIT/cvmfsexec/singcvmfs exec {container} {ddsimJob}
'''
        ddsimCmd=f'''#!/bin/bash
echo "Job running on:" `hostname`
echo "Start Time" `date`
cd {xmlDir}
source {lcgRelease}
source {dd4Dir}/install/bin/thisDualTestBeam.sh 
time ddsim -N {args.nevt} \
--compactFile={compactFile} --steeringFile={steeringFile} --runType=batch \
--outputFile={outFile} --part.userParticleHandler='' \
-G --gun.position="{beamOrigin}" --gun.direction "{beamDir}" \
--gun.energy "{e}*GeV" --gun.particle="{args.particle}"
exitcode=$?
echo "End Time" `date`
echo "exitcode: $exitcode"
'''
        
        with open(slurmJob, 'w') as f:
            f.write(slurmCmd)
        with open(ddsimJob, 'w') as f:
            f.write(ddsimCmd)  

        os.system(f'echo sbatch {slurmJob}')
        os.system(f'sbatch {slurmJob}')
