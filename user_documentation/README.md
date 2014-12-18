Swait User Documentation 
========================
###1. Introduction 
The purpose of swait is to check whether a specified job on the cluster has completed its operation. 

Jobs can be searched for by specifying either the: 
* `JOBID`
* `USERID`
* or `JOBNAME` 

Search parameters are set by specifying the `-j` `-jr` `-u` and `-n` flags. 

Where,
* `-j` is for specifying a single JOBID or list of JOBIDs 
* `-jr` for specifying a range of JOBIDs
* `-u` for specifying a particular user that has active jobs on the cluster.
* `-n` for specifying a jobname

Optional parameters,
* `-dbg` turns on debug mode (OFF by default)
* `-pf` sets the polling frequency (I.e how often swait checks the cluster for changes. Set at 5 seconds by default)

###2. Quick Usage Notes 

1. Waiting for a single Job ID to complete: `swait.py -j [JOBID]` 
2. Waiting for list of Job ID's (separated by whitespace) to complete: `swait.py -j [JOBID1] [JOBID2] [JOBID3] [JOBIDn]` 
3. Waiting for a range of Job ID's to complete: `swait.py -jr [JOBID_START] [JOBID_END]`
4. Waiting for a specific users' jobs to complete: `swait.py -u [USERID]` 
5. Waiting for specific job name to complete: `swait.py -n [JOBNAME]` , note: this only works for the current logged in user
6. Turning Debug messages ON: `swait.py -dbg 1` , where a `1 = ON` & `0 = OFF`
7. Setting the polling frequency: `swait.py -pf 10`

####Swait return codes: 
`0 = Successfull job completion.` 
`1 = Polling error.` 
`2 = Invalid input.` 

###3. Usage examples

####1. Using swait on the terminal
 
 run the file `examplejob.sl` on the cluster by executing 
```bash
$ sbatch examplejob.sl
```
The above command would then output `Submitted batch job [JOBID]`. In this example sbatch outputs the following 
```bash
Submitted batch job 12050168
```
We then execute swait to wait for the job `12050168` to complete.
```bash
$ python swait.py -j 12050168 -dbg 1 
```
Note: the `-dbg 1` flag turns on debug messages. 

The output of the last command looks as follows 
```bash
[DBG] Debug mode turned ON: True 
[DBG] Searching for JOBID: 12050191 
[DBG] Polling frequency set at: 5 seconds. 
[DBG] Job still active.. [DBG] Job still active..
[DBG] Job still active.. [DBG] Job still active.. 
[DBG] Job still active.. [DBG] Job still active.. 
[DBG] Job finished (or it was never there to begin with) 
```
swait will then return control to the terminal prompt and return `0` indicating a successful job completion. 

####2. An example workflow utilizing swait 

```bash
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
```

The above script shows how you would implement swait to determine whether a particular job had completed by checking its return value.


