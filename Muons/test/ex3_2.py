#!/usr/bin/env python

from math import *
from ROOT import *
gStyle.SetOptStat(0)

massNbin, massMin, massMax = 100, 70, 115
minPt, maxPt, minEta, maxEta = 20, 200, 0., 2.4

f = TFile("tnp.root")
ntuple = f.Get("ntuple")

cutStr = "probe_isTight"

gROOT.cd()
hPass = TH1D("hPass", "hPass", massNbin, massMin, massMax)
hFail = TH1D("hFail", "hFail", massNbin, massMin, massMax)

ntuple.Draw("z_m>>hPass", "probe_pt>=%f && probe_pt<%f && fabs(probe_eta)>=%f && fabs(probe_eta)<%f &&  (%s)" % (minPt, maxPt, minEta, maxEta, cutStr), "goff")
ntuple.Draw("z_m>>hFail", "probe_pt>=%f && probe_pt<%f && fabs(probe_eta)>=%f && fabs(probe_eta)<%f && !(%s)" % (minPt, maxPt, minEta, maxEta, cutStr), "goff")

nTotal = hPass.Integral()+hFail.Integral()

## Setup RooFit for efficiency calculation
ws = RooWorkspace("ws")

ws.factory('mass[%f, %f]' % (massMin, massMax))
mass = ws.var("mass")
mass.setBins(massNbin)
ws.factory('weight[0, 1e9]')
ws.factory('index[Pass,Fail]')

w_weight = ws.var('weight')
w_index = ws.cat('index')

## Build data for simultaneous fit
dataPass = RooDataSet("dataPass", "mass", RooArgSet(mass, w_weight), RooFit.WeightVar(w_weight))
dataFail = RooDataSet("dataFail", "mass", RooArgSet(mass, w_weight), RooFit.WeightVar(w_weight))
for b in range(massNbin):
    x = hPass.GetBinCenter(b+1)
    yPass = hPass.GetBinContent(b+1)
    yFail = hFail.GetBinContent(b+1)

    if yPass > 0:
        mass.setVal(x)
        w_weight.setVal(yPass)
        w_weight.setError(hPass.GetBinError(b+1))
        dataPass.add(RooArgSet(mass, w_weight), yPass)

    if yFail > 0:
        mass.setVal(x)
        w_weight.setVal(yFail)
        w_weight.setError(hFail.GetBinError(b+1))
        dataFail.add(RooArgSet(mass, w_weight), yFail)

mass.setVal(0)
w_weight.setVal(0)

dataSim = RooDataSet("dataSim", "mass", RooArgSet(mass, w_weight), RooFit.WeightVar(w_weight),
                     RooFit.Index(w_index), RooFit.Import("Pass", dataPass), RooFit.Import("Fail", dataFail))
getattr(ws, 'import')(dataSim)

ws.factory("Voigtian::signalPass(mass, mPass[91.2,89,93], width[2.9,0.5,5], sigmaPass[2,0.1,5])")
ws.factory("Voigtian::signalFail(mass, mFail[91.2,89,93], width, sigmaFail[2,0.1,5])")
#ws.factory("Exponential::backgroundPass(mass, p0Pass[0, -1e-1, 0])")
#ws.factory("Exponential::backgroundFail(mass, p0Fail[0, -1e-1, 0])")
ws.factory("Chebychev::backgroundPass(mass, {cPass1[0,-10,10], cPass2[0,-10,10]})")
ws.factory("Chebychev::backgroundFail(mass, {cFail1[0,-10,10]})")#, cFail2[0,-10,10]})")

ws.factory("efficiency[0.9,0,1]")
ws.factory("expr::nSigPass('efficiency*fSig*nTotal', efficiency, fSig[0.3,0,1], nTotal[%f,0,%f])" % (nTotal, nTotal+sqrt(nTotal)))
#ws.factory("expr::nSigPass('efficiency*fSig*nTotal', efficiency, fSig[0.9,0,1], nTotal[%f])" % (nTotal))
ws.factory("expr::nSigFail('(1-efficiency)*fSig*nTotal', efficiency, fSig, nTotal)")
ws.factory("expr::nBkgPass('bkgEff*(1-fSig)*nTotal', bkgEff[0.1,0,1], fSig, nTotal)")
ws.factory("expr::nBkgFail('(1-bkgEff)*(1-fSig)*nTotal', bkgEff, fSig, nTotal)")

ws.factory("SUM::pdfPass(nSigPass*signalPass, nBkgPass*backgroundPass)")
ws.factory("SUM::pdfFail(nSigFail*signalFail, nBkgFail*backgroundFail)")

ws.factory("SIMUL::simPdf(index, Pass=pdfPass, Fail=pdfFail)")

print "@@@ Starting Minimization @@@"
RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)
simPdf = ws.pdf("simPdf")
simNLL = simPdf.createNLL(dataSim, RooFit.Extended(True))
scanner = RooMinimizer(simNLL)
minuit = RooMinuit(simNLL)
minuit.setStrategy(1)
minuit.setProfile(True)
scanner.minimize("Minuit2","Scan")
minuit.migrad()
minuit.hesse()

print "@@@ Continue to profile NLL @@@"

w_effic = ws.var("efficiency")
#y, eyLo, eyHi = w_effic.getVal(), w_effic.getErrorLo(), w_effic.getErrorHi()

profileLL = RooProfileLL("simPdfNLL", "", simNLL, RooArgSet(w_effic))
profileLL.getVal()
profMinuit = profileLL.minimizer()

profMinuit.setProfile(True)
profMinuit.setStrategy(2)
profMinuit.setPrintLevel(1)
profMinuit.seek()
profMinuit.migrad()
profMinuit.minos(RooArgSet(w_effic))
result = profMinuit.save()

RooMsgService.instance().setGlobalKillBelow(RooFit.ERROR)

r_effic = result.floatParsFinal().find("efficiency")
y, eyLo, eyHi = r_effic.getVal(), r_effic.getErrorLo(), r_effic.getErrorHi()

framePass = mass.frame()
frameFail = mass.frame()

dataSim.plotOn(framePass, RooFit.Cut("index==index::Pass"), RooFit.DataError(RooAbsData.Poisson))
options = (RooFit.Slice(w_index, "Pass"), RooFit.ProjWData(RooArgSet(w_index), dataSim), RooFit.LineColor(kGreen))
simPdf.plotOn(framePass, RooFit.Components("backgroundPass"), RooFit.LineStyle(kDashed), *options)
simPdf.plotOn(framePass, *options)

dataSim.plotOn(frameFail, RooFit.Cut("index==index::Fail"), RooFit.DataError(RooAbsData.Poisson))
options = (RooFit.Slice(w_index, "Fail"), RooFit.ProjWData(RooArgSet(w_index), dataSim), RooFit.LineColor(kRed))
simPdf.plotOn(frameFail, RooFit.Components("backgroundFail"), RooFit.LineStyle(kDashed), *options)
simPdf.plotOn(frameFail, *options)

c = TCanvas("c", "c", 800, 800)
c.Divide(2,2)
c.cd(1)
framePass.Draw()
c.cd(2)
frameFail.Draw()
c.cd(3)
w_effic.setMin(0.8)
frameNLL = w_effic.frame()
profileLL.plotOn(frameNLL)
frameNLL.Draw()
c.cd(4)

print "@@@ Finished efficiency calculation @@@"
print "Efficiency = %f + %f -%f" % (y, eyHi, eyLo)

