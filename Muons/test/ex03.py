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
    for iMuon, muon in enumerate(muonHandle.product()):
        print '  ', iMuon, 'th muon pt=', muon.pt()
