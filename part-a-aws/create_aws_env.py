#!/usr/bin/env python3
import os, boto3
from botocore.config import Config

LOCAL = os.getenv("LOCALSTACK","0") == "1"
EP = "http://localhost:4566" if LOCAL else None
cfg = Config(retries={'max_attempts': 5})

def client(srv):
    return boto3.client(srv, region_name='us-east-1', endpoint_url=EP, config=cfg) if EP else boto3.client(srv, region_name='us-east-1', config=cfg)

ec2 = client('ec2')
# elbv2 = client('elbv2')  # Disabled for LocalStack free tier

def create_vpc():
    r = ec2.create_vpc(CidrBlock='10.10.0.0/16')
    vpc = r['Vpc']['VpcId']
    ec2.create_tags(Resources=[vpc], Tags=[{'Key':'Name','Value':'task2-vpc'}])
    ec2.modify_vpc_attribute(VpcId=vpc, EnableDnsSupport={'Value': True})
    ec2.modify_vpc_attribute(VpcId=vpc, EnableDnsHostnames={'Value': True})
    print("VPC:", vpc); return vpc

def create_subnets(vpc):
    a = ec2.create_subnet(VpcId=vpc, CidrBlock='10.10.1.0/24', AvailabilityZone='us-east-1a')['Subnet']['SubnetId']
    b = ec2.create_subnet(VpcId=vpc, CidrBlock='10.10.2.0/24', AvailabilityZone='us-east-1b')['Subnet']['SubnetId']
    ec2.create_tags(Resources=[a], Tags=[{'Key':'Name','Value':'task2-subnet-a'}])
    ec2.create_tags(Resources=[b], Tags=[{'Key':'Name','Value':'task2-subnet-b'}])
    print("Subnets:", a, b); return [a,b]

def create_route_table(vpc, subnets):
    rt = ec2.create_route_table(VpcId=vpc)['RouteTable']['RouteTableId']
    for s in subnets:
        ec2.associate_route_table(RouteTableId=rt, SubnetId=s)
    print("RouteTable:", rt); return rt

# -------------------------
# ELBv2-related functions are commented out for LocalStack free tier
# def create_tg(vpc): pass
# def create_alb(subnets): pass
# def create_listener(lb, tg): pass
# def register_targets(tg, ips): pass
# -------------------------

def main():
    vpc = create_vpc()
    subs = create_subnets(vpc)
    create_route_table(vpc, subs)
    # ELBv2 calls removed for LocalStack free tier
    print("DONE. VPC:", vpc)

if __name__ == "__main__":
    main()
