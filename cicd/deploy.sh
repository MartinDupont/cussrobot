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

aws cloudformation deploy \
    --stack-name cussrobot-infrastructure \
    --template-file infrastructure/lambda-bucket.yaml \
    --capabilities CAPABILITY_IAM \
    --no-fail-on-empty-changeset
