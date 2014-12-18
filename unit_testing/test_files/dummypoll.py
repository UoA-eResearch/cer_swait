# file: dummypoll.py
# description: fakes squeue output; used in unit testing swait
#
# Notes:
#   - `swait.py` calls `dummypoll.py` instead of `squeue` when cmd is set to `python dummypoll.py` inside
#     `swait.py`
#   - if the elapsed_time value is greater than the timeout value, then this script omits all job
#     listings by rsam046 to fake that those jobs have been "completed".

import sys
import time

# -- Global Var's

TIMEOUT = 5
squeue_dummy_output = [ 'JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON))',
                        '12000000      high    hello  rsam046  R       0:20      1 compute-bigmem-001',
                        '12000001      high    hello  rsam046  R       0:25      1 compute-bigmem-001',
                        '12000002      high    hello  rsam046  R      12:08      1 compute-bigmem-001',
                        '12000003      high    hello  rsam046  R    3:56:14      1 compute-stats-006',
                        '12000004      high    hello  rsam046  R    3:56:14      1 compute-stats-006',
                        '12000005      high    hello  rsam046  R    3:56:14      1 compute-stats-006',
                        '12000006      high    hello  rsam046  R    3:56:24      1 compute-stats-008',
                        '12000007      high    hello  rsam046  R    3:56:24      1 compute-stats-007',
                        '12000008      high    hello  rsam046  R    3:56:24      1 compute-stats-007',
                        '12048664      high 1_403gen  dxie004  R      57:47      1 compute-bigmem-002', # index = 10
                        '12048684      high 1_403gen  dxie004  R      57:47      1 compute-bigmem-002',
                        '12048704      high 1_403gen  dxie004  R      57:47      1 compute-bigmem-002',
                        '12048724      high 1_403gen  dxie004  R      57:47      1 compute-bigmem-001',
                        '12048584      high 1_403gen  dxie004  R      57:50      1 compute-bigmem-002',
                        '6051 job(s) queued, 801 pending, 3398 running, 1852 suspended'                 # index = 15
                      ]

# -- Reading file to get the start time that unittests_offline.py had set..

try:
    with open('timer.txt','rb') as fi:
        START_TIME = fi.read()
except:
    print 'error: \'timer.txt\' has not been set. '
    sys.exit(1)
fi.close()

# -- Grabbing the start time from text file.

START_TIME = START_TIME.strip("START_TIME=")
START_TIME = float(START_TIME)

# -- Getting the current time..

END_TIME = time.time()

# -- Calculating the elapsed time..

ELAPSED_TIME = END_TIME - START_TIME

# if elapsed is greater than our predetermined timeout value, then omit fields.
if ELAPSED_TIME > TIMEOUT:
    print squeue_dummy_output[0]
    for i in range(10,16):
        print squeue_dummy_output[i]

# otherwise print complete "cluster" to show that the jobs are still running..
else:
    for x in squeue_dummy_output:
        print x

