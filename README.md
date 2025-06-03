# dd4hep-rivanna

Build the container
---

```bash
cd container
source build.sh
```
This will create your contianer and link it to your ~/apptainer directory.

Build cvmfsexec
---
```bash
mkdir -p ~/GIT
cd ~/GIT
module load gcc; module load cmake;
git clone https://github.com/cvmfs/cvmfsexec
cd cvmfsexec
./makedist -s -m rhel8-x86_64 default
module unload gcc; module unload cmake;
```

Run the container
----
```bash
export SINGCVMFS_REPOSITORIES="geant4.cern.ch,sft.cern.ch"
export SINGCMD=apptainer
~/GIT/cvmfsexec/singcvmfs shell ~/apptainer/alma8.sif
```
control-d to exit.

Within the container follow the build instructions at<br>
https://gitlab.cern.ch/calvisionsimulation/DualTestBeam<br>
try using the branch: feature/no_dd4hep_build

```bash
git checkout feature/no_dd4hep_build
```
and follow the example to run the DRConly.xml geometry.
