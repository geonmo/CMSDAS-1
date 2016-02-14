#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
from math import *
from copy import deepcopy
gROOT.ProcessLine(".x .rootlogon.C")

#files = ["file:/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root",]
files = ["file:dymm.root",]

events = Events(files)
trgResHandle = Handle("edm::TriggerResults")
trgObjHandle = Handle("std::vector<pat::TriggerObjectStandAlone>")
muonHandle = Handle('std::vector<pat::Muon>')
for event in events:
    event.getByLabel("TriggerResults::HLT", trgResHandle)
    trgRes = trgResHandle.product()
    trgNames = event._event.triggerNames(trgRes)

    event.getByLabel("selectedPatTrigger", trgObjHandle)
    trgObjs = trgObjHandle.product()

    event.getByLabel('slimmedMuons', muonHandle)
    muons = muonHandle.product()

    interestedTrgObjs = []
    for trgObj in trgObjs:
        trgObj.unpackPathNames(trgNames)
        if trgObj.hasPathName("HLT_IsoMu20_v*") or trgObj.hasPathName("HLT_IsoTkMu20_v*"):
            interestedTrgObjs.append(trgObj)

    for iMuon, mu in enumerate(muons):
        drMin = 0.1
        matchedTrgObj = None
        for trgObj in interestedTrgObjs:
            dr = sqrt( (mu.eta()-trgObj.eta())**2 + (mu.phi()-trgObj.phi())**2 )
            if dr < drMin:
                drMin = dr
                matchedTrgObj = trgObj

        if matchedTrgObj != None:
            print  "pat muon (pt=%f eta=%f phi=%f) is matched to trg obj (pt=%f eta=%f phi=%f)" % (mu.pt(), mu.eta(), mu.phi(), matchedTrgObj.pt(), matchedTrgObj.eta(), matchedTrgObj.phi())
