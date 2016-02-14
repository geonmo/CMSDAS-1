from ROOT import *
gROOT.ProcessLine(".x .rootlogon.C")

#f = TFile("/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root")
f = TFile("dymm.root")
events = f.Get("Events")
c1 = TCanvas("cpt", "cpt", 500, 500)
events.Draw("patMuons_slimmedMuons__PAT.obj.pt()>>hpt(100, 0, 200)")
c2 = TCanvas("cmult", "cmult", 500, 500)
events.Draw("patMuons_slimmedMuons__PAT.@obj.size()>>hmult(7, 0, 7)")
