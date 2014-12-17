Unit Testing Doc
----------------
Files:	
	- unittests_offline.py  // runs unit tests offline using dummy input.
    - unittests_online.py   // runs unit tests on the cluster using hello.sl and arrayjob.sl as inputs
    - dummypoll.py          // generates a dummy `squeue` output
    - swait2.py             // unit testing version of the swait script.
	- hello.sl
	- arrayjob.sl

Info
---------
`unittests_online.py` needs to be run on the cluster using the test jobs `hello.sl` and `arrayjob.sl`. 

`unittests_offline.py` runs `swait2.py` which in turns calls `dummypoll.py` to generate dummy input


