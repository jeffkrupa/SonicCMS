echo "ssh-ing into $(hostname) succeeded."
cd $1
timetoRun=$2
name=$3
timeNow=$(date +%s)


mkdir -p data/${name}
log="data/${name}/${RANDOM}.log"
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`

#sleep_seconds=$(echo "$timetoRun - $timeNow"|bc)
echo date >$log
#sleep $sleep_seconds
echo "Sleeping $sleep_seconds seconds" > $log 
echo date >$log
echo $pwd
cmsRun OnLine_HLT_GRun.py > $log & ##maxEvents=25 address=t3btch042.mit.edu port=8001

echo "Process on $(hostname) finished."
