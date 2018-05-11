#!/user/bin/env python

import sys
import yaml
import boto3

# break if no args given,
# otherwise set the instance name var
if len(sys.argv) == 1:
    print "Please provide an instance name, Eg:\n<script_name> my_new_instance"
    sys.exit(1)
else:
    instance_name = sys.argv[1]

# set the instance_id var to blank for later
instance_id = None

conf = yaml.load(open('conf/aws.config'))
config_aws_access_key_id = conf['aws']['access_key_id']
config_aws_secret_access_key = conf['aws']['secret_access_key']
config_region_name = conf['aws']['region_name']

# set the instance variables from the conf file
security_group = conf['instance']['sg']
ssh_key = conf['instance']['ssh_key']
flavour = conf['instance']['flavour']
ami = conf['instance']['ami']

ec2 = boto3.resource('ec2',
        aws_access_key_id=config_aws_access_key_id,
        aws_secret_access_key=config_aws_secret_access_key,
        region_name=config_region_name)

def create_instance():
    """
    Create an instance with some basic defaults
    and return the instance ID
    """
    instance = ec2.create_instances(
            ImageId=ami,
            MinCount=1,
            MaxCount=1,
            KeyName=ssh_key,
            SecurityGroupIds=[security_group],
            InstanceType=flavour)
    print "Instance:", instance[0].id, "created successfully."
    global instance_id
    instance_id = instance[0].id

def create_default_tags(instance_id, instance_name):
    """
    Set the default tags for deployment
    """

    # you could duplicate this line if you have extra default tags
    ec2.create_tags(Resources=[instance_id], Tags=[{'Key':'Name', 'Value':instance_name}])

def main():
    create_instance()
    create_default_tags(instance_id, instance_name)

if __name__ == "__main__":
    main()
