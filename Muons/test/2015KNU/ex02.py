#!/usr/bin/env python

#from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
gROOT.ProcessLine(".x tdrstyle.C")

f = TFile("/cmsdas/data/ShortEX_Muon/RelValZMM_13_MINIAODSIM/0AF36725-FB1A-E511-BCB2-0025905A497A.root")
# f = TFile("/store/relval/CMSSW_7_4_6/RelValZMM_13/MINIAODSIM/PU50ns_MCRUN2_74_V8-v2/00000/0AF36725-FB1A-E511-BCB2-0025905A497A.root")
events = f.Get("Events")
c1 = TCanvas("cpt", "cpt", 500, 500)
events.Draw("patMuons_slimmedMuons__PAT.obj.pt()>>hpt(100, 0, 200)")
c2 = TCanvas("cmult", "cmult", 500, 500)
events.Draw("patMuons_slimmedMuons__PAT.@obj.size()>>hmult(7, 0, 7)")
