# file: swait_unittests0.py
# info: unit testing swait.py

import unittest
import swait
import subprocess

debugOn = False

class SwaitUnitTests(unittest.TestCase):
    # -- Helper members and methods --

    jobid = None
    p = None

    def run_terminal_cmnd(self,command):
        try:
            self.p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            if debugOn: print 'subprocess.Popen error! \n'
            sys.exit(-1)

    def get_jobid_from_sbatchtxt(self):
        # Make sure to run run_terminal_cmnd() before calling this method.
        if self.p != None:
            for line in self.p.stdout.readlines():
                tmp = line.split()
                if tmp >= 3:
                    self.jobid = tmp[3]
                    if debugOn: print 'jobid: ',self.jobid,'\n'
                    return self.jobid

    def print_swait_output(self):
        # Use after appropriate function calls. (Swait needs to set the dbg flag to get any output)
        if self.p != None:
            for line in self.p.stdout.readlines():
                    print line,'\n'

    def tearDown(self):
        self.jobid = None
        self.terminal_command = None
        p = None
        
    # -- Test functions --------------

    def test_searchfor_single_jobid(self):
        #Step 1:    Launch "sbatch hello.sl" and get the "Submitted batch job JOBID" text. Extract the JOBID.
        self.run_terminal_cmnd('sbatch hello.sl')
        self.get_jobid_from_sbatchtxt()

        #Step 2:    Run "python swait.py -j JOBID -dbg 1"
        #self.run_terminal_cmnd('python swait.py -j '+self.jobid+' -dbg 1')
        self.run_terminal_cmnd('python swait.py -j '+self.jobid)
        #self.print_swait_output()  # needs the dbg flag to be set

        #Step 3:    Wait for the job to complete and swait to return "0".
        data = self.p.communicate()[0] # communicate() needs to be called before 'returncode' can be accessed (double check the docs!)
        retval = self.p.returncode

        self.assertEqual(retval,0)

    def test_searchfor_list_of_jobids(self):
        self.run_terminal_cmnd('sbatch arrayjob.sl')
        self.get_jobid_from_sbatchtxt()

        #constructing argument for list of jobids
        arg = self.jobid+'_1'+' '+self.jobid+'_2'+' '+self.jobid+'_3'+' '+self.jobid+'_4'+' '+self.jobid+'_5'
        
        self.run_terminal_cmnd('python swait.py -j '+arg)

        data = self.p.communicate()[0]
        retval = self.p.returncode

        self.assertEqual(retval,0)

    def test_searchfor_single_jobid_in_jobarrary(self):
        self.run_terminal_cmnd('sbatch arrayjob.sl')
        self.get_jobid_from_sbatchtxt()

        self.run_terminal_cmnd('python swait.py -j '+self.jobid)

        data = self.p.communicate()[0]
        retval = self.p.returncode

        self.assertEqual(retval,0)
        
    def test_searchfor_user(self):
        self.run_terminal_cmnd('sbatch hello.sl')
        self.run_terminal_cmnd('python swait.py -u rsam046')

        data = self.p.communicate()[0]
        retval = self.p.returncode

        self.assertEqual(retval,0)

    def test_searchfor_jobname(self):
        self.run_terminal_cmnd('sbatch hello.sl')
        self.run_terminal_cmnd('python swait.py -n hello')

        data = self.p.communicate()[0]
        retval = self.p.returncode

        self.assertEqual(retval,0)
        

if __name__ == '__main__':
    unittest.main()


    




    
