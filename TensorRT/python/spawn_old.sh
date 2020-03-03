# Determine whether the -c flag was used
getopts 'c' flag
clearSet=0

case ${flag} in
    c ) clearSet=1;;
esac

# Check to make sure the number of clients was given
if [ "$#" -le "$(($clearSet+1))" ]; then
    echo "Please provide the number of clients to spawn and your username, in that order."
    exit
fi

numClients="$((1+$clearSet))"
userName="$((2+$clearSet))"
minHostNum="$((3+$clearSet))"
hostFile="${!minHostNum}"
name=$5
timetorun="$6"
pathToPython="~/CMSSW_10_6_6/src/SonicCMS/TensorRT/python/"



# update latest changes to git
git gc --prune=now
git remote prune origin
git commit -am "update"
git push
cat $hostFile
# Run the clients

while read hostNum; do
    echo "Updating and compiling host ${hostNum}"
    gcloud compute ssh jeffkrupa@${hostNum} --zone "us-central1-a" --command="cd $pathToPython/../../; git pull -f; source /cvmfs/cms.cern.ch/cmsset_default.sh; cmsenv; scram b;" --ssh_args="-n"
done <$hostFile

while read hostNum; do
    mkdir -p data/$name/$hostNum
    rm -r data/$name/$hostNum/*
    echo "Starting host ${hostNum}"


    for ((i=0; i < ${!numClients}; i++))
    do
        pkill -USR1 cmsRun
        echo "Starting client number $i at ${hostNum}"
        log="data/$name/$hostNum/$i.log"
        gcloud compute ssh jeffkrupa@${hostNum} --zone us-central1-a\
	--command="cd $pathToPython;\
	 rm DQM.root;\
	 sh $pathToPython/quickHcalRun.sh $pathToPython $timetorun $name" &> $log &

    done
    disown

done <$hostFile


echo "Done"
