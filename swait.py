# file: swait.py
# description: waits for a specified job on the cluster to complete and returns 0 on completion.
# usage:
#       1. Waiting for a single Job ID to complete. `swait.py -j [JOBID]`
#       2. Waiting for list of Job ID's (separated by whitespace) to complete. `swait.py -j [JOBID1] [JOBID2] [JOBID3] [JOBIDn]`
#       3. Waiting for a range of Job ID's to complete. `swait.py -jr [JOBID_START] [JOBID_END]`
#       4. Waiting for a specific users' jobs to complete. `swait.py -u [USERID]`
#       5. Waiting for specific job name to complete. (note: this only works for the current logged in user) `swait.py -n [JOBNAME]`
# Swait return codes:
#       0 = Successfull job completion.
#       1 = Polling error.
#       2 = Invalid input.

import os
import sys
import argparse
import subprocess
import time

class Swait:
    
    polling_freq = 5
    debug_mode = False
    job_id = None
    job_id_range_start = None
    job_id_range_end = None
    user_id = None
    job_name = None
    job_id_list = []
    whoami = None
    default_on = False
    jobid_list_for_searching_jobnames = []
    jobname_list = []
    default_on = False


    def __init__(self):
        self.whoami = os.popen("whoami").read()
        self.whoami = self.whoami.strip('\n')

        parser = argparse.ArgumentParser(argument_default=self.whoami,description='Waits for specified job(s) to finish and returns true on completion. (note: if a particular job did not exist on the cluster to begin with, swait will return true).')
        group = parser.add_mutually_exclusive_group()
        
        group.add_argument('--job','-j',help='Wait until a specific job ID completes. Either a single id or a list of ids separated by a whitespace.',nargs='*',default=None)
        group.add_argument('--jobrange','-jr',help='Wait for a range of job IDs to complete. (Enter the startID and endID separated by a white space).',nargs=2,default=None)
        group.add_argument('--user','-u',help='Wait until all jobs for a specific user completes.',nargs=1,default=None)
        group.add_argument('--name','-n',help='Wait until specified job name completes. (note: this only works for the current logged in users\' jobs).',nargs=1,default=None)

        parser.add_argument('--pollfreq','-pf',help='Set polling frequency.',nargs=1,default=5)
        parser.add_argument('--debug','-dbg',help='Turn on debug messages. (Enter 1 for true or 0 for false)',nargs=1, type=bool,default=False)

        args = parser.parse_args()

        if args.job:
                if len(args.job) == 1:
                        # for when a single job ID given
                        self.job_id = args.job[0]
                        if self.debug_mode:  print '[DBG] the job id that was given was: ', args.job[0],'\n'
                        
                if len(args.job) > 2:
                        # for when a list of job ID's given
                        for x in args.job:
                                self.job_id_list.append(x)
                                if self.debug_mode:  print '[DBG] the job id list contains: ', x , '\n'
       
        if args.jobrange:
                # for when a range of job ID's given
                if ('_' in args.jobrange[0]) or ('_' in args.jobrange[1]):
                        if self.debug_mode: print '[DBG] invalid input: range id\'s cannot contain underscores.\n'

                        sys.exit(2)
                        
                self.job_id_range_start = args.jobrange[0]
                self.job_id_range_end = args.jobrange[1]
                if self.debug_mode:  print '[DBG] the job id range given was: ', args.jobrange[0],' and ', args.jobrange[1], '\n'

        if args.user:
                self.user_id = args.user[0]
                if self.debug_mode:  print '[DBG] the user that was given was: ', args.user[0],'\n'

        if args.name:
                self.job_name = args.name[0]
                if self.debug_mode:  print '[DBG] the job name that was given was: ', args.name[0],'\n'

        if args.pollfreq:
                self.polling_freq = args.pollfreq
                if self.debug_mode:  print '[DBG] polling frequency set at: ', args.pollfreq[0],'\n'

        if args.debug:
                self.debug_mode = bool(args.debug)
                if self.debug_mode:  print '[DBG] Debug mode turned ON: ', args.debug[0],'\n'

        if (args.job == None) and (args.jobrange == None) and (args.user == None) and (args.name == None):
                self.default_on = True
                if self.debug_mode:  print '[DBG] no arugments given, running as default user: ',self.whoami,'\n',


    def poll_terminal(self,arg = None):
        try:
            if arg != None:
                p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            elif self.default_on == True:
                p = subprocess.Popen('squeue -u '+self.whoami, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                p = subprocess.Popen('squeue', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        except:
                if self.debug_mode:  print '[DBG] polling error.'
                sys.exit(1)
        return p
    

    def block_until_not_found(self):
        while (self.search_cluster_for_jobs() != False): 
            time.sleep(float(self.polling_freq))

        if self.debug_mode:  print '[DBG] Job finished (or it was never there to begin with)'
        return 0

      
    def search_cluster_for_jobs(self):
        # Search for JOBID
        if self.job_id != None:
            return( self.search_for_jobid(self.job_id) )

        # Search for JOB ID's in range
        if self.job_id_range_start != None:
            return( self.search_for_jobids_inrange(self.job_id_range_start,self.job_id_range_end) )

        # Search for JOB ID's in list
        if len(self.job_id_list) != 0:
            return( self.search_for_jobids_inlist(self.job_id_list) )

        # Search for USER ID
        if self.user_id != None:
            return( self.search_for_userid(self.user_id) )

        # Search for JOB NAME
        if self.job_name != None:
            return( self.search_for_jobname(self.job_name) )

        # Search for when Default is on: Wait until all job(s) of the current logged in user is complete..
        if self.default_on == True: # or just if () instead of being so explicit?
            return( self.search_for_default_usersjobs(self.whoami) )


    def search_for_jobid(self,job_id):
        p = self.poll_terminal()

        for line in p.stdout.readlines():               
            tmp = line.split()

            if (len(tmp) >= 3):
                match_job_id = tmp[0]
                
                if match_job_id == self.job_id:
                    if self.debug_mode:  print '[DBG] Job still active..'
                    return True

                if "_" in match_job_id:
                    if self.job_id in match_job_id:
                        if debug_mode:  print '[DBG] Job still active..'
                        return True
        return False


    def search_for_jobids_inrange(self,job_id_range_start,job_id_range_end):
        p = self.poll_terminal()

        for line in p.stdout.readlines():               
            tmp = line.split()

            if (len(tmp) >= 3):

                match_job_id = tmp[0]

                for x in xrange(int(self.job_id_range_start),int(self.job_id_range_end)+1):
                    # if there is atleast one match, return as success.
                    if match_job_id == str(x):
                        if self.debug_mode:  print '[DBG] Job still active..'
                        return True
        return False


    def search_for_jobids_inlist(self,job_id_list):
        p = self.poll_terminal()

        for line in p.stdout.readlines():               
            tmp = line.split()

            if (len(tmp) >= 3):

                match_job_id = tmp[0]

                for x in self.job_id_list:
                    if match_job_id == x:
                        if self.debug_mode:  print '[DBG] Job still active..'
                        return True
        return False


    def search_for_userid(self,user_id):
        p = self.poll_terminal()

        for line in p.stdout.readlines():               
            tmp = line.split()

            if (len(tmp) >= 3):
                
                match_user_id = tmp[3]

                if match_user_id == self.user_id:
                    if self.debug_mode:  print '[DBG] Job still active..'
                    return True
        return False


    def search_for_jobname(self,job_name):
        # Resetting Lists
        self.jobname_list = []
        self.jobid_list_for_searching_jobnames = []

        #Step 1. Create list of job id's
        # Note: Only searches for current logged in user. Otherwise,
        # it would search the entire cluster for jobs and cause a large delay.

        w = self.poll_terminal('squeue -u '+self.whoami)

        for line in w.stdout.readlines():
            tmp = line.split()
                      
            if (len(tmp)>= 3):
                if ( (tmp[0] != "JOBID") and (tmp[1] != "job(s)") ):
                    # in order not to append garbage..
                    self.jobid_list_for_searching_jobnames.append(tmp[0])

        #Step 2. using scontrol and the jobids in list, get all job names and append to another list

        for x in self.jobid_list_for_searching_jobnames:

            command = "scontrol show jobid="+x
            z = self.poll_terminal(command)

            for line in z.stdout.readlines():
                tmp = line.split()

                if len(tmp)>=2:

                    if "JobId" in tmp[0]:
                        tmp_jobname = tmp[1].strip('Name=')
                        self.jobname_list.append(tmp_jobname)

        #Step 3. using the list of job names, use what the user inputed to match and see if the specified job is
        #   is still active and in the list..

        for x in self.jobname_list:
            if x == self.job_name:
                if self.debug_mode:  print '[DBG] Job still active..'
                return True

        return False


    def search_for_default_usersjobs(self,whoami):
        p = self.poll_terminal()

        for line in p.stdout.readlines():               
            tmp = line.split()

            if (len(tmp) >= 3):

                match_job_id = tmp[0]
                match_user_id = tmp[3]

                if match_user_id == self.whoami:
                    if (match_job_id != "JOBID"):
                        if self.debug_mode:  print '[DBG] Job still active..'
                        return True

        print 'returning false'
        return False



if __name__ == "__main__":

    swait = Swait()
    sys.exit(swait.block_until_not_found())








            
