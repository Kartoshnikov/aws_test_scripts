import boto3
import json
from json_custom import MyJsonEncoder
import datetime


client_def = boto3.client('ec2')
for i in dir(client_def):
    if not i.startswith('__'):
        print(i)

regions = [r['RegionName'] for r in client_def.describe_regions()['Regions']]
session = boto3.Session(profile_name="cnn3p")
for region in regions:
    client = session.client('rds', region)
    resp_inct = client.describe_db_instances()
    resp_clsr = client.describe_db_clusters()
    if not (len(resp_inct['DBInstances']) == 0 and len(resp_clsr['DBClusters']) == 0):
        print(region)
        print(json.dumps(resp_clsr, cls=MyJsonEncoder), json.dumps(resp_inct, cls=MyJsonEncoder), sep='\n')
        for cluster in resp_clsr['DBClusters']:
            print("DBClusterIdentifier: {:>25}; DBClusterParameterGroup: {:>30}; Engine: {}({}); DBClusterMembers: {}".format(
                cluster['DBClusterIdentifier'],
                cluster['DBClusterParameterGroup'],
                cluster['Engine'],
                cluster['EngineVersion'],
                ",".join(cl['DBInstanceIdentifier'] for cl in cluster['DBClusterMembers']),
            ))
        else:
            print()
