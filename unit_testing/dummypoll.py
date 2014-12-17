# file: dummypoll.py
# description: fakes squeue output; used in unit testing swait
#
# Notes:
#   swait2.py calls `dummypoll.py` inside its poll_terminal() function, instead of
#   calling `squeue`.
#
#   if the elapsed_time value is greater than the timeout value, then this script omits all job
#   listings by rsam046 to fake that those jobs have been "completed".

import sys

no_args = len(sys.argv)
arg_list = list(sys.argv)
elapsed_time = None
timeout = 5

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

# Setting elapsed time..
if len(arg_list) == 2:   
        elapsed_time = int(arg_list[1])

# if elapsed is greater than our predetermined timeout value, then omit fields.
if elapsed_time > timeout:
    print squeue_dummy_output[0]
    for i in range(10,16):
        print squeue_dummy_output[i]

# otherwise print complete "cluster"
else:
    for x in squeue_dummy_output:
        print x


