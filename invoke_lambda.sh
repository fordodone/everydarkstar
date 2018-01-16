#!/bin/bash

aws --profile everydarkstarbot --region us-west-1 lambda invoke --function-name EveryDarkStarBot output.txt \
  && cat output.txt \
  && rm output.txt

