echo "ssh-ing into $(hostname) succeeded."
cd $1
timetoRun=$(date -d "$2" +%s)
name=$3
timeNow=$(date +%s)
echo $timetoRun
echo $timeNow

mkdir -p data/${name}
log="data/${name}/${RANDOM}.log"
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`

sleep_seconds=$(($timetoRun - $timeNow))
echo "Sleeping $sleep_seconds seconds"  
sleep $sleep_seconds
cmsRun HcalTest_mc_cfg.py address=35.238.195.223 inputfile=TRK-Run3Summer19DR-00017_step1.root ##maxEvents=25 address=t3btch042.mit.edu port=8001
echo "HCALTEST!"
echo "Process on $(hostname) finished."

