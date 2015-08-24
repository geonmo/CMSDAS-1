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

def detIso03(muon):
    return (muon.isolationR03().sumPt + muon.isolationR03().emEt + muon.isolationR03().hadEt )/muon.pt()

def detIso05(muon):
    return (muon.isolationR05().sumPt + muon.isolationR05().emEt + muon.isolationR05().hadEt )/muon.pt()

def pfIso(muon):
    return (muon.chargedHadronIso()+muon.neutralHadronIso()+muon.photonIso())/muon.pt()

def pfIsoDB(muon):
    return (muon.chargedHadronIso()+max(0, muon.neutralHadronIso()+muon.photonIso()-0.5*muon.puChargedHadronIso()))/muon.pt()

np = 20
nTotalSig, nTotalBkg = 0, 0

hDetIso03Sig = TH1F("hDetIso03Sig", "DetIso03", np, 0, 0.5)
hDetIso05Sig = TH1F("hDetIso05Sig", "DetIso05", np, 0, 0.5)
#hPFIsoSig = TH1F("hPFIsoSig", "PFIso", np, 0, 0.3)
#hPFIsoDBSig = TH1F("hPFIsoDBSig", "PFIsoDB", np, 0, 0.3)

hDetIso03Bkg = TH1F("hDetIso03Bkg", "DetIso03", np, 0, 0.5)
hDetIso05Bkg = TH1F("hDetIso05Bkg", "DetIso05", np, 0, 0.5)
#hPFIsoBkg = TH1F("hPFIsoBkg", "PFIso", np, 0, 0.3)
#hPFIsoDBBkg = TH1F("hPFIsoDBBkg", "PFIsoDB", np, 0, 0.3)

events = Events(files)
muonHandle = Handle('std::vector<pat::Muon>')
vertexHandle = Handle('std::vector<reco::Vertex>')
for iEvent, event in enumerate(events):
    print 'Analyzing', iEvent, 'th event\r',
    event.getByLabel('slimmedMuons', muonHandle)
    event.getByLabel('offlineSlimmedPrimaryVertices', vertexHandle)
    muons = muonHandle.product()
    vertex = vertexHandle.product().at(0)
    if muons.size() < 2: continue
    muon1, muon2 = muons[0], muons[1]
    if muon1.pt() < 20 or muon2.pt() < 20: continue
    dimuonP4 = muon1.p4()+muon2.p4()
    if not muon1.isTightMuon(vertex): continue
    if not muon2.isLooseMuon(): continue

    muonDetIso03 = detIso03(muon2)
    muonDetIso05 = detIso05(muon2)
    #pfIso2 = pfIso(muon2)
    #pfIsoDB2 = pfIsoDB(muon2)

    if muon1.charge() + muon2.charge() == 0:
        nTotalSig += 1
        hDetIso03Sig.Fill(muonDetIso03)
        hDetIso05Sig.Fill(muonDetIso05)
        #hPFIsoSig.Fill(pfIso2)
        #hPFIsoDBSig.Fill(pfIsoDB2)
    else:
        nTotalBkg += 1
        hDetIso03Bkg.Fill(muonDetIso03)
        hDetIso05Bkg.Fill(muonDetIso05)
        #hPFIsoBkg.Fill(pfIso2)
        #hPFIsoDBBkg.Fill(pfIsoDB2)

grpDetIso03 = TGraph()
grpDetIso05 = TGraph()
#grpPFIso = TGraph()
#grpPFIsoDB = TGraph()
for i in xrange(np):
    x = hDetIso03Sig.GetBinLowEdge(i)+hDetIso03Sig.GetBinWidth(i)
    rSig, rBkg = hDetIso03Sig.Integral(0, i), hDetIso03Bkg.Integral(0, i)
    grpDetIso03.SetPoint(i, 100.*rBkg/nTotalBkg, 100.*rSig/nTotalSig)
    print "detIso03: ", x, " signal=", 100.*rSig/nTotalSig, "%, bkg=", 100.*rBkg/nTotalBkg, "%"
    rSig, rBkg = hDetIso05Sig.Integral(0, i), hDetIso05Bkg.Integral(0, i)
    grpDetIso05.SetPoint(i, 100.*rBkg/nTotalBkg, 100.*rSig/nTotalSig)
    print "detIso05: ", x, " signal=", 100.*rSig/nTotalSig, "%, bkg=", 100.*rBkg/nTotalBkg, "%"
    #rSig, rBkg = hPFIsoSig.Integral(0, i), hPFIsoBkg.Integral(0, i)
    #grpPFIso.SetPoint(i, 100.*rBkg/nTotalBkg, 100.*rSig/nTotalSig)
    #print "pfIso: ", x, " signal=", 100.*rSig/nTotalSig, "%, bkg=", 100.*rBkg/nTotalBkg, "%"
    #rSig, rBkg = hPFIsoDBSig.Integral(0, i), hPFIsoDBBkg.Integral(0, i)
    #grpPFIsoDB.SetPoint(i, 100.*rBkg/nTotalBkg, 100.*rSig/nTotalSig)
    #print "pfIso dbeta: ", x, " signal=", 100.*rSig/nTotalSig, "%, bkg=", 100.*rBkg/nTotalBkg, "%"

grpDetIso03.SetLineColor(kRed)
grpDetIso03.SetMarkerColor(kRed)
#grpPFIso.SetLineColor(kBlue)
#grpPFIsoDB.SetLineColor(kGreen+1)
grpDetIso05.SetLineColor(kBlue)
grpDetIso05.SetMarkerColor(kBlue)
#grpPFIso.SetMarkerColor(kBlue)
#grpPFIsoDB.SetMarkerColor(kGreen+1)
c = TCanvas("cROC", "cROC", 500, 500)
hFrame = TH2F("hFrame", "hFrame;Background efficiency (%%);Signal efficiency (%%)", 100, 0, 100, 100, 0, 100)
hFrame.Draw()
grpDetIso03.Draw("LP")
grpDetIso05.Draw("LP")
#grpPFIso.Draw("LP")
#grpPFIsoDB.Draw("LP")
