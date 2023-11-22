#!/bin/bash -x

echo "Activating venv"

source ~/venvs/torch/bin/activate
# Execute your pipeline python project/pipeline.py

echo "Starting the data engineering pipeline"

python data_engineering_pipeline.py


read -p "Press any key to continue... " -n1 -s
exit 0
