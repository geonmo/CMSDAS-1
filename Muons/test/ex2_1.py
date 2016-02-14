#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
from math import *
gROOT.ProcessLine(".x .rootlogon.C")

#files = ["file:/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root",]
files = ["file:dymm.root",]

f = TFile("id.root", "recreate")
ntuple = TNtupleD("ntuple", "ntuple", "pt:eta:chi2:nValidMuonHit:nStation:chi2LPos:trkKink:trkFrac:nValidPix:nTrkLayer:dxy:dz:segCompat")

events = Events(files)
genParticleHandle = Handle("std::vector<reco::GenParticle>")
muonHandle = Handle('std::vector<pat::Muon>')
vertexHandle = Handle("std::vector<reco::Vertex>")
for event in events:
    event.getByLabel("offlineSlimmedPrimaryVertices", vertexHandle)
    vertices = vertexHandle.product()
    if vertices.size() == 0: continue
    vertex = vertices.at(0)

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
        if mu.pt() < 20 or abs(mu.eta()) > 2.5: continue

        if 'dymm' in files[0]:
            isGenMatched = False
            for gen in genMuons:
                dr = sqrt( (mu.eta()-gen.eta())**2 + (mu.phi()-gen.phi())**2 )
                if dr < 0.1:
                    isGenMatched = True
                    break
            if not isGenMatched: continue

        trkVars = [-999., -999., -999.]
        if mu.isTrackerMuon() and mu.innerTrack() != None:
            trk = mu.innerTrack()
            hit = trk.hitPattern()
            trkVars = [trk.validFraction(), hit.numberOfValidPixelHits(), hit.trackerLayersWithMeasurement()]

        glbVars = [-999., -999.]
        if mu.isGlobalMuon() and mu.globalTrack() != None:
            glb = mu.globalTrack()
            hit = glb.hitPattern()
            glbVars = [glb.normalizedChi2(), hit.numberOfValidMuonHits()]

        dxy, dz = -999, -999
        if mu.muonBestTrack() != None:
            dxy = abs(mu.muonBestTrack().dxy(vertex.position()))
            dz  = abs(mu.muonBestTrack().dz(vertex.position()))

        muQual = mu.combinedQuality()

        ntuple.Fill(mu.pt(), mu.eta(),
                    glbVars[0], glbVars[1], mu.numberOfMatchedStations(),
                    muQual.chi2LocalPosition, muQual.trkKink,
                    trkVars[0], trkVars[1], trkVars[2],
                    dxy, dz,
                    mu.segmentCompatibility())

f.cd()
ntuple.Write()
f.Close()

