#!/bin/bash

export REACT_APP_AZURE_APP_ID=$(aws ssm get-parameter --name /dev/$PROJECT_NAME/AZURE_APP_ID --query 'Parameter.Value' --output text)
export REACT_APP_AZURE_AUTHORITY=$(aws ssm get-parameter --name /dev/$PROJECT_NAME/AZURE_AUTHORITY --query 'Parameter.Value' --output text)

npm start
