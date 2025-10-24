#!/usr/bin/env python3
import os, boto3
from botocore.config import Config

# LocalStack configuration
LOCAL = os.getenv("LOCALSTACK","0") == "1"
EP = "http://localhost:4566" if LOCAL else None
cfg = Config(retries={'max_attempts': 5})

def client(srv):
    return boto3.client(srv, region_name='us-east-1', endpoint_url=EP, config=cfg) if EP else boto3.client(srv, region_name='us-east-1', config=cfg)

ec2 = client('ec2')

def safe_print(s):
    # Replace unsupported unicode symbols for Windows terminal
    print(s.encode('ascii', errors='replace').decode())

# VPCs
vpcs = ec2.describe_vpcs()['Vpcs']
safe_print("\nVPCs:")
for v in vpcs:
    name = next((t['Value'] for t in v.get('Tags',[]) if t['Key']=='Name'), 'N/A')
    safe_print(f"  {v['VpcId']} - {name} - {v['CidrBlock']} - {v['State']}")

# Subnets
safe_print("\nSubnets:")
subnets = ec2.describe_subnets()['Subnets']
for s in subnets:
    name = next((t['Value'] for t in s.get('Tags',[]) if t['Key']=='Name'), 'N/A')
    safe_print(f"  {s['SubnetId']} - {name} - VPC: {s['VpcId']} - CIDR: {s['CidrBlock']} - AZ: {s['AvailabilityZone']}")

# Route Tables
safe_print("\nRoute Tables:")
rts = ec2.describe_route_tables()['RouteTables']
for rt in rts:
    safe_print(f"  {rt['RouteTableId']} - VPC: {rt['VpcId']} - Routes: {[r['DestinationCidrBlock'] for r in rt['Routes']]}")

# EC2 Instances
safe_print("\nEC2 Instances:")
instances = ec2.describe_instances()['Reservations']
for r in instances:
    for i in r['Instances']:
        safe_print(f"  {i['InstanceId']} - Subnet: {i['SubnetId']} - State: {i['State']['Name']}")

safe_print("\nEnvironment verification complete!")

