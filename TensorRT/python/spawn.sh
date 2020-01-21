#!/bin/bash
# spawn.sh

# Spawns a lot of instances of cmsRun Hcal*.py on whatever machines you like
# Use the -c flag to clear the data directory beforehand.

# Determine whether the -c flag was used
getopts 'c' flag
clearSet=0

case ${flag} in
    c ) clearSet=1;;
esac

# Check to make sure the number of clients was given
if [ $# == $clearSet ]; then
    echo "Please provide the number of clients to spawn."
    exit
fi

# Clear the data directory if -c was used
if [ $clearSet == 1 ]; then
    echo "Clearing data directory"
    rm data/*.dat
fi

# Get the ssh password
echo "Please enter your ssh password."
read -s password

# Run the clients
minHostNum="$((2+$clearSet))"
numClients="$((1+$clearSet))"

for ((hostNum=$minHostNum; hostNum <= $#; hostNum++))
do  
    echo "Starting host ${!hostNum}"
    for ((i=0; i < ${!numClients}; i++))
    do
        echo $i
        sshpass -p ${password} ssh jtdinsmo@${!hostNum} "sh /home/jtdinsmo/quickHcalRun.sh" &
        disown
    done
done

echo "Done"



