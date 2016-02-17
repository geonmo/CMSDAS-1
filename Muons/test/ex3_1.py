#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
from math import *
gROOT.ProcessLine(".x .rootlogon.C")

#files = ["file:/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root",]
files = ["file:dymm.root",]

f = TFile("tnp.root", "recreate")
ntuple = TNtupleD("ntuple", "ntuple", "z_m:tag_pt:tag_eta:probe_pt:probe_eta:probe_isTight:probe_isLoose:probe_relIso")

events = Events(files)
trgResHandle = Handle("edm::TriggerResults")
trgObjHandle = Handle("std::vector<pat::TriggerObjectStandAlone>")
muonHandle = Handle('std::vector<pat::Muon>')
vertexHandle = Handle("std::vector<reco::Vertex>")
for event in events:
    event.getByLabel("TriggerResults::HLT", trgResHandle)
    trgRes = trgResHandle.product()
    trgNames = event._event.triggerNames(trgRes)

    event.getByLabel("selectedPatTrigger", trgObjHandle)
    trgObjs = trgObjHandle.product()

    event.getByLabel("offlineSlimmedPrimaryVertices", vertexHandle)
    vertices = vertexHandle.product()
    if vertices.size() == 0: continue
    vertex = vertices.at(0)

    event.getByLabel('slimmedMuons', muonHandle)
    muons = muonHandle.product()
    if muons.size() < 2: continue

    interestedTrgObjs = []
    for trgObj in trgObjs:
        trgObj.unpackPathNames(trgNames)
        if trgObj.hasPathName("HLT_IsoMu20_v*") or trgObj.hasPathName("HLT_IsoTkMu20_v*"):
            interestedTrgObjs.append(trgObj)

    ## Select tag muon
    tag = None
    for iMu, mu in enumerate(muons):
        ## Kinematic cuts
        if mu.pt() < 20 or abs(mu.eta()) > 2.5: continue

        ## Basic id cuts
        if not mu.isPFMuon(): continue
        if not mu.isTightMuon(vertex): continue

        ## Isolation cuts
        chIso = mu.chargedHadronIso()
        nhIso = mu.neutralHadronIso()
        phIso = mu.photonIso()
        puIso = mu.puChargedHadronIso()

        relIso = (chIso+nhIso+phIso+0.5*max(0., -puIso))/mu.pt()
        if relIso > 0.15: continue

        isTrigMatched = False
        for trgObj in interestedTrgObjs:
            dr = sqrt( (mu.eta()-trgObj.eta())**2 + (mu.phi()-trgObj.phi())**2 )
            if dr < 0.1:
                isTrigMatched = True
                break
        if not isTrigMatched: continue

        tag = (iMu, mu)
        break ## No need to continue to next muon if tag is already found

    if tag == None: continue ## Skip event if no tag found

    ## Select probe muon
    probe = None
    for iMu, mu in enumerate(muons):
        if iMu == tag[0]: continue ## Overlap checking

        ## Kinematic cuts
        if mu.pt() < 20 or abs(mu.eta()) > 2.5: continue

        probe = (iMu, mu)
        break ## No need to continue to next muon if probe is already found

    if probe == None: continue ## Skip event if no probe found

    tag, probe = tag[1], probe[1]
    z = tag.p4()+probe.p4()

    chIso = probe.chargedHadronIso()
    nhIso = probe.neutralHadronIso()
    phIso = probe.photonIso()
    puIso = probe.puChargedHadronIso()

    relIso = (chIso+ max(0, nhIso+phIso-0.5*puIso))/probe.pt()

    ntuple.Fill(z.mass(), tag.pt(), tag.eta(),
                probe.pt(), probe.eta(),
                probe.isTightMuon(vertex), probe.isLooseMuon(), relIso)

f.cd()
ntuple.Write()
f.Close()

