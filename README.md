cer_swait
=========
Quick Usage Notes
-----------------
1. Waiting for a single Job ID to complete. `swait.py -j [JOBID]`
2. Waiting for list of Job ID's (separated by whitespace) to complete. `swait.py -j [JOBID1] [JOBID2] [JOBID3] [JOBIDn]`
3. Waiting for a range of Job ID's to complete. `swait.py -jr [JOBID_START] [JOBID_END]`
4. Waiting for a specific users' jobs to complete. `swait.py -u [USERID]`
5. Waiting for specific job name to complete. (note: this only works for the current logged in user) `swait.py -n [JOBNAME]`

Swait return codes
------------------
* 0 = Successfull job completion.
* 1 = Polling error.
* 2 = Invalid input.
