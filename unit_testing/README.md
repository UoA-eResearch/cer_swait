Unit Testing Doc
================
#### Files involved in testing
* `unittests_offline.py`: Runs the unit tests offline using dummy input.
* `unittests_online.py`: Runs the unit tests on the cluster using the files `hello.sl` and `arrayjob.sl` as inputs
* `dummypoll.py`: Generates a dummy `squeue` output
* `swait.py` : A slightly different version of swait, modified to call `dummypoll.py`
* `hello.sl`: A test input file
* `arrayjob.sl` A test input file

####1.  Running unit tests offline

Execute `unittests_offline.py` with `swait.py` and `dummypoll.py` in the same directory.

Note: The copy of `swait.py` in this directory is slightly different and is set to poll `dummypoll.py` instead of `squeue`. 

See line no. 296 in `swait.py`, it calls
```python
swait = Swait('python dummypoll.py')
```


#####Example test session
```bash
$ python unittests_offline.py
.....
----------------------------------------------------------------------
Ran 5 tests in 20.328s

OK
```

####2. Running unit tests on the cluster
#####Example test session (Note: the relevant files are stored and run on the cluster)

```bash
$ python unittests_online.py
.....
----------------------------------------------------------------------
Ran 5 tests in 263.461s

OK
```

