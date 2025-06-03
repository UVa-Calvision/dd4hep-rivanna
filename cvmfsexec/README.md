Build cvmfsexec
===============

module load gcc; module load cmake; 
git clone https://github.com/cvmfs/cvmfsexec
cd cvmfsexec
./makedist -m rhel8-x86_64 default

module unload gcc; module unload cmake;

