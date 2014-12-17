# file: swait_unittest1.py
# info: unit testing swait.py offline with mock input

import unittest
import swait2
import subprocess
import time

debugOn = False

class SwaitUnitTests(unittest.TestCase):
    # -- Helper members and methods --
    p = None

    def run_terminal_cmnd(self,command):
        try:
            self.p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            if debugOn: print 'subprocess.Popen error! \n'
            sys.exit(-1)

    def tearDown(self):
        self.p = None


    # -- Test Functions
    def test_searchfor_single_jobid(self):

        # The job ID 12000000 is defined within the dummypoll.py script..
        self.run_terminal_cmnd('python swait2.py --unittests 1 -dbg 1 -j 12000000')

        data = self.p.communicate()[0]
        retval = self.p.returncode
        self.assertEqual(retval,0)

    def test_searchfor_list_of_jobids(self):

        self.run_terminal_cmnd('python swait2.py --unittests 1 -dbg 1 -j 12000001 12000002 12000003 12000004 12000005')

        data = self.p.communicate()[0]
        retval = self.p.returncode

        self.assertEqual(retval,0)

    def test_searchfor_range_of_jobids(self):
        
        self.run_terminal_cmnd('python swait2.py --unittests 1 -dbg 1 -jr 12000000 12000008')
        
        data = self.p.communicate()[0]
        retval = self.p.returncode

        self.assertEqual(retval,0) 

    def test_searchfor_user(self):

        self.run_terminal_cmnd('python swait2.py --unittests 1 -dbg 1 -u rsam046')

        data = self.p.communicate()[0]
        retval = self.p.returncode

        self.assertEqual(retval,0)

    def test_searchfor_jobname(self):

        self.run_terminal_cmnd('python swait2.py --unittests 1 -dbg 1 -n hello')

        data = self.p.communicate()[0]
        retval = self.p.returncode

        self.assertEqual(retval,0)


if __name__ == '__main__':
    unittest.main()






