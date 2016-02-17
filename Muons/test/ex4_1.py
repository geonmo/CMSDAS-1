#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
from math import *
gROOT.ProcessLine(".x .rootlogon.C")

#files = ["file:/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root",]
files = ["file:dymm.root",]

f = TFile("hZmass.root", "recreate")
f.cd()
hGenZMass = TH1D("hGenZMass", "Generator level;Dilepton mass (GeV);Events per 2GeV", 50, 50, 150)
hRecZMass = TH1D("hRecZMass", "Reconstruction level;Dilepton mass (GeV);Events per 2GeV", 50, 50, 150)

#hRecZMassVsPosEta = TH2D("hRecZMassVsPosEta", "Rec level;Positive muon pseudorapidity;Dilepton mass (GeV)", 10, -2.4, 2.4, 50, 50, 150)
#hRecZMassVsNegEta = TH2D("hRecZMassVsNegEta", "Rec level;Negitive muon pseudorapidity;Dilepton mass (GeV)", 10, -2.4, 2.4, 50, 50, 150)
#hRecZMassVsPosPhi = TH2D("hRecZMassVsPosPhi", "Rec level;Positive muon azimuthal angle;Dilepton mass (GeV)", 10, -pi, pi, 50, 50, 150)
#hRecZMassVsNegPhi = TH2D("hRecZMassVsNegPhi", "Rec level;Negitive muon azimuthal angle;Dilepton mass (GeV)", 10, -pi, pi, 50, 50, 150)

events = Events(files)
muonHandle = Handle('std::vector<pat::Muon>')
vertexHandle = Handle("std::vector<reco::Vertex>")
genHandle = Handle('std::vector<reco::GenParticle>')
for event in events:
    event.getByLabel('prunedGenParticles', genHandle)
    genParticles = genHandle.product()
    genPosMuons, genNegMuons = [], []
    for gen in genParticles:
        if abs(gen.pdgId()) != 13 or gen.pt() < 20 or abs(gen.eta()) > 2.4: continue

        if gen.charge() > 0: genPosMuons.append(gen)
        else: genNegMuons.append(gen)
    if len(genPosMuons) < 1 or len(genNegMuons) < 1: continue
    genPosMuons.sort(key=lambda x: x.pt(), reverse=True)
    genNegMuons.sort(key=lambda x: x.pt(), reverse=True)

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
        selMuons.append(mu)
    if len(selMuons) < 2: continue

    genZ = genPosMuons[0].p4()+genNegMuons[0].p4()
    recZ = selMuons[0].p4()+selMuons[1].p4()

    #posMuon, negMuon = selMuons[0], selMuons[1]
    #if posMuon.charge() < 0: posMuon, negMuon = negMuon, posMuon

    hGenZMass.Fill(genZ.mass())
    hRecZMass.Fill(recZ.mass())

    #hRecZMassVsPosEta.Fill(posMuon.eta(), recZ.mass())
    #hRecZMassVsNegEta.Fill(negMuon.eta(), recZ.mass())
    #hRecZMassVsPosPhi.Fill(posMuon.phi(), recZ.mass())
    #hRecZMassVsNegPhi.Fill(negMuon.phi(), recZ.mass())

f.cd()
hGenZMass.SetLineColor(kBlack)
hRecZMass.SetLineColor(kRed)
hGenZMass.Write()
hRecZMass.Write()

#hRecZMassVsPosEta.Write()
#hRecZMassVsNegEta.Write()
#hRecZMassVsPosPhi.Write()
#hRecZMassVsNegPhi.Write()

f.Write()
f.Close()


