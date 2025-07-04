# dd4hep-rivanna

Instructions for running the CalVision DD4HEP simulations on Rivanna.

Build the container
---

```bash
cd container
./build.sh alma9
```
This will create an alma9 contianer and link it to your ~/apptainer directory.  alma8 is also an option.

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

Run the alma9 container
----
```bash
module load apptainer
export SINGCVMFS_REPOSITORIES="geant4.cern.ch,sft.cern.ch"
export SINGCMD=apptainer
~/GIT/cvmfsexec/singcvmfs shell ~/apptainer/alma9.sif
```
control-d to exit.

Build the stable version of the DualTestBeam code
----
CERN computing account required for gitlab access.

See also https://github.com/saraheno/DualTestBeam and https://foswiki.web.cern.ch/Calvision/DualCrystalDD4hep#making_digis

```bash
cd ~/GIT
source /cvmfs/sft.cern.ch/lcg/views/LCG_107/x86_64-el9-gcc14-opt/setup.sh
git clone https://gitlab.cern.ch/calvisionsimulation/DualTestBeam.git 
cd DualTestBeam/
mkdir build install
cd build
cmake -DDD4HEP_USE_GEANT4=ON -DBoost_NO_BOOST_CMAKE=ON -DDD4HEP_USE_LCIO=ON -DBUILD_TESTING=ON -DROOT_DIR=$ROOTSYS -D CMAKE_BUILD_TYPE=Release -DDD4HEP_BUILD_EXAMPLES=ON -DCMAKE_INSTALL_PREFIX=../install ..
make -j4
make install
```

Running the example: DRConly
---
Make sure you're running in your container and have the LCG release set up.

```bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_107/x86_64-el9-gcc14-opt/setup.sh
cd ~/GIT/DualTestBeam
source ./install/bin/thisDualTestBeam.sh
cd compact
# generate 5 events with verbose output to the screen
ddsim --compactFile=DRConly.xml --runType=batch -G --steeringFile SCEPCALsteering.py --outputFile=junk.root --part.userParticleHandler= -G --gun.position="0. 0. -1*cm" --gun.direction "0. 0. 1." --gun.energy "20*GeV" --gun.particle="pi-" --outputFile=junk.root -v VERBOSE -N 5 2>&1 | tee  output.log
# to run quietly
ddsim --compactFile=DRConly.xml --runType=batch -G --steeringFile SCEPCALsteering.py --outputFile=junk.root --part.userParticleHandler= -G --gun.position="0. 0. -1*cm" --gun.direction "0. 0. 1." --gun.energy "20*GeV" --gun.particle="pi-" --outputFile=junk.root -v VERBOSE -N 5 >& output.log
```
This will produce the file ```junk.root```

see: https://github.com/saraheno/DualTestBeam/blob/master/compact/massjobs.py for a guide on running the example through a script.

Example of running with Qt GUI
---
```ddsim --compactFile=./DRConly.xml --runType=qt -G --steeringFile SCEPCALsteering.py --outputFile=out.root --part.userParticleHandler='' -G --gun.position="0.,0.,-2400." --gun.direction "0 0 1" --gun.energy "10*GeV" --gun.particle="mu-"```

```
/control/execute Qt.mac
/run/beamOn 1
...
```

note: set ```QT_DEBUG_PLUGINS=1``` to debug Qt libraries if needed


Quick start to resume a working session
---
```bash
module load apptainer
export SINGCVMFS_REPOSITORIES="geant4.cern.ch,sft.cern.ch"
export SINGCMD=apptainer
~/GIT/cvmfsexec/singcvmfs shell ~/apptainer/alma9.sif
source /cvmfs/sft.cern.ch/lcg/views/LCG_107/x86_64-el9-gcc14-opt/setup.sh
cd ~/GIT/DualTestBeam
source ./install/bin/thisDualTestBeam.sh
cd compact
```
Root with TBrowser
---
```bash
root --web=off junk.root
root [1] new TBrowser()
...
```
OR
cut/paste the file URL provided with the web-based browser

```bash
root [1] new TBrowser()

ROOT comes with a web-based browser, which is now being started. 
Revert to TBrowser by setting "Browser.Name: TRootBrowser" in rootrc file or
by starting "root --web=off"
Find more info on https://root.cern/for_developers/root7/#rbrowser
Info in <THttpEngine::Create>: Starting HTTP server on port 127.0.0.1:9400
Error in <THttpEngine::Log>: cannot bind to 127.0.0.1:9400: 98 (Address already in use)
Info in <THttpEngine::Create>: Starting HTTP server on port 127.0.0.1:9495
gio: file:///tmp/root_start_RDDKJD.html: Failed to find default application for content type ?text/plain?
```

see https://github.com/saraheno/DualTestBeam/blob/master/compact/Resolution.C for analysis code

Looking at the geometry
---
```
~/GIT/cvmfsexec/singcvmfs shell ~/apptainer/alma9.sif
source /cvmfs/sft.cern.ch/lcg/views/LCG_107/x86_64-el9-gcc14-opt/setup.sh
cd ~/GIT/DualTestBeam
source ./install/bin/thisDualTestBeam.sh
cd compact
geoDisplay DRConly.xml
```
When ROOT starts lok for a message like this:
```
root [0] gio: file:///tmp/root_start_oxP9Wo.html: Failed to find default application for content type ?text/plain?
```
cut/paste the file URL into your web browser to see the geometry display.  <br>
To do: figure out how to fix this mime type issue in the Rivanna virtual desktop.

Running CrystalAna.C
---
```
cd compact
root -l
```
When root starts, load and run CrystalAna.C as follows:
```
.L CrystalAna.C
crystalana(100,"junk.root",20,1,1,0,1,"hist.root")
```
Then quit and run hist.root in a TBrowser():
```
.q
root hist.root
new TBrowser()
```

Links
-----
*  [DD4hep Guide for Young Students](https://docs.google.com/document/d/1J1Qx08Ozn8g4XEAypybaJbVPWNe5J576tK-5u2ouMt4/edit?usp=sharing)


Git cheatsheet
--------------
* view remote branches: ```git branch -r```
* checkout/activate remote branch: ```git checkout -b fwdsegmentation origin/fwdsegmentation```

