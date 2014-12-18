#!/bin/bash

x=$(sbatch examplejob.sl)   # 1. Run sbatch with the input file "examplejob.sl".
JOBID=($x)                  # 2. Grab the output from sbatch and extract and
JOBID=${JOBID[3]}           #    store the job id.

python swait.py -j $JOBID   # 3. Run swait with the job id.

# Checks for successful job completion..
if [ "$?"==0 ]
 then
  echo "Job: ${JOBID} completed successfully!"
fi

# Note: '$?' returns the exit code of the previously executed command.
# In our case, the exitcode from swait.

