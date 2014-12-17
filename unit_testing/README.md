Unit Testing Doc
================
Files:
------	
	* `unittests_offline.py`    -runs unit tests offline using dummy input.
    * `unittests_online.py`     -runs unit tests on the cluster using hello.sl and arrayjob.sl as inputs
    * `dummypoll.py`            -generates a dummy `squeue` output
    * `swait.py`                -cmd is set to `python dummypoll.py` to poll `dummypoll.py` instead of `squeue`
    * `timer.txt`               -holds the start time that `unittest_offline.py` & `dummypoll.py` uses.
	* `hello.sl`
	* `arrayjob.sl`

Info
----
`unittests_online.py` needs to be run on the cluster using the test jobs `hello.sl` and `arrayjob.sl`. 

`unittests_offline.py` runs `swait.py` which in turns calls `dummypoll.py` to generate dummy input

