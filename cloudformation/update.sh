#!/bin/bash

#aws --profile everydarkstarbot --region us-west-1 cloudformation create-stack --stack-name EveryDarkStarBot --capabilities CAPABILITY_NAMED_IAM --template-body file://template.yml --parameters file://parameters.json
aws --profile everydarkstarbot --region us-west-1 cloudformation update-stack --stack-name EveryDarkStarBot --capabilities CAPABILITY_NAMED_IAM --template-body file://template.yml --parameters file://parameters.json
aws --profile everydarkstarbot --region us-west-1 cloudformation wait stack-update-complete --stack-name EveryDarkStarBot
