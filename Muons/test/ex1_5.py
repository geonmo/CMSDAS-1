#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
gROOT.ProcessLine(".x .rootlogon.C")

#files = ["file:/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root",]
files = ["file:dymm.root",]

events = Events(files)
muonHandle = Handle('std::vector<pat::Muon>')
vertexHandle = Handle("std::vector<reco::Vertex>")
for event in events:
    event.getByLabel("offlineSlimmedPrimaryVertices", vertexHandle)
    vertex = vertexHandle.product()
    if vertex.size() == 0: continue

    event.getByLabel('slimmedMuons', muonHandle)
    muons = muonHandle.product()

    for iMuon, mu in enumerate(muons):
        print "muon", iMuon, "isTightMuon=", mu.isTightMuon(vertex.at(0))


