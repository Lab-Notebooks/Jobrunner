#!/bin/bash


JobWorkDir="/home/akash/Desktop/Akash/Workbench/Jobrunner/tests/SimpleProject/JobObject"

cd /home/akash/Desktop/Akash/Workbench/Jobrunner/tests/SimpleProject

# Bash file for environment

echo "Hello from environment script"
export ENV_VAR_1="First environment variable"
Env_Var_2="Second environment variable"

cd /home/akash/Desktop/Akash/Workbench/Jobrunner/tests/SimpleProject/JobObject

# pre process script

echo "Hello from pre process script"
echo "ENV_VAR_1=$ENV_VAR_1"
echo "Env_Var_2=$Env_Var_2"

cd /home/akash/Desktop/Akash/Workbench/Jobrunner/tests/SimpleProject/JobObject

# submit script

echo "Hello from submit script"
echo "ENV_VAR_1=$ENV_VAR_1"
echo "Env_Var_2=$Env_Var_2"
