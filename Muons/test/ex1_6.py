#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
from math import *
gROOT.ProcessLine(".x .rootlogon.C")

#files = ["file:/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root",]
files = ["file:dymm.root",]

events = Events(files)
genParticleHandle = Handle("std::vector<reco::GenParticle>")
muonHandle = Handle('std::vector<pat::Muon>')
for event in events:
    event.getByLabel("prunedGenParticles", genParticleHandle)
    genParticles = genParticleHandle.product()

    event.getByLabel('slimmedMuons', muonHandle)
    muons = muonHandle.product()

    for genP in genParticles:
        if abs(genP.pdgId()) != 13: continue ## Generator level muons only

        matchedMuon = None
        drMin = 0.5
        for iMuon, mu in enumerate(muons):
            dr = sqrt( (mu.eta()-genP.eta())**2 + (mu.phi()-genP.phi())**2 )
            if dr < drMin:
                drMin = dr
                matchedMuon = mu
        
        if matchedMuon != None:
            print  "gen muon (pt=%f eta=%f phi=%f) is matched to pat muon (pt=%f eta=%f phi=%f)" % (genP.pt(), genP.eta(), genP.phi(), matchedMuon.pt(), matchedMuon.eta(), matchedMuon.phi())

