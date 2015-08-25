#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
gROOT.ProcessLine(".x tdrstyle.C")

hPt1 = TH1F("hPt1", "Muon1;Muon p_{T} (GeV);Events / 20GeV", 100, 0, 200)
hPt2 = TH1F("hPt2", "Muon2;Muon p_{T} (GeV);Events / 20GeV", 100, 0, 200)
hM = TH1F("hM", "Dimuon;Dimuon mass (GeV);Events / 20GeV", 100, 0, 200)
hPt1.SetLineColor(kRed)
hPt2.SetLineColor(kBlue)

files = [
    "file:/cmsdas/data/ShortEX_Muon/RelValZMM_13_MINIAODSIM/0AF36725-FB1A-E511-BCB2-0025905A497A.root",
    #"/store/relval/CMSSW_7_4_6/RelValZMM_13/MINIAODSIM/PU50ns_MCRUN2_74_V8-v2/00000/0AF36725-FB1A-E511-BCB2-0025905A497A.root",
]

events = Events(files)
muonHandle = Handle('std::vector<pat::Muon>')
for iEvent, event in enumerate(events):
    print 'Analyzing', iEvent, 'th event'
    event.getByLabel('slimmedMuons', muonHandle)
    muons = muonHandle.product()
    if muons.size() < 2: continue
    muon1, muon2 = muons[0], muons[1]

    hPt1.Fill(muon1.pt())
    hPt2.Fill(muon2.pt())
    dimuonP4 = muon1.p4()+muon2.p4()
    hM.Fill(dimuonP4.mass())

cPt = TCanvas("cPt", "cPt", 500, 500)
hPt1.Draw()
hPt2.Draw("same")
cM = TCanvas("cM", "cM", 500, 500)
hM.Draw()
