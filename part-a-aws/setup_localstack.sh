#!/bin/bash
set -e
cd "$(dirname "$0")"
docker compose -f docker-compose-localstack.yml up -d
echo "LocalStack starting on http://localhost:4566"
sleep 3

