#!/usr/bin/env bash
mkdir -p build

aws cloudformation deploy \
    --stack-name lambda-artifacts \
    --template-file infrastructure/lambda-bucket.yaml \
    --capabilities CAPABILITY_IAM \
    --no-fail-on-empty-changeset

LAMBDA_ARTIFACTS_BUCKET=$(aws cloudformation describe-stacks --output json --stack-name lambda-artifacts | jq -r '.Stacks | .[0].Outputs[] | select(.OutputKey == "LambdaArtifactsBucketName") | .OutputValue')

aws cloudformation package \
    --template-file infrastructure/cf-lambdas.yaml \
    --s3-bucket "$LAMBDA_ARTIFACTS_BUCKET" \
    --output-template-file build/packaged-stack.yaml

echo "successfully created package."
aws cloudformation delete-stack --role-arn arn:aws:iam::229185685484:role/cussrobot-pipeline-CloudFormationRole-AQRAK5PJO6W3 --stack-name cussrobot-infrastructure

aws cloudformation deploy \
    --stack-name cussrobot-infrastructure \
    --template-file build/packaged-stack.yaml \
    --capabilities CAPABILITY_IAM \
    --no-fail-on-empty-changeset
