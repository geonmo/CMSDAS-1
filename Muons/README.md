ssh -Y cluster902.knu.ac.kr
mkdir MuonExercise
cmsrel CMSSW_7_4_7_patch2
cd CMSSW_7_4_7_patch2/src
cmsenv
git-cms-init
# This step may take 5 min depending on network speed
git clone https://github.com/cms-kr/CMSDAS
scram b -j 8
cd CMSDAS/Muons/test
