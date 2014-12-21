Unit Testing Doc
================
#### Files involved in testing
* `unittests_offline_0.py`: Runs the unit tests offline. The necessary variables are set directly by importing swait.
* `unittests_offline_1.py`: Runs the unit tests offline using dummy input via command line.
* `unittests_online.py`: Runs the unit tests on the cluster using the files `hello.sl` and `arrayjob.sl` as inputs
* `dummypoll.py`: Generates a dummy `squeue` output
* `swait.py` : A slightly different version of swait, modified to call `dummypoll.py`
* `hello.sl`: A test input file
* `arrayjob.sl` A test input file

####1.  Running unit tests offline

Execute `unittests_offline_0.py` with `swait.py` and `dummypoll.py` in the same directory.

Note: The copy of `swait.py` in this directory is slightly different and is set to poll `dummypoll.py` instead of `squeue`. 


See line no. 296 in `swait.py`, it calls
```python
swait = Swait('python dummypoll.py')
```

#####Example test session
```bash
$ python unittests_offline_0.py

Test: search under default user
.Test: search for list of JOBIDs
.Test: search for range of JOBIDs
.Test: search for single JOBID
.Test: search for USERID
.
----------------------------------------------------------------------
Ran 5 tests in 25.154s

OK
```

####2. Running unit tests on the cluster
#####Example test session (Note: the relevant files are stored and run on the cluster)

```bash
$ python unittests_online.py
Test: search for DEFAULTUSER
.Test: search for JOBNAME
.Test: search for list of JOBIDs
.Test: search for range of JOBIDs
.Test: search for single JOBID
.Test: search for USERID
.
----------------------------------------------------------------------
Ran 6 tests in 322.172s

OK
```

