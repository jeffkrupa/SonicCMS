echo "Hello world"
cd $1
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
cmsRun HcalTest_mc_cfg.py maxEvents=1 address=t3btch042.mit.edu port=8001 
