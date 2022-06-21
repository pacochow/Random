#!/bin/bash
#$ -q short.qc
#$ -t 1-1:1 
#$ -j y
#$ -r y 
#$ -o /well/saxe/users/qbe080/logs 
#$ -wd /well/saxe/users/qbe080/Lols

echo "------------------------------------------------"
echo "Run on host: "`hostname`
echo "Operating system: "`uname -s`
echo "Username: "`whoami`
echo "Started at: "`date`
echo "------------------------------------------------"

source ~/.bashrc
conda activate for_fun
python Chaos_game.py ${SGE_TASK_ID}

