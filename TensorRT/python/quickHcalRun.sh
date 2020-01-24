echo "ssh-ing into $(hostname) succeeded."
cd $1
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
cmsRun HcalTest_mc_cfg.py maxEvents=25 address=t3btch042.mit.edu port=8001
echo "Process on $(hostname) finished."
