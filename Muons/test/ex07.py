#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
gROOT.ProcessLine(".x tdrstyle.C")

hMSig = TH1F("hMSig", "Dimuon in Sig;Dimuon mass (GeV);Events / 20GeV", 100, 0, 200)
hMBkg = TH1F("hMBkg", "Dimuon in Bkg;Dimuon mass (GeV);Events / 20GeV", 100, 0, 200)
hMSig.SetLineColor(kRed)
hMBkg.SetLineColor(kBlue)

files = [
    "file:/cmsdas/data/ShortEX_Muon/DoubleMuon_Run2015C_MINIAOD/CC542F3F-AC2D-E511-B093-02163E014181.root",
]

nTotalSig, nTotalBkg = 0, 0
nLooseSig, nLooseBkg = 0, 0
nMediumSig, nMediumBkg = 0, 0
nTightSig, nTightBkg = 0, 0
nSoftSig, nSoftBkg = 0, 0
events = Events(files)
muonHandle = Handle('std::vector<pat::Muon>')
vertexHandle = Handle('std::vector<reco::Vertex>')
for iEvent, event in enumerate(events):
    print 'Analyzing', iEvent, 'th event'
    event.getByLabel('slimmedMuons', muonHandle)
    event.getByLabel('offlineSlimmedPrimaryVertices', vertexHandle)
    muons = muonHandle.product()
    vertex = vertexHandle.product().at(0)
    if muons.size() < 2: continue
    muon1, muon2 = muons[0], muons[1]
    if muon1.pt() < 20 or muon2.pt() < 20: continue
    dimuonP4 = muon1.p4()+muon2.p4()
    if not muon1.isTightMuon(vertex): continue

    if muon1.charge() + muon2.charge() == 0:
        nTotalSig += 1
        if muon2.isLooseMuon(): nLooseSig += 1
        if muon2.isMediumMuon(): nMediumSig += 1
        if muon2.isTightMuon(vertex): nTightSig += 1
        if muon2.isSoftMuon(vertex): nSoftSig += 1
    else:
        nTotalBkg += 1
        if muon2.isLooseMuon(): nLooseBkg += 1
        if muon2.isMediumMuon(): nMediumBkg += 1
        if muon2.isTightMuon(vertex): nTightBkg += 1
        if muon2.isSoftMuon(vertex): nSoftBkg += 1

print "Loose : signal=%f%%, bkg=%f%%" % (100.*nLooseSig/nTotalSig, 100.*nLooseBkg/nTotalBkg)
print "Medium: signal=%f%%, bkg=%f%%" % (100.*nMediumSig/nTotalSig, 100.*nMediumBkg/nTotalBkg)
print "Tight : signal=%f%%, bkg=%f%%" % (100.*nTightSig/nTotalSig, 100.*nTightBkg/nTotalBkg)
print "Soft  : signal=%f%%, bkg=%f%%" % (100.*nSoftSig/nTotalSig, 100.*nSoftBkg/nTotalBkg)
