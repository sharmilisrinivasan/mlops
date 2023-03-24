#!/bin/sh
# Command to run
# docker run --user root -e CONDA_ENV_NAME=<pbtxt_name> -v <folderpath>:/model ubuntu:latest /model/build_env.sh

# setting up conda
apt-get update && apt-get install -y wget
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh
sh Miniconda3-py39_4.11.0-Linux-x86_64.sh -b -p $HOME/miniconda
eval "$(/root/miniconda/bin/conda shell.bash hook)"

# creating conda environment
conda create -k -y -n ${CONDA_ENV_NAME} python=3.8
conda activate ${CONDA_ENV_NAME}

# installing dependencies
pip install numpy conda-pack
pip install -r /model/requirements.txt

file="/model/${CONDA_ENV_NAME}.tar.gz"
if [ -f "$file" ]; then
  echo "Removing existing $file file"
  rm -rf $file
fi


# packaging conda environment
conda pack -o /model/${CONDA_ENV_NAME}.tar.gz
