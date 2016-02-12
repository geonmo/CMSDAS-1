# 2016 Top quark analysis at CMSDASia @ NTU
This analysis is aiming to measure the top quark mass in dilepton channel.
Overview on the analysis can be found from the school's web pages.

https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSDataAnalysisSchoolNTU2016TopExercise

In this exercise, we will measure the top quark mass using one of the alternative methods in CMS.
The example given in this school is synchronized to the one given at LPC, but we can extend
to other method if we have enough person-power.

## Setup workspace
First start from setting up your workspace.
We will be based on the analysis framework developed for the top quark analysis.
Specific configuration files for this school are available under the 
CMSDAS/TopQuarkAnalysis directory.

```bash
cmsrel CMSSW_7_6_3_patch2
cd CMSSW_7_6_3_patch2/src
cmsenv

git-cms-init
git clone https://github.com/vallot/CATTools
git clone https://github.com/cms-kr/CMSDAS

scram b -j8
```

