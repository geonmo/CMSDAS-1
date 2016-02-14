#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
gROOT.ProcessLine(".x .rootlogon.C")

h = TH1F("h", "h;Mass (GeV);Events per 2GeV", 50, 50, 150)

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
    print "Leading pt, eta, phi, charge = ", (muon1.pt(), muon1.eta(), muon1.phi(), muon1.charge())
    print "Trailing pt, eta, phi, charge = ", (muon2.pt(), muon2.eta(), muon2.phi(), muon2.charge())
    zLVec = muon1.p4()+muon2.p4()
    print "Dilepton invariant mass = ", zLVec.mass()
    h.Fill(zLVec.mass())

h.Draw()
