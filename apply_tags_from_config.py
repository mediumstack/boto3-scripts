#!/usr/bin/env python

import sys
import yaml
import boto3

# init the list
list_of_tags = []

# break if there are no arguments supplied
# otherwise set the instance id variable
if len(sys.argv) == 1:
    print "Please provide an instance id, Eg:\n<script_name> i-********"
    sys.exit(1)
else:
    instance_id = sys.argv[1]

conf = yaml.load(open('conf/aws.config'))
config_aws_access_key_id = conf['aws']['access_key_id']
config_aws_secret_access_key = conf['aws']['secret_access_key']
config_region_name = conf['aws']['region_name']

ec2 = boto3.resource('ec2',
        aws_access_key_id=config_aws_access_key_id,
        aws_secret_access_key=config_aws_secret_access_key,
        region_name=config_region_name)

client = boto3.client('ec2',
        aws_access_key_id=config_aws_access_key_id,
        aws_secret_access_key=config_aws_secret_access_key,
        region_name=config_region_name)

def gen_tag_list():
    """
    Grab tags from conf file
    and turn into a list.
    """

    # declare the path to the config file
    input_file = 'conf/tags.config'
    
    # open the tags config file
    tags_config = yaml.load(open(input_file))

    # move underneath the tags header
    tags = tags_config['tags']

    # iterate over the tags
    for key,value in tags.iteritems():
    
        # prepare the variable for appending
        temp = [key,value]

        # append the tags to the list
        list_of_tags.append(temp)
    
    return list_of_tags

def set_tags(instance_id):
    """
    Set instance tags based on
    the tags created by the
    gen_tag_list() function.
    """

    # iterate over the tags from the list
    for tag in list_of_tags:

        # split the item into key and value
        key = tag[0]
        value = tag[1]
    
        # set the tags
        ec2.create_tags(Resources=[instance_id], Tags=[{'Key':key, 'Value':value}])

def main():
    gen_tag_list()
    set_tags(instance_id)

if __name__ == "__main__":
    main()
