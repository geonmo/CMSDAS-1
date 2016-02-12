import FWCore.ParameterSet.Config as cms

catEventContentsTTLL = cms.untracked.vstring(
    "drop *",

    "keep *_TriggerResults_*_*",
    "keep *_slimmedGenJets_*_*",
    "keep *_prunedGenParticles_*_*",

    "keep *_pileupWeight_*_*",
    "keep *_genWeight_*Weight_*",
    "keep *_genWeight_pdfWeights_*",
    "keep *_genWeight_scaleWeights_*",

    "keep *_catVertex_nGoodPV_*",
    "keep *_partonTop_*_*",

    "keep *_eventsTTLL_*_CATeX",
    "keep *_filter*_*_CATeX",
)

