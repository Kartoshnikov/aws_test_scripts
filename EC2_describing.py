import boto3
import json
from json_custom import MyJsonEncoder
import datetime

session = boto3.Session(profile_name="custom")

client_def = boto3.client('ec2')
regions = [r['RegionName'] for r in client_def.describe_regions()['Regions']]
for i in dir(client_def):
    if not i.startswith('__'):
        print(i)


for region in regions:
    client = session.client('ec2', region)
    resp = client.describe_instances()
    if not len(resp['Reservations']) == 0: print(json.dumps(resp, cls=MyJsonEncoder))
    for instance in client.describe_instances()['Reservations']:
        print("Region: {:15}, InstanceID: {}, AZ: {}".format(
            region,
            instance['Instances'][0]['InstanceId'],
            instance['Instances'][0]['Placement']['AvailabilityZone']
        ))
