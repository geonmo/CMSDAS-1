#!/usr/bin/env python

#from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
gROOT.ProcessLine(".x tdrstyle.C")

f = TFile("/cmsdas/data/ShortEX_Muon/RelValZMM_13_GEN-SIM-RECO/6E6BF265-451A-E511-9B42-0025905B855E.root")
events = f.Get("Events")
c1 = TCanvas("cpt", "cpt", 500, 500)
events.Draw("recoMuons_muons__RECO.obj.pt()>>hpt(100, 0, 200)")
c2 = TCanvas("cmult", "cmult", 500, 500)
events.Draw("recoMuons_muons__RECO.@obj.size()>>hmult(7, 0, 7)")
