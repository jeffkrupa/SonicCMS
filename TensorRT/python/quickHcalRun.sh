echo "ssh-ing into $(hostname) succeeded."
cd $1
timetoRun=$2
nCPUS=$3
nperCPU=$4
timeNow=$(date %s)


mkdir -p data/${nCPUS}_${nperCPU}
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv

log="data/${nCPUS}_${nperCPU}_${RANDOM}.log"
sleep_seconds=$(echo "$timtoRun - $timeNow"|bc)
date >$log
sleep $sleep_seconds
echo "Sleeping $sleep_seconds seconds" > $log 
date >$log
cmsRun OnLine_HLT_GRun.py > $log ##maxEvents=25 address=t3btch042.mit.edu port=8001
echo "Process on $(hostname) finished."
