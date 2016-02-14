#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
from array import *
gROOT.ProcessLine(".x .rootlogon.C")

f = TFile("hist.root", "recreate")
tree = TNtupleD("ntuple", "ntuple", "mu1_pt:mu2_pt:mu1_eta:mu2_eta:z_m")

#files = ["file:/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root",]
files = ["file:dymm.root",]

events = Events(files)
muonHandle = Handle('std::vector<pat::Muon>')
for iEvent, event in enumerate(events):
    print 'Analyzing', iEvent, 'th event'
    event.getByLabel('slimmedMuons', muonHandle)
    muons = muonHandle.product()
    if muons.size() < 2: continue
    muon1, muon2 = muons[0], muons[1]
    if muon2.pt() <= 1: continue
    zLVec = muon1.p4()+muon2.p4()

    tree.Fill(muon1.pt(), muon2.pt(), muon1.eta(), muon2.eta(), zLVec.mass())

f.cd()
tree.Write()
f.Close()
