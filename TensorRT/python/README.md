
<<<<<<< HEAD
`cmsRun reco_pat_facile.py` does RAW->MINIAOD with hbheprereco done via FACILE as-a-service.
`cmsRun reco_pat_mahi.py` does RAW->MINIAOD with nominal hbheprereco algo (MAHI).

Jet analysis follows this (using Pat::Jet): https://twiki.cern.ch/twiki/bin/view/CMS/JUMPSHOTJetScaleResolution#Setup
=======
`cmsRun reco_pat_facile.py` does RAW->MINIAOD with hbheprereco done via FACILE as-a-service
`cmsRun reco_pat_mahi.py` does RAW->MINIAOD with nominal hbheprereco algo (MAHI).
Jet analysis follows this running on Pat::Jet https://twiki.cern.ch/twiki/bin/view/CMS/JUMPSHOTJetScaleResolution#Setup
>>>>>>> aabff61... user instructions

`cmsRun OnLine_HLT_GRun.py` does HLT step with hbheprereco done via FACILE as-a-service
`cmsRun OnLine_HLT_GRun_nominal.py` does HLT step with nominal hbheprereco algo (MAHI).
`python correlation.py` runs on top of the files produced by the HLT step to show the correlation.



