#!/bin/bash

WEB_BUCKET=$(aws cloudformation describe-stack-resource --stack-name $DISTRIBUTION_STACK_NAME --logical-resource-id ContentBucket --output text --query StackResourceDetail.PhysicalResourceId)
aws s3 sync ./build s3://$WEB_BUCKET/ --exclude index.html max-age=100000
aws s3 cp ./build/index.html s3://$WEB_BUCKET/ --cache-control max-age=20
