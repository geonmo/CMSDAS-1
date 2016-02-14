{
  TFile* f = TFile::Open("/wk3/cmsdas/store/user/cmsdas/2016/SHORT_EXERCISES/Muons/dymm.root");
  TTree* events = (TTree*)f->Get("Events");
  TCanvas* c = new TCanvas("cpt", "cpt", 500, 500);
  events->Draw("patMuons_slimmedMuons__PAT.obj.pt()>>hpt(100, 0, 200)");
  TCanvas* c2 = new TCanvas("cmult", "cmult", 500, 500);
  events->Draw("patMuons_slimmedMuons__PAT.@obj.size()>>hmult(7, 0, 7)")
}
