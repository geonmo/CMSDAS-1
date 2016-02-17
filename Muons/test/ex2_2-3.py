#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
from math import *
gROOT.ProcessLine(".x .rootlogon.C")

#files = ["file:/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root",]
signal_file = TFile("iso.root")
bkg_file    = TFile("iso_bkg.root")

sig_nt = signal_file.Get("ntuple")
bkg_nt = bkg_file.Get("ntuple")

sig_hist = TH1F("roc_sig","ROC curve for DY sample; iso value ; # of entries",100,0,1.0)
bkg_hist = TH1F("roc_bkg","ROC curve for QCD sample; iso value ; # of entries",100,0,1.0)

sig_nt.Project("roc_sig","relIso")
bkg_nt.Project("roc_bkg","relIso")

c1 = TCanvas("c1","c1")
sig_hist.SetLineColor(kBlue)
sig_hist.Draw()
bkg_hist.SetLineColor(kRed)
bkg_hist.Draw("same")
sig_hist.SetTitle("Overlay plot ; iso value ; # of entries")
c1.SetLogy()

c1.SaveAs("roc.png")

c2 = TCanvas("c2","c2")
sum_hist = sig_hist.Clone()
sig_histC = sig_hist.Clone()

sig_histC.Sumw2()
bkg_hist.Sumw2()
sum_hist.Sumw2()
sum_hist.Add( bkg_hist)

sig_histC.Divide(sum_hist)
sig_histC.Draw()
c2.SaveAs("eff.png")


