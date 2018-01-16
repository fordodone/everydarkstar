#!/bin/bash
set -e

pip install --upgrade tweepy pyyaml -t lambda/

pushd lambda && zip -r ../package.zip * && popd

aws --profile everydarkstarbot s3 cp package.zip s3://everydarkstar.today/functions/

rm package.zip

LambdaPackageVersion=$(aws --profile everydarkstarbot s3api get-object-tagging --bucket everydarkstar.today --key functions/package.zip --query VersionId --output text)

cat cloudformation/parameters.json \
  | jq -r ". | map(if .ParameterKey == \"LambdaPackageVersion\" then . + { \"ParameterValue\":\"${LambdaPackageVersion}\"} else . end)" \
  > parameters.json.tmp \
  && mv parameters.json.tmp cloudformation/parameters.json
