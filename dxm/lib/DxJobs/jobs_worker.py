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
# Copyright (c) 2018 by Delphix. All rights reserved.
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
from masking_apis.models.database_masking_options import DatabaseMaskingOptions
from masking_apis.models.masking_job_script import MaskingJobScript

from threading import Thread
from threading import active_count
import time
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

def profilejob_add(p_engine, params):
    """
    Add profile job to Masking engine
    param1: p_engine: engine name from configuration
    param2: params: job parameters
    return 0 if added, non 0 for error
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    logger = logging.getLogger()

    envname = params['envname']
    jobname = params['jobname']
    rulesetname = params['rulesetname']
    profilename = params['profilename']

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])

        if engine_obj.get_session():
            continue

        joblist = DxProfileJobsList()
        envlist = DxEnvironmentList()
        rulesetlist = DxRulesetList()
        profilesetlist = DxProfilesList()
        profileref = profilesetlist.get_profileSetId_by_name(profilename)
        envlist.LoadEnvironments()
        logger.debug("Envname is %s, job name is %s" % (envname, jobname))
        rulesetlist.LoadRulesets(envname)
        rulesetref = rulesetlist.get_rulesetId_by_name(rulesetname)


        job = DxProfileJob(engine_obj, None)
        job.ruleset_id = rulesetref
        job.job_name = jobname
        job.profile_set_id = profileref

        for p in masking_params_list:
            if params[p] is not None:
                if params[p] == 'Y':
                    value = True
                elif params[p] == 'N':
                    value = False
                else:
                    value = params[p]
                setattr(job, p, value)

        if joblist.add(job):
            ret = ret + 1

    return ret

def job_add(p_engine, params):
    """
    Add masking job to Masking engine
    param1: p_engine: engine name from configuration
    param2: params: job parameters
    return 0 if added, non 0 for error
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    logger = logging.getLogger()

    envname = params['envname']
    jobname = params['jobname']
    rulesetname = params['rulesetname']

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])

        if engine_obj.get_session():
            continue

        joblist = DxJobsList()
        envlist = DxEnvironmentList()
        rulesetlist = DxRulesetList()
        envlist.LoadEnvironments()
        logger.debug("Envname is %s, job name is %s" % (envname, jobname))
        rulesetlist.LoadRulesets(envname)

        rulesetref = rulesetlist.get_rulesetId_by_name(rulesetname)

        job = DxJob(engine_obj, None)
        job.ruleset_id = rulesetref
        job.job_name = jobname

        for p in optional_params_list:
            if params[p] is not None:
                if params[p] == 'Y':
                    value = True
                elif params[p] == 'N':
                    value = False
                else:
                    value = params[p]
                setattr(job, p, value)

        dmo = DatabaseMaskingOptions()

        for p in optional_options_list:
            if params[p] is not None:
                if params[p] == 'Y':
                    value = True
                elif params[p] == 'N':
                    value = False
                else:
                    value = params[p]
                setattr(job, p, value)

        if params["prescript"]:
            prescript = MaskingJobScript()
            prescript.contents = ''.join(params["prescript"].readlines())
            prescript.name = params["prescript"].name
            dmo.prescript = prescript

        if params["postscript"]:
            postscript = MaskingJobScript()
            postscript.contents = ''.join(params["postscript"].readlines())
            postscript.name = params["postscript"].name
            dmo.postscript = postscript

        job.database_masking_options = dmo

        if joblist.add(job):
            ret = ret + 1

    return ret

def job_copy(p_engine, jobname, envname, newjobname):
    """
    Copy masking job in Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: newjobname: new job name
    return 0 if deleted, non 0 for error
    """
    return job_copy_worker(p_engine, jobname, envname, newjobname, "DxJobsList")

def profilejob_copy(p_engine, jobname, envname, newjobname):
    """
    Copy profile job in Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: newjobname: new job name
    return 0 if deleted, non 0 for error
    """
    return job_copy_worker(p_engine, jobname, envname, newjobname, "DxProfileJobsList")

def job_copy_worker(p_engine, jobname, envname, newjobname, joblist_class):
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

def job_update(p_engine, jobname, envname, params):
    """
    Update a job in Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: params: dict with job parameters
    return 0 if updated, non 0 for error
    """
    return job_update_worker(p_engine, jobname, envname, params, "DxJobsList")

def profilejob_update(p_engine, jobname, envname, params):
    """
    Update a job in Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    param4: params: dict with job parameters
    return 0 if updated, non 0 for error
    """
    return job_update_worker(p_engine, jobname, envname, params, "DxProfileJobsList")

def job_update_worker(p_engine, jobname, envname, params, joblist_class):
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

    if "rulesetname" in params:
        rulesetname = params['rulesetname']
        # as job is in particular environment
        # new ruleset need to be search in same environment
        # job metadata doesn't return environment id so it has to be
        # found by linking old ruleset via connector id to environment
        rulesetlist = DxRulesetList()
        rulesetlist.LoadRulesets(None)
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
                setattr(jobobj, p, value)

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
    else:

        if "profilename" in params:
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
                setattr(jobobj, p, value)

    if update:
        return jobobj.update()
    else:
        print_message('Nothing to update')
        return 1


def do_copy(**kwargs):
    jobref = kwargs.get('jobref')
    joblist = kwargs.get('joblist')
    newjobname = kwargs.get('newjobname')
    jobobj = joblist.get_by_ref(jobref)
    jobobj.job_name = newjobname
    return joblist.add(jobobj)


def do_delete(**kwargs):
    jobref = kwargs.get('jobref')
    joblist = kwargs.get('joblist')
    return joblist.delete(jobref)

def do_cancel(**kwargs):
    jobref = kwargs.get('jobref')
    joblist = kwargs.get('joblist')
    jobobj = joblist.get_by_ref(jobref)
    return jobobj.cancel()

def job_cancel(p_engine, jobname, envname):
    """
    Delete job from Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    return 0 if deleted, non 0 for error
    """
    return job_cancel_worker(p_engine, jobname, envname, "DxJobsList")

def profilejob_cancel(p_engine, jobname, envname):
    """
    Delete job from Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    return 0 if deleted, non 0 for error
    """
    return job_cancel_worker(p_engine, jobname, envname, "DxProfileJobsList")

def job_cancel_worker(p_engine, jobname, envname, joblist_class):
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

def job_delete(p_engine, jobname, envname):
    """
    Delete job from Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    return 0 if deleted, non 0 for error
    """
    return job_delete_worker(p_engine, jobname, envname, "DxJobsList")

def profilejob_delete(p_engine, jobname, envname):
    """
    Delete job from Masking engine
    param1: p_engine: engine name from configuration
    param2: jobname: job name
    param3: envname: environment name
    return 0 if deleted, non 0 for error
    """
    return job_delete_worker(p_engine, jobname, envname, "DxProfileJobsList")

def job_delete_worker(p_engine, jobname, envname, joblist_class):
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

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])
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
            ret = ret + 1
            continue

    return ret


def job_start(p_engine, jobname, envname, tgt_connector,
              tgt_connector_env, nowait, parallel, monitor):
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
                p_engine, jobname, envname, tgt_connector,
                tgt_connector_env, nowait, parallel, monitor,
                "DxJobsList")

def profilejob_start(p_engine, jobname, envname, nowait, parallel, monitor):
    """
    Start profile job
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environment name
    param6: nowait: no wait for job to complete
    param7: parallel: number of concurrent masking jobs
    param8: monitor: enable progress bar
    return 0 if environment found
    """
    return job_start_worker(
                p_engine, jobname, envname, None,
                None, nowait, parallel, monitor,
                "DxProfileJobsList")


def job_start_worker(p_engine, jobname, envname, tgt_connector,
                     tgt_connector_env, nowait, parallel, monitor,
                     joblist_class):
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
                                'joblist_class': joblist_class})
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
            print "Error: unable to start thread"

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
    print "\n" * posno

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

    jobobj = joblist.get_by_ref(jobref)

    targetconnector = None

    if jobobj.multi_tenant:
        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        connectorlist = DxConnectorsList()
        connectorlist.LoadConnectors(tgt_connector_env)
        targetconnector = DxConnectorsList.get_connectorId_by_name(tgt_connector)

    #staring job
    jobobj.monitor = monitor
    return jobobj.start(targetconnector, None, nowait, posno, lock)



def jobs_list(p_engine, jobname, envname, p_format):
    """
    Print list of masking jobs
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environemnt name to list jobs from
    param4: p_format: output format
    return 0 if environment found
    """
    return jobs_list_worker(p_engine, jobname, envname, p_format, "DxJobsList")

def profilejobs_list(p_engine, jobname, envname, p_format):
    """
    Print list of profile jobs
    param1: p_engine: engine name from configuration
    param2: jobname: job name to list
    param3: envname: environemnt name to list jobs from
    param4: p_format: output format
    return 0 if environment found
    """
    return jobs_list_worker(p_engine, jobname, envname, p_format, "DxProfileJobsList")

def jobs_list_worker(p_engine, jobname, envname, p_format, joblist_class):
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

    enginelist = get_list_of_engines(p_engine)

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
        engine_obj = DxMaskingEngine(engine_tuple[0], engine_tuple[1],
                                     engine_tuple[2], engine_tuple[3])
        if engine_obj.get_session():
            continue

        # load all objects
        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulesetlist = DxRulesetList()
        connectorlist = DxConnectorsList()
        joblist = globals()[joblist_class]()

        logger.debug("Envname is %s, job name is %s" % (envname, jobname))

        joblist.LoadJobs(envname)
        rulesetlist.LoadRulesets(envname)
        connectorlist.LoadConnectors(envname)

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
            connectorobj = connectorlist.get_by_ref(rulesetobj.connectorId)
            envobj = envlist.get_by_ref(connectorobj.environment_id)

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
                              rulesetobj.ruleset_name,
                              connectorobj.connector_name,
                              envobj.environment_name,
                              endtime,
                              status,
                              runtime
                            )
        print("")
        print (data.data_output(False))
        print("")
        return ret
