#!/user/bin/env python
#
# This script can be used to plug into a monitoring platform
# which accepts Nagios style scripts.

import sys
import yaml
import boto3

# init the list
instance_list = []

# set the aws access credentials
conf = yaml.load(open('conf/aws.config'))
config_aws_access_key_id = conf['aws']['access_key_id']
config_aws_secret_access_key = conf['aws']['secret_access_key']
config_region_name = conf['aws']['region_name']

# init the aws ec2 client
ec2 = boto3.resource('ec2',
        aws_access_key_id=config_aws_access_key_id,
        aws_secret_access_key=config_aws_secret_access_key,
        region_name=config_region_name)

def instances_without_tag(tag_key):
    """
    Return instances which do not have
    the supplied tag key
    """

    instances = [i for i in ec2.instances.all()]
    
    # Print instance_id of instances that do not have a Tag of Key=tag
    for i in instances:
      if tag_key not in [t['Key'] for t in i.tags]:
          instance_list.append(i.instance_id)

    return instance_list

def monitor(tag_key):
    """
    Logic to test and raise an error
    if instances have no Name
    """

    # call the above function to generate the list
    instances = instances_without_tag(tag_key)

    # if no instance ids return then exit with success
    if len(instances) < 1:
        print "OK: All instances have %s tag." % tag_key
        sys.exit(0)
    
    elif len(instances) >= 1:
        print "ERROR: Some instances do not have %s tags. See below:\n" % tag_key, instances
        sys.exit(2)

    else:
        print "The script has malfunctioned."
        sys.exit(3)

def main():
    # break if no args given,
    # otherwise set the desired tag variable
    if len(sys.argv) == 1:
        print "Please provide a tag key, Eg:\n<script_name> Name"
        sys.exit(1)
    else:
        tag_key = sys.argv[1]
        monitor(tag_key)

if __name__ == "__main__":
    main()

