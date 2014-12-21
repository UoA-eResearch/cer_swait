# file: unittesting_swaitfunctions.py
# info: unit testing swait

import unittest
from swait import Swait
import subprocess
import time
import os

class SwaitUnitTests(unittest.TestCase):
    # -- Helper members and methods --
    swait = None    
    def setUp(self):
        self.swait = Swait('python dummypoll.py')

        START_TIME = float(time.time())
        fo = open('timer.txt','wb+')
        fo.write('START_TIME='+str(START_TIME))
        fo.close()

    def tearDown(self):
        os.remove('timer.txt')    
    
    # -- Test Functions --
    def test_searchfor_single_jobid(self):
        print 'Test: search for single JOBID'

        self.swait.job_id = 12000000
        
        self.assertEqual(self.swait.block_until_not_found(),0)

    def test_searchfor_list_of_jobids(self):
        print 'Test: search for list of JOBIDs'

        self.swait.job_id_list.append(12000001)
        self.swait.job_id_list.append(12000002)
        self.swait.job_id_list.append(12000003)
        self.swait.job_id_list.append(12000004)
        self.swait.job_id_list.append(12000005)

        self.assertEqual(self.swait.block_until_not_found(),0)
    
    def test_searchfor_range_of_jobids(self):
        print 'Test: search for range of JOBIDs'

        self.swait.job_id_range_start = 12000000
        self.swait.job_id_range_end = 12000008

        self.assertEqual(self.swait.block_until_not_found(),0)
        
    def test_searchfor_user(self):
        print 'Test: search for USERID'

        self.swait.user_id = "rsam046"

        self.assertEqual(self.swait.block_until_not_found(),0)  

    def test_searchfor_defaultuser(self):
        print 'Test: search under default user'
        self.swait.job_id = None
        self.swait.job_id_range_start = None
        self.swait.user_id = None
        self.swait.job_name = None
        self.swait.whoami = "rsam046"

        self.assertEqual(self.swait.block_until_not_found(),0)

    '''
    NOTE:
        searching for a JOBNAME requires access to the scontrol function.
        since it is not available off the cluster. This test is omitted.
    
    def test_searchfor_jobname(self):
        print 'Test: search for JOBNAME'
        self.swait.job_name = "hello"

        self.assertEqual(self.swait.block_until_not_found(),0)
    '''
   
if __name__ == '__main__':
    unittest.main()

