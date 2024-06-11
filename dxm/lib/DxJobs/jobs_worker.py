#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (c) 2018-2020 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : April 2018


from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
import logging
import sys
from datetime import datetime
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.Output.DataFormatter import DataFormatter
from dxm.lib.DxTools.DxTools import get_list_of_engines

from dxm.lib.DxEnvironment.DxEnvironment import DxEnvironment
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList

from dxm.lib.DxJobs.DxJobsList import DxJobsList
from dxm.lib.DxJobs.DxJob import DxJob
from dxm.lib.DxJobs.DxProfileJobsList import DxProfileJobsList
from dxm.lib.DxJobs.DxProfileJob import DxProfileJob
from dxm.lib.DxRuleset.DxRulesetList import DxRulesetList
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList
from dxm.lib.DxProfile.DxProfilesList import DxProfilesList
from dxm.lib.DxJobs.DxJobOptions import DxDatabaseMaskingOptions
from dxm.lib.DxJobs.DxJobOptions import DxMaskingScriptJob
from dxm.lib.DxJobs.DxJobOptions import DxOnTheFlyJob


from threading import Thread
from threading import active_count
import time
import os
from tqdm import tqdm
from threading import RLock
import dxm.lib.DxJobs.DxJobCounter


lock = RLock()

masking_params_list =  ("email",
                        "feedback_size",
                        "max_memory",
                        "min_memory",
                        "job_description",
                        "num_input_streams",
                        "multi_tenant")

optional_params_list = ("email",
                        "feedback_size",
                        "max_memory",
                        "min_memory",
                        "job_description",
                        "num_input_streams",
                        "on_the_fly_masking",
                        "multi_tenant")

optional_options_list = ("commit_size",
                         "num_output_threads_per_stream",
                         "batch_update",
                         "bulk_data",
                         "disable_constraints",
                         "drop_indexes",
                         "disable_triggers",
                         "truncate_tables")

def profilejob_add(p_engine, p_username,  params):
    """
    Add profile job to Masking engine
    param1: p_engine: engine name from configuration
    param2: params: job parameters
    return 0 if added, non 0 for error
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine, p_username)

    logger = logging.getLogger()

    envname = params['envname']
    jobname = params['jobname']
    rulesetname = params['rulesetname']
    profilename = params['profilename']

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        joblist = DxProfileJobsList()
        envlist = DxEnvironmentList()
        rulesetlist = DxRulesetList(envname)
        profilesetlist = DxProfilesList()
        profileref = profilesetlist.get_profileSetId_by_name(profilename)
        envlist.LoadEnvironments()
        logger.debug("Envname is %s, job name is %s" % (envname, jobname))
        #rulesetlist.LoadRulesets()
        rulesetref = rulesetlist.get_rulesetId_by_name(rulesetname)


        job = DxProfileJob(engine_obj, None)
        job.create_job(job_name=jobname, ruleset_id=rulesetref, profile_set_id=profileref)

        for p in masking_params_list:
            if params[p] is not None:
                if params[p] == 'Y':
                    value = True
                elif params[p] == 'N':
                    value = False
                else:
                    value = params[p]
                setattr(job.obj, p, value)

        if joblist.add(job):
            ret = ret + 1

    return ret

def job_add(p_engine, p_username,  params):
    """
    Add masking job to Masking engine
    param1: p_engine: engine name from configuration
    param2: params: job parameters
    return 0 if added, non 0 for error
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine, p_username)

    logger = logging.getLogger()

    envname = params['envname']
    jobname = params['jobname']
    rulesetname = params['rulesetname']

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        joblist = DxJobsList()
        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        logger.debug("Envname is %s, job name is %s" % (envname, jobname))
        rulesetlist = DxRulesetList(envname)


        rulesetref = rulesetlist.get_rulesetId_by_name(rulesetname)

        job = DxJob(engine_obj, None, None)
        job.create_job(job_name=jobname, ruleset_id=rulesetref)

        for p in optional_params_list:
            if params[p] is not None:
                if params[p] == 'Y':
                    value = True
                elif params[p] == 'N':
                    value = False
                else:
                    value = params[p]
                setattr(job, p, value)


        dmo = DxDatabaseMaskingOptions()

        for p in optional_options_list:
            if params[p] is not None:
                if params[p] == 'Y':
                    value = True
                elif params[p] == 'N':
                    value = False
                else:
                    value = params[p]
                setattr(dmo, p, value)

        if params["on_the_fly_masking"] == 'Y' :
            src_env = params["on_the_fly_src_envname"]
            src_con = params["on_the_fly_src_connector"]
            conlist = DxConnectorsList(src_env)
            conid = conlist.get_connectorId_by_name(src_con)
            if not conid :
                return 1
            on_the_fly_maskking_srcobj = DxOnTheFlyJob()
            on_the_fly_maskking_srcobj.connector_id = conid[1:]

            conObj = conlist.get_by_ref(conid)
            if conObj.is_database :
                on_the_fly_maskking_srcobj.connector_type = "DATABASE"
            else:
                on_the_fly_maskking_srcobj.connector_type = "FILE"
            job.on_the_fly_masking_source = on_the_fly_maskking_srcobj


        if params["prescript"]:
            scriptname = os.path.basename(params["prescript"].name)
            prescript = DxMaskingScriptJob(name=scriptname, contents=''.join(params["prescript"].readlines()))
            dmo.prescript = prescript

        if params["postscript"]:
            scriptname = os.path.basename(params["postscript"].name)
            postscript = DxMaskingScriptJob(name=scriptname, contents = ''.join(params["postscript"].readlines()))
            dmo.postscript = postscript

        job.database_masking_options = dmo

        if joblist.add(job):
            ret = ret + 1

    return ret

def job_copy(p_engine, p_username,  jobname, envname, newjobname):
    """
    Copy masking job in Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: newjobname: new job name
    return 0 if deleted, non 0 for error
    """
    return job_copy_worker(p_engine, p_username,  jobname, envname, newjobname, "DxJobsList")

def profilejob_copy(p_engine, p_username,  jobname, envname, newjobname):
    """
    Copy profile job in Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: newjobname: new job name
    return 0 if deleted, non 0 for error
    """
    return job_copy_worker(p_engine, p_username,  jobname, envname, newjobname, "DxProfileJobsList")

def job_copy_worker(p_engine, p_username,  jobname, envname, newjobname, joblist_class):
    """
    Copy job in Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: newjobname: new job name
    param5: joblist_class: type of job
    return 0 if deleted, non 0 for error
    """
    return job_selector(
        p_engine=p_engine,
        jobname=jobname,
        envname=envname,
        function_to_call='do_copy',
        newjobname=newjobname,
        joblist_class=joblist_class)

def job_update(p_engine, p_username,  jobname, envname, params):
    """
    Update a job in Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: params: dict with job parameters
    return 0 if updated, non 0 for error
    """
    return job_update_worker(p_engine, p_username,  jobname, envname, params, "DxJobsList")

def profilejob_update(p_engine, p_username,  jobname, envname, params):
    """
    Update a job in Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: params: dict with job parameters
    return 0 if updated, non 0 for error
    """
    return job_update_worker(p_engine, p_username,  jobname, envname, params, "DxProfileJobsList")

def job_update_worker(p_engine, p_username,  jobname, envname, params, joblist_class):
    """
    Update a job in Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: params: dict with job parameters
    param5: joblist_class: type of job
    return 0 if updated, non 0 for error
    """
    return job_selector(
        p_engine=p_engine,
        jobname=jobname,
        envname=envname,
        function_to_call='do_update',
        params=params,
        joblist_class=joblist_class)

def do_update(**kwargs):
    jobref = kwargs.get('jobref')
    joblist = kwargs.get('joblist')
    params = kwargs.get('params')

    jobobj = joblist.get_by_ref(jobref)
    update = False

    logger = logging.getLogger()

    if "rulesetname" in params and params['rulesetname'] != None:
        rulesetname = params['rulesetname']
        # as job is in particular environment
        # new ruleset need to be search in same environment
        # job metadata doesn't return environment id so it has to be
        # found by linking old ruleset via connector id to environment
        rulesetlist = DxRulesetList()
        #rulesetlist.LoadRulesets(None)
        connlist = DxConnectorsList()
        connlist.LoadConnectors(None)
        oldrulesetref = jobobj.ruleset_id
        logger.debug("old ruleset %s" % oldrulesetref)
        oldruleobj = rulesetlist.get_by_ref(oldrulesetref)
        oldconnobj = connlist.get_by_ref(oldruleobj.connectorId)
        rulesetlist.LoadRulesetsbyId(oldconnobj.environment_id)
        rulesetref = rulesetlist.get_rulesetId_by_name(rulesetname)
        logger.debug("new ruleset %s" % rulesetref)
        if rulesetref != oldrulesetref:
            update = True
            jobobj.ruleset_id = rulesetref


    if type(jobobj) == dxm.lib.DxJobs.DxJob.DxJob:

        for p in optional_params_list:
            if params[p] is not None:
                update = True
                if params[p] == 'Y':
                    value = True
                elif params[p] == 'N':
                    value = False
                else:
                    value = params[p]
                setattr(jobobj.obj, p, value)

        dmo = jobobj.database_masking_options

        for p in optional_options_list:
            if params[p] is not None:
                update = True
                if params[p] == 'Y':
                    value = True
                elif params[p] == 'N':
                    value = False
                else:
                    value = params[p]
                setattr(dmo, p, value)

        if params["prescript"]=='':
            dmo.prescript = None
        elif params["prescript"]:
            scriptname = os.path.basename(params["prescript"].name)
            prescript = DxMaskingScriptJob(name=scriptname, contents=''.join(params["prescript"].readlines()))
            dmo.prescript = prescript

        if params["postscript"]=='':
            dmo.postscript = None
        if params["postscript"]:
            scriptname = os.path.basename(params["postscript"].name)
            postscript = DxMaskingScriptJob(name=scriptname, contents = ''.join(params["postscript"].readlines()))
            dmo.postscript = postscript
    else:
        if "profilename" in params and params['rulesetname'] != None:
            profilename = params['profilename']

            oldprofile = jobobj.profile_set_id
            logger.debug("old profile %s" % oldprofile)
            profilelist = DxProfilesList()
            profileref = profilelist.get_profileSetId_by_name(profilename)
            logger.debug("new profile %s" % profileref)
            if profileref != oldprofile:
                update = True
                jobobj.profile_set_id = profileref

        for p in masking_params_list:
            if params[p] is not None:
                update = True
                if params[p] == 'Y':
                    value = True
                elif params[p] == 'N':
                    value = False
                else:
                    value = params[p]
                setattr(jobobj.obj, p, value)

    if update:
        return jobobj.update()
    else:
        print_message('Nothing to update')
        return 1


def do_copy(**kwargs):
    jobref = kwargs.get('jobref')
    joblist = kwargs.get('joblist')
    newjobname = kwargs.get('newjobname')
    engine_obj = kwargs.get('engine_obj')
    job_type = kwargs.get('joblist_class')
    if kwargs.get('joblist_class') == "DxJobsList":
        job = DxJob(engine_obj, None, None)
    else:
        job = DxProfileJob(engine_obj, None)

    jobobj = joblist.get_by_ref(jobref)

    job.load_obj(jobobj)
    job.job_name = newjobname
    return joblist.add(job)


def do_delete(**kwargs):
    jobref = kwargs.get('jobref')
    joblist = kwargs.get('joblist')
    return joblist.delete(jobref)

def do_cancel(**kwargs):
    jobref = kwargs.get('jobref')
    joblist = kwargs.get('joblist')
    jobobj = joblist.get_by_ref(jobref)
    return jobobj.cancel()

def job_cancel(p_engine, p_username,  jobname, envname):
    """
    Delete job from Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    return 0 if deleted, non 0 for error
    """
    return job_cancel_worker(p_engine, p_username,  jobname, envname, "DxJobsList")

def profilejob_cancel(p_engine, p_username,  jobname, envname):
    """
    Delete job from Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    return 0 if deleted, non 0 for error
    """
    return job_cancel_worker(p_engine, p_username,  jobname, envname, "DxProfileJobsList")

def job_cancel_worker(p_engine, p_username,  jobname, envname, joblist_class):
    """
    Delete job from Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: joblist_class: type of job
    return 0 if deleted, non 0 for error
    """
    return job_selector(
        p_engine=p_engine,
        jobname=jobname,
        envname=envname,
        function_to_call='do_cancel',
        joblist_class=joblist_class)

def job_delete(p_engine, p_username,  jobname, envname):
    """
    Delete job from Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    return 0 if deleted, non 0 for error
    """
    return job_delete_worker(p_engine, p_username,  jobname, envname, "DxJobsList")

def profilejob_delete(p_engine, p_username,  jobname, envname):
    """
    Delete job from Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    return 0 if deleted, non 0 for error
    """
    return job_delete_worker(p_engine, p_username,  jobname, envname, "DxProfileJobsList")

def job_delete_worker(p_engine, p_username,  jobname, envname, joblist_class):
    """
    Delete job from Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: joblist_class: type of job
    return 0 if deleted, non 0 for error
    """
    return job_selector(
        p_engine=p_engine,
        jobname=jobname,
        envname=envname,
        function_to_call='do_delete',
        joblist_class=joblist_class)

def job_selector(**kwargs):
    """
    Select unique job from Masking engine and run function on it
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: function_to_call: name of function to call on connector
    return 0 if added, non 0 for error
    """

    p_engine = kwargs.get('p_engine')
    jobname = kwargs.get('jobname')
    envname = kwargs.get('envname')
    function_to_call = kwargs.get('function_to_call')
    joblist_class = kwargs.get('joblist_class')
    lock = kwargs.get('lock')
    p_username = kwargs.get('p_username')
    ret = 0

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()

        joblist = globals()[joblist_class]()
        joblist.LoadJobs(envname)

        jobref = joblist.get_jobId_by_name(jobname)

        if jobref:
            dynfunc = globals()[function_to_call]
            ret = ret + dynfunc(
                jobref=jobref,
                engine_obj=engine_obj,
                joblist=joblist, **kwargs)

        else:
            if lock:
                lock.acquire()

            dxm.lib.DxJobs.DxJobCounter.ret = \
                dxm.lib.DxJobs.DxJobCounter.ret + 1

            if lock:
                lock.release()

            # for delete / update / copy global counter is not used
            ret = ret + 1
            continue

    return ret


def job_start(p_engine, p_username,  jobname, envname, tgt_connector,
              tgt_connector_env, nowait, parallel, monitor, ignore_warning):
    """
    Start job
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environment name
    param4: tgt_connector: target connector for multi tenant
    param5: tgt_connector_env: target connector environment for multi tenant
    param6: nowait: no wait for job to complete
    param7: parallel: number of concurrent masking jobs
    param8: monitor: enable progress bar
    return 0 if environment found
    """

    return job_start_worker(
                p_engine, p_username, jobname, envname, tgt_connector,
                tgt_connector_env, nowait, parallel, monitor,
                "DxJobsList", ignore_warning)

def profilejob_start(p_engine, p_username,  jobname, envname, nowait, parallel, monitor,
                     tgt_connector, tgt_connector_env):
    """
    Start profile job
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environment name
    param4: nowait: no wait for job to complete
    param5: parallel: number of concurrent masking jobs
    param6: monitor: enable progress bar
    param7: tgt_connector: target connector for multi tenant
    param8: tgt_connector_env: target connector environment for multi tenant
    return 0 if environment found
    """
    return job_start_worker(
                p_engine, p_username, jobname, envname, tgt_connector,
                tgt_connector_env, nowait, parallel, monitor,
                "DxProfileJobsList", None)


def job_start_worker(p_engine, p_username,  jobname, envname, tgt_connector,
                     tgt_connector_env, nowait, parallel, monitor,
                     joblist_class, ignore_warning):
    """
    Start job
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environment name
    param4: tgt_connector: target connector for multi tenant
    param5: tgt_connector_env: target connector environment for multi tenant
    param6: nowait: no wait for job to complete
    param7: parallel: number of concurrent masking jobs
    param8: monitor: enable progress bar
    param9: joblist_class - DxJobsList or DxProfileJobsList
    param10: ignore_warning - ignore warining for 22 and higher
    return 0 if environment found
    """


    job_list = [x for x in jobname]
    jobsno = len(job_list)

    posno = 1
    no_of_active_threads = 1

    logger = logging.getLogger()

    logger.debug("parallel % s active count %s"
                 % (parallel, active_count()))

    if monitor:
        no_of_active_threads = 2
        jobsbar = tqdm(
            total=jobsno,
            desc="No of started jobs",
            bar_format="{desc}: |{bar}| {n_fmt}/{total_fmt}")
        time.sleep(1)

    while len(job_list) > 0:

        ac = parallel - active_count() + no_of_active_threads

        logger.debug("parallel % s ac %s active count %s"
                     % (parallel, ac, active_count()))

        try:
            for i in range(1, ac+1):
                try:
                    single_jobname = job_list.pop()
                    logger.debug("starting job %s" % single_jobname)
                    t = Thread(
                        target=job_selector,
                        kwargs={'p_engine': p_engine,
                                'jobname': single_jobname,
                                'envname': envname,
                                'function_to_call': 'do_start',
                                'tgt_connector': tgt_connector,
                                'tgt_connector_env': tgt_connector_env,
                                'nowait': nowait, 'posno': posno,
                                'lock': lock, 'monitor': monitor,
                                'joblist_class': joblist_class,
                                'ignore_warning': ignore_warning})
                    t.start()
                    posno = posno + 1
                    logger.debug("before update")
                    time.sleep(1)
                    if monitor:
                        jobsbar.update(1)
                        logger.debug("after update ")

                except IndexError:
                    pass
        except Exception:
            print_error("Error: unable to start thread")

        # wait 1 sec before kicking off next job
        time.sleep(1)

    # Wait for all threads to complete
    while (active_count() > no_of_active_threads):
        logger.debug("waiting for threads - active count %s"
                     % active_count())
        time.sleep(1)

    logger.debug("all threds finished %s" % active_count())

    if monitor:
        jobsbar.close()

    logger.debug("After close")
    print_message("\n" * posno)

    if joblist_class == "DxJobsList":
        return dxm.lib.DxJobs.DxJobCounter.ret
    else:
        return dxm.lib.DxJobs.DxJobCounter.profileret


def do_start(**kwargs):
    """
    Start job
    """
    jobref = kwargs.get('jobref')
    joblist = kwargs.get('joblist')
    tgt_connector = kwargs.get('tgt_connector')
    tgt_connector_env = kwargs.get('tgt_connector_env')
    nowait = kwargs.get('nowait')
    posno = kwargs.get('posno')
    lock = kwargs.get('lock')
    monitor = kwargs.get('monitor')
    joblist_class = kwargs.get('joblist_class')
    ignore_warning = kwargs.get('ignore_warning')
    jobobj = joblist.get_by_ref(jobref)

    targetconnector = None

    if jobobj.multi_tenant:
        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        

        if tgt_connector is None:
            print_error("Target connector is required for multitenant job")
            lock.acquire()
            if joblist_class == "DxJobsList":
                dxm.lib.DxJobs.DxJobCounter.ret = \
                    dxm.lib.DxJobs.DxJobCounter.ret + 1
            else:
                dxm.lib.DxJobs.DxJobCounter.profileret = \
                    dxm.lib.DxJobs.DxJobCounter.profileret + 1
            lock.release()
            return 1

        connectorlist = DxConnectorsList(tgt_connector_env)
        #connectorlist.LoadConnectors()
        targetconnector = connectorlist.get_connectorId_by_name(
                            tgt_connector)
        if targetconnector:
            targetconnector = targetconnector[1:]
        else:
            print_error("Target connector for multitenant job not found")
            lock.acquire()
            if joblist_class == "DxJobsList":
                dxm.lib.DxJobs.DxJobCounter.ret = \
                    dxm.lib.DxJobs.DxJobCounter.ret + 1
            else:
                dxm.lib.DxJobs.DxJobCounter.profileret = \
                    dxm.lib.DxJobs.DxJobCounter.profileret + 1
            lock.release()
            return 1

    #staring job
    jobobj.monitor = monitor
    return jobobj.start(targetconnector, None, nowait, posno, lock, ignore_warning)



def jobs_list(p_engine, p_username,  jobname, envname, p_format):
    """
    Print list of masking jobs
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environemnt name to list jobs from
    param4: p_format: output format
    return 0 if environment found
    """
    return jobs_list_worker(p_engine, p_username,  jobname, envname, p_format, "DxJobsList")

def jobs_report(p_engine, p_username,  jobname, envname, p_format, last, startdate, enddate, details, error_details):
    """
    Print report of masking jobs
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environemnt name to list jobs from
    param4: p_format: output format
    return 0 if environment found
    """

    if details and error_details:
        print_error("--details and --error_details flags are mutally excluded")
        return 1
    
    worker_details = None

    if details:
        worker_details = 'jobdetails'

    if error_details:
        worker_details = 'errordetails'

    return jobs_report_worker(p_engine, p_username,  jobname, envname, p_format, last, startdate, enddate, worker_details)


def profilejobs_report(p_engine, p_username,  jobname, envname, p_format, last, startdate, enddate, details):
    """
    Print report of masking jobs
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environemnt name to list jobs from
    param4: p_format: output format
    return 0 if environment found
    """

    if details == True:
        print_error("Details option not supported for profile jobs")
        return -1

    return jobs_report_worker(p_engine, p_username,  jobname, envname, p_format, last, startdate, enddate, None, 'profile')

def profilejobs_list(p_engine, p_username,  jobname, envname, p_format):
    """
    Print list of profile jobs
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environemnt name to list jobs from
    param4: p_format: output format
    return 0 if environment found
    """
    return jobs_list_worker(p_engine, p_username,  jobname, envname, p_format, "DxProfileJobsList")

def jobs_list_worker(p_engine, p_username,  jobname, envname, p_format, joblist_class):
    """
    Print list of jobs
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environemnt name to list jobs from
    param4: p_format: output format
    param5: joblist_class - DxJobsList, DxProfileJobslist
    return 0 if environment found
    """

    ret = 0

    logger = logging.getLogger()

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Job name", 30),
                    ("Ruleset name", 30),
                    ("Connector name", 30),
                    ("Environment name", 30),
                    ("Completed", 20),
                    ("Status", 20),
                    ("Runtime", 20)
                  ]
    data.create_header(data_header)
    data.format_type = p_format

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        # load all objects
        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulesetlist = DxRulesetList(envname)
        connectorlist = DxConnectorsList(envname)
        joblist = globals()[joblist_class]()

        logger.debug("Envname is %s, job name is %s" % (envname, jobname))

        joblist.LoadJobs(envname)
        #rulesetlist.LoadRulesets(envname)
        #connectorlist.LoadConnectors(envname)

        if jobname is None:
            jobs = joblist.get_allref()
        else:
            jobs = joblist.get_all_jobId_by_name(jobname)
            if jobs is None:
                ret = ret + 1
                continue

        for jobref in jobs:
            jobobj = joblist.get_by_ref(jobref)

            rulesetobj = rulesetlist.get_by_ref(jobobj.ruleset_id)
            # those test are requierd for 5.X engies where API is not showing all types of connectors
            if rulesetobj is not None:
                rulename = rulesetobj.ruleset_name
                connectorobj = connectorlist.get_by_ref(rulesetobj.connectorId)
                if connectorobj is not None:
                    connectorname = connectorobj.connector_name
                    envobj = envlist.get_by_ref(connectorobj.environment_id)
                    if envobj is not None:
                        envobjname = envobj.environment_name
                    else:
                         envobjname = "N/A"   
                else:
                    connectorname = "N/A"
                    envobjname = "N/A"
            else:
                rulename = "N/A"
                connectorname = "N/A"
                envobjname = "N/A"

            if jobobj.lastExec is not None:
                status = jobobj.lastExec.status
                if (jobobj.lastExec.end_time is not None) and \
                   (jobobj.lastExec.end_time is not None):
                    endtime = jobobj.lastExec.end_time \
                        .strftime("%Y-%m-%d %H:%M:%S")
                    runtimetemp = jobobj.lastExec.end_time \
                        - jobobj.lastExec.start_time
                    runtime = str(runtimetemp)
                else:
                    endtime = 'N/A'
                    runtime = 'N/A'
            else:
                status = 'N/A'
                endtime = 'N/A'
                runtime = 'N/A'

            data.data_insert(
                              engine_tuple[0],
                              jobobj.job_name,
                              rulename,
                              connectorname,
                              envobjname,
                              endtime,
                              status,
                              runtime
                            )
    
    print("")
    print (data.data_output(False))
    print("")
    return ret

def jobs_report_worker(p_engine, p_username,  jobname, envname, p_format, last, startdate, enddate, details, jobtype='masking'):
    """
    Print report of jobs
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environemnt name to list jobs from
    param4: p_format: output format
    param5: last: display last job only
    param6: startdate: filter by start date
    param7: enddate: filter by end date
    param8: details
    param9: joblist_class - DxJobsList, DxProfileJobslist
    return 0 if environment found
    """

    ret = 0

    logger = logging.getLogger()

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    data = DataFormatter()


    data.format_type = p_format

    if jobtype == 'masking':
        joblist = DxJobsList()
    else:
        joblist = DxProfileJobsList()


    data_header = joblist.set_report_headers(details=details)
    data.create_header(data_header)

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        # load all objects
        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulesetlist = DxRulesetList(envname)
        connectorlist = DxConnectorsList(envname)

        logger.debug("Envname is %s, job name is %s" % (envname, jobname))

        joblist.LoadJobs(envname)
        #rulesetlist.LoadRulesets(envname)
        #connectorlist.LoadConnectors(envname)

        if jobname is None:
            jobs = joblist.get_allref()
        else:
            jobs = joblist.get_all_jobId_by_name(jobname)
            if jobs is None:
                ret = ret + 1
                continue

        for jobref in jobs:
            jobobj = joblist.get_by_ref(jobref)

            if last:
                lastonly = True
            else:
                lastonly = False


            if lastonly:
                execlist = [ jobobj.lastExec ]
            else:
                if startdate or enddate:
                    execlist = jobobj.filter_executions(startdate, enddate)
                else:
                    execlist = jobobj.execList


            if execlist:
                for jobexec in execlist:
                    joblist.set_report_output(data, engine_tuple[0], jobobj, jobexec, details)

            else:
                # no executions
                ret = 1

        print("")
        print (data.data_output(False))
        print("")
        return ret