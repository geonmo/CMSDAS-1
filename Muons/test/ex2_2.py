#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
from math import *
gROOT.ProcessLine(".x .rootlogon.C")

#files = ["file:/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root",]
files = ["file:dymm.root",]

f = TFile("iso.root", "recreate")
ntuple = TNtupleD("ntuple", "ntuple", "nvtx:pt:eta:chIso:nhIso:phIso:puIso:relIso:relIsoRaw")

events = Events(files)
genParticleHandle = Handle("std::vector<reco::GenParticle>")
muonHandle = Handle('std::vector<pat::Muon>')
vertexHandle = Handle("std::vector<reco::Vertex>")
for event in events:
    event.getByLabel("offlineSlimmedPrimaryVertices", vertexHandle)
    vertices = vertexHandle.product()
    if vertices.size() == 0: continue
    vertex = vertices.at(0) ## Need vertex selection to be precise...

    event.getByLabel('slimmedMuons', muonHandle)
    muons = muonHandle.product()

    ## Require gen matching for signal
    genMuons = []
    if 'dymm' in files[0]:
        event.getByLabel("prunedGenParticles", genParticleHandle)
        genParticles = genParticleHandle.product()
        for genP in genParticles:
            if abs(genP.pdgId()) == 13: genMuons.append(genP)

    for mu in muons:
        if not mu.isPFMuon(): continue
        if not mu.isTightMuon(vertex): continue
        if mu.pt() < 20 or abs(mu.eta()) > 2.5: continue

        if 'dymm' in files[0]:
            isGenMatched = False
            for gen in genMuons:
                dr = sqrt( (mu.eta()-gen.eta())**2 + (mu.phi()-gen.phi())**2 )
                if dr < 0.1:
                    isGenMatched = True
                    break
            if not isGenMatched: continue

        chIso = mu.chargedHadronIso()
        nhIso = mu.neutralHadronIso()
        phIso = mu.photonIso()
        puIso = mu.puChargedHadronIso()

        ntuple.Fill(vertices.size(), mu.pt(), mu.eta(),
                    chIso, nhIso, phIso, puIso,
                    (chIso+max(0.,nhIso+phIso-0.5*puIso))/mu.pt(),
                    (chIso+nhIso+phIso)/mu.pt())

f.cd()
ntuple.Write()
f.Close()

