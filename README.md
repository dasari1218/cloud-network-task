# Cloud & Network Automation Task

## Candidate: Dasari Mohan Kumar

### Overview
This repository contains scripts and documentation for **Task 2 – Practical & Scripted Cloud Networking**.  
The task demonstrates automation of cloud and network environment setup, verification, and management using **Python/Boto3**, **AWS CLI**, and **local emulators**.

Skills covered:
- IP/Subnet Logic
- L2/L3 Routing
- Load Balancer & GSLB
- WAF & Multi-tenancy
- VRF, PG, NSX-T concepts (simulated)
- API/CLI Automation

---

## Part A – AWS Cloud (CLI/API)

**Approach:** LocalStack (AWS Emulator)

### Resources Created
- VPC: `task2-vpc`
- Subnets: `task2-subnet-a`, `task2-subnet-b`
- Route Table(s)
- Target Group: `task2-tg`
- Application Load Balancer: `task2-alb`
- EC2 instances (dummy/test targets)

### Scripts
- `create_aws_env.py` – Automates creation of VPC, subnets, route tables, TG, ALB, and registers targets.
- `verify_env.py` – Lists and verifies all resources created via API calls.

### How to Run
```bash
# Start LocalStack
docker-compose -f part-a-aws/docker-compose-localstack.yml up -d

# Set localstack mode
export LOCALSTACK=1

# Create AWS environment
python part-a-aws/create_aws_env.py

# Verify environment
python part-a-aws/verify_env.py
