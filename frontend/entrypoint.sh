#!/bin/bash

export REACT_APP_AZURE_APP_ID=$(aws ssm get-parameter --name $PARAMETER_PATH/AZURE_APP_ID --query 'Parameter.Value' --output text)
export REACT_APP_AZURE_AUTHORITY=$(aws ssm get-parameter --name $PARAMETER_PATH/AZURE_AUTHORITY --query 'Parameter.Value' --output text)

npm start
