#!/bin/bash

set -e

if [[ $# -eq 0 ]] ; then
    printf 'Please provide a state argument\nEg. <script_name> [running|stopped|pending|terminated]'
    exit 0
fi

STATE=$1

if [ $STATE = "running" ]; then
	aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId, Tags[?Key==`Name`].Value | [0], InstanceType, LaunchTime, State.Name, PublicIpAddress, KeyName]' --filters Name=instance-state-name,Values=$STATE --output table --region ap-southeast-2
else
	aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,Tags[?Key==`Name`].Value | [0], InstanceType, State.Name]' --filters Name=instance-state-name,Values=$STATE --output table --region ap-southeast-2
fi
