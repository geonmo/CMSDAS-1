#!/bin/bash

OUTBASE=/store/user/jhgoh/CATTools/TTLL/v7-6-2

## real data
CMD="create-batch -g --maxFiles 50 --cfg analyze_data_cfg.py"
for D in DoubleEG_Run2015C DoubleEG_Run2015D DoubleMuon_Run2015C DoubleMuon_Run2015D MuonEG_Run2015C MuonEG_Run2015D; do
  $CMD --jobName $D --fileList dataset/dataset_$D --transferDest $OUTBASE/$D
done

## MC background
CMD="create-batch -g --maxFiles 100 --cfg analyze_bkg_cfg.py"
for D in DYJets DYJets_10to50 WJets WW WZ ZZ WWZ WZZ ZZZ SingleTbar_t SingleTbar_tW SingleTop_s SingleTop_t SingleTop_tW; do
  $CMD --jobName $D --fileList dataset/dataset_$D --transferDest $OUTBASE/$D
done

## QCD background
#QCD_DoubleEM_Pt_30to40 QCD_DoubleEM_Pt_30toInf QCD_DoubleEM_Pt_40toInf
CMD="create-batch -g --maxFiles 500 --cfg analyze_bkg_cfg.py"
for D in 15to20 20to30 30to50 50to80 80to120 120to170 170to300; do
  $CMD --jobName QCD_Pt-${D}_MuEnriched --fileList dataset/dataset_QCD_Pt-${D}_MuEnriched --transferDest $OUTBASE/QCD_Pt-${D}_MuEnriched
  $CMD --jobName QCD_Pt-${D}_EMEnriched --fileList dataset/dataset_QCD_Pt-${D}_EMEnriched --transferDest $OUTBASE/QCD_Pt-${D}_EMEnriched
done
D=300toInf_EMEnriched
$CMD --jobName QCD_Pt-${D}_EMEnriched --fileList dataset/dataset_QCD_Pt-${D}_EMEnriched --transferDest $OUTBASE/QCD_Pt-${D}_EMEnriched
for D in 300to470 470to600 600to800 800to1000 1000toInf; do
  $CMD --jobName QCD_Pt-${D}_MuEnriched --fileList dataset/dataset_QCD_Pt-${D}_MuEnriched --transferDest $OUTBASE/QCD_Pt-${D}_MuEnriched
done

## Signal MC
CMD="create-batch -g --maxFiles 20 --cfg analyze_sig_cfg.py"
for D in TT_powheg TTJets_MG5 TTJets_aMC TT_amcatnlo-herwigpp TT_powheg-herwigpp TT_powheg_pythia6; do
  $CMD --jobName $D --fileList dataset/dataset_$D --transferDest $OUTBASE/$D
done
#TT_powheg_scaledown TT_powheg_scaleup
#TTJets_scaledown TTJets_scaleup


