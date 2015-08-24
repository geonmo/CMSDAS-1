#!/usr/bin/env python

from DataFormats.FWLite import Events, Handle,Lumis
from ROOT import *
gROOT.ProcessLine(".x tdrstyle.C")

hPtOS1 = TH1F("hPtOS1", "Muon1 in OS;Muon p_{T} (GeV);Events / 20GeV", 100, 0, 200)
hPtOS2 = TH1F("hPtOS2", "Muon2 in OS;Muon p_{T} (GeV);Events / 20GeV", 100, 0, 200)
hPtSS1 = TH1F("hPtSS1", "Muon1 in SS;Muon p_{T} (GeV);Events / 20GeV", 100, 0, 200)
hPtSS2 = TH1F("hPtSS2", "Muon2 in SS;Muon p_{T} (GeV);Events / 20GeV", 100, 0, 200)
hMOS = TH1F("hMOS", "Dimuon in OS;Dimuon mass (GeV);Events / 20GeV", 100, 0, 200)
hMSS = TH1F("hMSS", "Dimuon in SS;Dimuon mass (GeV);Events / 20GeV", 100, 0, 200)
hPtOS1.SetLineColor(kRed)
hPtOS2.SetLineColor(kBlue)
hPtSS1.SetLineColor(kMagenta)
hPtSS2.SetLineColor(kGreen+1)
hMOS.SetLineColor(kRed)
hMSS.SetLineColor(kBlue)

files = [
    "file:/cmsdas/data/ShortEX_Muon/DoubleMuon_Run2015C_MINIAOD/CC542F3F-AC2D-E511-B093-02163E014181.root",
]

events = Events(files)
muonHandle = Handle('std::vector<pat::Muon>')
for iEvent, event in enumerate(events):
    print 'Analyzing', iEvent, 'th event'
    event.getByLabel('slimmedMuons', muonHandle)
    muons = muonHandle.product()
    if muons.size() < 2: continue
    muon1, muon2 = muons[0], muons[1]
    dimuonP4 = muon1.p4()+muon2.p4()

    if muon1.charge() + muon2.charge() == 0:
        hPtOS1.Fill(muon1.pt())
        hPtOS2.Fill(muon2.pt())
        hMOS.Fill(dimuonP4.mass())
    else:
        hPtSS1.Fill(muon1.pt())
        hPtSS2.Fill(muon2.pt())
        hMSS.Fill(dimuonP4.mass())

cPt = TCanvas("cPt", "cPt", 500, 500)
hPtOS1.Draw()
hPtOS2.Draw("same")
hPtSS1.Draw("same")
hPtSS2.Draw("same")
cM = TCanvas("cM", "cM", 500, 500)
hMOS.Draw()
hMSS.Draw("same")
