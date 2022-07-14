import boto3
import json
from json_custom import MyJsonEncoder
import datetime


parameters = [
    {
        'ParameterName': 'max_allowed_packet',
        'ParameterValue': '536870912',
        'ApplyMethod': 'immediate'
    },
]

regions = [
    'ap-southeast-2',
    'ca-central-1',
    'eu-west-2'
]

session = boto3.Session(profile_name="custom")

clients = {}
for region in regions:
    clients[region] = session.client('rds', region)

for region, client in clients.items():

    resp = client.modify_db_cluster_parameter_group(
        DBClusterParameterGroupName='custom-cluster-parameters' if region == 'ap-southeast-2' else 'custom-parameters-cluster',
        Parameters=parameters
    )
    print(json.dumps(resp, cls=MyJsonEncoder))
