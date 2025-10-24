import boto3, os
from botocore.config import Config

EP = "http://localhost:4566" if os.getenv("LOCALSTACK","0")=="1" else None
cfg = Config(retries={'max_attempts': 5})
ec2 = boto3.client('ec2', region_name='us-east-1', endpoint_url=EP, config=cfg) if EP else boto3.client('ec2', region_name='us-east-1', config=cfg)

print("VPCs:")
print(ec2.describe_vpcs())

print("\nSubnets:")
print(ec2.describe_subnets())

print("\nRoute Tables:")
print(ec2.describe_route_tables())

