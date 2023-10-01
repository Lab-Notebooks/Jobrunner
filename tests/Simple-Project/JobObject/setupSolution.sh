#!/bin/bash
set -e

JobWorkDir="/home/runner/work/Jobrunner/Jobrunner/tests/Simple-Project/JobObject"

cd /home/runner/work/Jobrunner/Jobrunner/tests/Simple-Project

# Bash file for environment

echo "Hello from environment script"
export ENV_VAR_1="First environment variable"
Env_Var_2="Second environment variable"

cd /home/runner/work/Jobrunner/Jobrunner/tests/Simple-Project/JobObject

# setup script

echo "Hello from setup script"
echo "ENV_VAR_1=$ENV_VAR_1"
echo "Env_Var_2=$Env_Var_2"
