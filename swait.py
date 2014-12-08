# file: swait.py
# info: handles all parsing, blocking and polling events for swait.
# usage:        

import os
import sys
import argparse
import subprocess
import time

'''
Notes:
        Quick Usage Notes:
        1. Waiting for a single Job ID to complete.
                swait.py -j [jobid]
        2. Waiting for list of Job ID's (separated by whitespace) to complete.
                swait.py -j [jobid1] [jobid2] [jobid3] [jobidn]
        3. waiting for Job ID's in range (separated by whitespace) to complete.
                swait.py -j [jobid_start] [jobid_end]
        4. Waiting for a specific users jobs to complete.
                swait.py -u [userid]
        5. Waiting for specific job name to complete.
                swait.py -n [jobname]

Swait return codes:
        -1 = Polling error.
         0 = Successfull job completion.    
'''

def poll_terminal(dictionary):           

        try:
                if global_variables['default_on'] == True:
                        p = subprocess.Popen('squeue -u '+global_variables['whoami'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                else:
                        p = subprocess.Popen('squeue', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
                sys.exit(-1)
                        

        for line in p.stdout.readlines():               
                tmp = line.split()
                
                if (len(tmp) >= 3):
                        global_variables['match_job_id'] = tmp[0]
                        global_variables['match_job_name'] = tmp[2]
                        global_variables['match_user_id'] = tmp[3]
                        
                        # Search for JOB ID
                        if global_variables['job_id'] != None:
                                if global_variables['match_job_id'] == global_variables['job_id']:
                                        if global_variables['debug_mode']:  print '[DBG] Job still active..'
                                        return True

                                if "_" in global_variables['match_job_id']:
                                        if global_variables['job_id'] in global_variables['match_job_id']:
                                                if global_variables['debug_mode']:  print '[DBG] Job still active..'
                                                return True
                                
                        # Search for JOB ID's in range
                        if global_variables['job_id_range_start'] != None:
                                for x in xrange(int(global_variables['job_id_range_start']),int(global_variables['job_id_range_end'])+1):
                                        # if there is atleast one match, return as success.
                                        if global_variables['match_job_id'] == str(x):
                                                if global_variables['debug_mode']:  print '[DBG] Job still active..'
                                                return True

                        # Search for JOB ID's in list
                        if len(global_variables['job_id_list']) != 0:
                                for x in global_variables['job_id_list']:
                                        if global_variables['match_job_id'] == x:
                                                if global_variables['debug_mode']:  print '[DBG] Job still active..'
                                                return True
                                                
                        # Search for USER ID
                        if global_variables['user_id'] != None:
                                if global_variables['match_user_id'] == global_variables['user_id']:
                                        if global_variables['debug_mode']:  print '[DBG] Job still active..'
                                        return True

                        # Search for JOB NAME
                        if global_variables['job_name'] != None:

                                # Resetting Lists
                                global_variables['jobname_list'] = []
                                global_variables['jobid_list_for_searching_jobnames'] = []

                                #Step 1. Create list of job id's

                                # Note: Only searches for current logged in user. Otherwise,
                                # it would search the entire cluster for jobs and cause a large delay.
                                w = subprocess.Popen('squeue -u '+global_variables['whoami'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                                for line in w.stdout.readlines():
                                        tmp = line.split()
                                       
                                        if (len(tmp)>= 3):
                                                if ( (tmp[0] != "JOBID") and (tmp[1] != "job(s)") ):
                                                        # in order not to append garbage..
                                                        global_variables['jobid_list_for_searching_jobnames'].append(tmp[0])

                                #Step 2. using scontrol and the jobids in list, get all job names and append to another list

                                for x in global_variables['jobid_list_for_searching_jobnames']:
                                        command = "scontrol show jobid="+x

                                        z = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                                        for line in z.stdout.readlines():
                                                tmp = line.split()

                                                if len(tmp)>=3:
                                                        if "JobId" in tmp[0]:
                                                                tmp_jobname = tmp[3].strip('Name=')
                                                                global_variables['jobname_list'].append(tmp_jobname)

                                #Step 3. using the list of job names, use what the user inputed to match and see if the specified job is
                                #   is still active and in the list..

                                for x in global_variables['jobname_list']:
                                        if x == global_variables['job_name']:
                                                if global_variables['debug_mode']:  print '[DBG] Job still active..'
                                                return True
                                return False


                        # Search for when Default is on: Wait until all job(s) of the current logged in user is complete..
                        if global_variables['default_on'] == True:
                                if global_variables['match_user_id'] == global_variables['whoami']:
                                        if (global_variables['match_job_id'] != "JOBID"):
                                                if global_variables['debug_mode']:  print '[DBG] Job still active..'
                                        return True
        return False


def block_until_not_found(dictionary):
        
        while (poll_terminal(global_variables) != False):
                time.sleep(float(global_variables['polling_freq']))
                
        if global_variables['debug_mode']:  print '[DBG] Job finished (or it was never there to begin with)'
        return 0


if __name__ == "__main__":

        global_variables = {'polling_freq' : 5,
                            'debug_mode' : False,
                            'job_id' : None,
                            'job_id_range_start' : None,
                            'job_id_range_end' : None,
                            'user_id' : None,
                            'job_name' : None,
                            'match_job_id' : None,
                            'match_job_name' : None,
                            'match_user_id' : None,
                            'job_id_list' : [],
                            'whoami' : None,
                            'default_on' : False,
                            'jobid_list_for_searching_jobnames' : [],   #different var name?!
                            'jobname_list' : []
                           }
        
        global_variables['whoami'] = os.popen("whoami").read()
        global_variables['whoami'] = global_variables['whoami'].strip('\n')

        parser = argparse.ArgumentParser(argument_default=global_variables['whoami'],description='Waits for specified job(s) to finish and returns true on completion.')
        group = parser.add_mutually_exclusive_group()
        
        group.add_argument('--job','-j',help='Wait until a specific job ID completes.',nargs='*',default=None)
        group.add_argument('--user','-u',help='Wait until all jobs for a specific user completes.',nargs=1,default=None)
        group.add_argument('--name','-n',help='Wait until specified job name completes.',nargs=1,default=None)

        parser.add_argument('--pollfreq','-pf',help='Set polling frequency.',nargs=1,default=5)
        parser.add_argument('--debug','-dbg',help='Turn on debug messages. (Enter 1 for true or 0 for false)',nargs=1, type=bool,default=False)

        args = parser.parse_args()

        if args.job:
                if len(args.job) == 1:
                        # for when a single job ID given
                        global_variables['job_id'] = args.job[0]
                        if global_variables['debug_mode']:  print '[DBG] the job id that was given was: ', args.job[0],'\n'
                if len(args.job) == 2:
                        # for when a range of job ID's given
                        global_variables['job_id_range_start'] = args.job[0]
                        global_variables['job_id_range_end'] = args.job[1]
                        if global_variables['debug_mode']:  print '[DBG] the job id range given was: ', args.job[0],' and ', args.job[1], '\n'
                if len(args.job) > 2:
                        for x in args.job:
                                global_variables['job_id_list'].append(x)
                                if global_variables['debug_mode']:  print '[DBG] the job id list contains: ', x , '\n'
                        
        if args.user:
                global_variables['user_id'] = args.user[0]
                if global_variables['debug_mode']:  print '[DBG] the user that was given was: ', args.user[0],'\n'

        if args.name:
                global_variables['job_name'] = args.name[0]
                if global_variables['debug_mode']:  print '[DBG] the job name that was given was: ', args.name[0],'\n'

        if args.pollfreq:
                global_variables['polling_freq'] = args.pollfreq
                if global_variables['debug_mode']:  print '[DBG] polling frequency set at: ', args.pollfreq[0],'\n'

        if args.debug:
                global_variables['debug_mode'] = bool(args.debug)
                if global_variables['debug_mode']:  print '[DBG] Debug mode turned ON: ', args.debug[0],'\n'


        if (args.job == None) and (args.user == None) and (args.name == None):
                global_variables['default_on'] = True
                if global_variables['debug_mode']:  print '[DBG] no arugments given, running as default user: ',global_variables['whoami'],'\n',

        sys.exit(block_until_not_found(global_variables))


        

