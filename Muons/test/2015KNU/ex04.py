#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
gROOT.ProcessLine(".x tdrstyle.C")

files = [
    "file:/cmsdas/data/ShortEX_Muon/RelValZMM_13_MINIAODSIM/0AF36725-FB1A-E511-BCB2-0025905A497A.root",
    #"/store/relval/CMSSW_7_4_6/RelValZMM_13/MINIAODSIM/PU50ns_MCRUN2_74_V8-v2/00000/0AF36725-FB1A-E511-BCB2-0025905A497A.root",
]

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
