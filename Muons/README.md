# CMSDAS @ NTU Muon exercise

Computing setup for CMSDAS@NTU
  * https://twiki.cern.ch/twiki/bin/view/CMSPublic/ComputingSetUpForTaipeiCMSDASia

```bash
ssh -Y ntugrid1.phys.ntu.edu.tw
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc491
export CMSSW_GIT_REFERENCE=/cvmfs/cms.cern.ch/cmssw.git.daily

cd ~
mkdir -p CMSDAS2016/MuonExercise
cd CMSDAS2016/MuonExercise
cmsrel CMSSW_7_6_3_patch2
cd CMSSW_7_6_3_patch2/src
cmsenv

git-cms-init
git clone https://github.com/cms-kr/CMSDAS -b Muon
scram b -j 8
cd CMSDAS/Muons/test
```
