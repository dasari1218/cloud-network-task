#!/usr/bin/env python3
import os, boto3
from botocore.config import Config

LOCAL = os.getenv("LOCALSTACK", "0") == "1"
EP = "http://localhost:4566" if LOCAL else None
cfg = Config(retries={'max_attempts': 5})

def client(srv):
    return boto3.client(srv, region_name='us-east-1', endpoint_url=EP, config=cfg) if EP else boto3.client(srv, region_name='us-east-1', config=cfg)

ec2 = client('ec2')

def get_subnets(vpc_id):
    subs = ec2.describe_subnets(Filters=[{'Name':'vpc-id','Values':[vpc_id]}])['Subnets']
    sub_ids = [s['SubnetId'] for s in subs]
    print("Subnets in VPC", vpc_id, ":", sub_ids)
    return sub_ids

def create_ec2_instances(subnets):
    instances = []
    for idx, subnet in enumerate(subnets):
        r = ec2.run_instances(
            ImageId='ami-12345678',  # dummy AMI for LocalStack
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            SubnetId=subnet,
        )
        inst_id = r['Instances'][0]['InstanceId']
        print(f"Created EC2 instance {inst_id} in subnet {subnet}")
        instances.append(inst_id)
    return instances

def main():
    # Pick the VPC created in Part A (replace with your VPC ID)
    vpcs = ec2.describe_vpcs()['Vpcs']
    vpc_id = None
    for v in vpcs:
        if any(tag['Key']=='Name' and tag['Value']=='task2-vpc' for tag in v.get('Tags', [])):
            vpc_id = v['VpcId']
            break
    if not vpc_id:
        print("Could not find VPC 'task2-vpc'")
        return

    subnets = get_subnets(vpc_id)
    instances = create_ec2_instances(subnets)
    print("All EC2 instances created:", instances)

if __name__ == "__main__":
    main()

