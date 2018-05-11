# AWS boto3 scripts

Messing around learning about boto3.

## Create an instance

Copy the sample conf file and then replace the access and secret key.
Populate your security group and SSH key name.

```
python create_instance.py name_of_my_new_instance
```

## Set tags of an instance from a config file

Edit your desired tags in conf/tags.config and then run via
```
python apply_tags_from_config.py <instance_id>
``` 
