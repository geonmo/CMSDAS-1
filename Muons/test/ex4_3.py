#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
from math import *
import ctypes
gROOT.ProcessLine(".x .rootlogon.C")
gSystem.CompileMacro("rochcor/muresolution_run2.cc", "k")
gSystem.CompileMacro("rochcor/rochcor2015.cc", "k")
mucor = rochcor2015()

#files = ["file:/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root",]
files = ["file:dymm.root",]

hRawMuRes = TH1D("hRawMuRes", "reconstructed muon;1/pT residual;Events", 100, -1, 1);
hCorMuRes = TH1D("hCorMuRes", "corrected muon;1/pT residual;Events", 100, -1, 1);

events = Events(files)
muonHandle = Handle('std::vector<pat::Muon>')
vertexHandle = Handle("std::vector<reco::Vertex>")
genHandle = Handle('std::vector<reco::GenParticle>')
for event in events:
    event.getByLabel('prunedGenParticles', genHandle)
    genParticles = genHandle.product()
    genMuons = []
    for gen in genParticles:
        if abs(gen.pdgId()) != 13 or gen.pt() < 20 or abs(gen.eta()) > 2.4: continue

        genMuons.append(gen)
    if len(genMuons) < 1: continue

    event.getByLabel("offlineSlimmedPrimaryVertices", vertexHandle)
    vertices = vertexHandle.product()
    if vertices.size() == 0: continue
    vertex = vertices.at(0)

    event.getByLabel('slimmedMuons', muonHandle)
    muons = muonHandle.product()
    selMuons = []
    for mu in muons:
        if not mu.isTightMuon(vertex): continue
        if mu.pt() < 20 or abs(mu.eta()) > 2.4: continue

        matchedDR = 1e9
        matchedGen = None
        for gen in genMuons:
           dr = sqrt( (gen.eta()-mu.eta())**2 + (gen.phi()-mu.phi())**2 )
           if dr < matchedDR: marchedDR, matchedGen = dr, gen
        if matchedGen != None: selMuons.append((mu, matchedGen))

    if len(selMuons) < 1: continue

    recMu, genMu = selMuons[0]
    corMu = TLorentzVector(recMu.px(), recMu.py(), recMu.pz(), recMu.energy())
    qter = ctypes.c_float(1.0) # From Higgs group to do uncertainty propagation
    mucor.momcor_mc(corMu, recMu.charge(), 0, qter);
    #mucor.moncor_data(corMu, recMu.charge(), 0, qter); # Fo the data

    hRawMuRes.Fill( (1./recMu.pt()-1./genMu.pt())/(1./genMu.pt()) )
    hCorMuRes.Fill( (1./corMu.Pt()-1./genMu.pt())/(1./genMu.pt()) )

hRawMuRes.Draw()
