#!/bin/bash

#SBATCH -J arrayjob
#SBATCH -A uoa99999         # Project Account
#SBATCH --time=01:00:00     # Walltime
#SBATCH --mem-per-cpu=1024  # memory/cpu (in MB)
#SBATCH --array=1-5

srun echo $SLURM_ARRAY_TASK_ID
sleep 60

