#!/bin/bash

JobWorkDir="/home/akash/Desktop/Akash/Workbench/Jobrunner/tests/SimpleProject/JobObject"

cd /home/akash/Desktop/Akash/Workbench/Jobrunner/tests/SimpleProject

# Bash file for environment

echo "Hello from environment script"
export ENV_VAR_1="First environment variable"
Env_Var_2="Second environment variable"

cd /home/akash/Desktop/Akash/Workbench/Jobrunner/tests/SimpleProject/JobObject

# setup script

echo "Hello from setup script"
echo "ENV_VAR_1=$ENV_VAR_1"
echo "Env_Var_2=$Env_Var_2"
