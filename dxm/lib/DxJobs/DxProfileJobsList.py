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
# Date    : September 2018


import logging
import sys
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxJobs.DxProfileJob import DxProfileJob
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxLogging import print_error
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.masking_api.api.profile_job_api import ProfileJobApi
from dxm.lib.masking_api.api.execution_api import ExecutionApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.DxRuleset.DxRulesetList import DxRulesetList
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList

class DxProfileJobsList(object):

    __engine = None
    __jobsList = {}
    __executionList = {}
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__engine = DxMaskingEngine
        self.__jobsList = {}
        self.__executionList = {}
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxProfileJobsList object")


    @classmethod
    def LoadJobs(self, environment_name=None):
        """
        Load list of rule sets
        Return None if OK
        """

        self.__api = ProfileJobApi
        self.__apiexec = ExecutionApi
        self.__apiexc = ApiException

        try:

            api_instance = self.__api(self.__engine.api_client)
            execapi = self.__apiexec(self.__engine.api_client)
            execList = paginator(
                        execapi,
                        "get_all_executions")

            # if execList.response_list:
            #     for e in execList.response_list:
            #         self.__executionList[e.job_id] = e


            if execList.response_list:
                for e in execList.response_list:
                    if e.job_id in self.__executionList:
                        self.__executionList[e.job_id].append(e)
                    else:
                        self.__executionList[e.job_id] = [e]

            if environment_name:
                environment_id = DxEnvironmentList.get_environmentId_by_name(
                                 environment_name)

                if environment_id:
                    jobs = paginator(
                            api_instance,
                            "get_all_profile_jobs",
                            environment_id=environment_id,
                            _request_timeout=self.__engine.get_timeout())
                else:
                    return 1
            else:

                jobs = paginator(
                    api_instance,
                    "get_all_profile_jobs",
                    _request_timeout=self.__engine.get_timeout())

            if jobs.response_list:
                for c in jobs.response_list:
                    if c.profile_job_id in self.__executionList:
                        execution_list = self.__executionList[c.profile_job_id]
                    else:
                        execution_list = None

                    job = DxProfileJob(self.__engine, execution_list)
                    job.load_obj(c)
                    self.__jobsList[c.profile_job_id] = job
            else:
                if environment_name is None:
                    print_error("No jobs found")
                    self.__logger.error("No jobs found")

            self.__logger.debug("All jobs loaded")

        except ApiException as e:
            print_error("Can't load job list %s" % e.body)
            return 1

    @classmethod
    def get_by_ref(self, reference):
        """
        return a job object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__jobsList[reference]

        except KeyError as e:
            self.__logger.debug("can't find job object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__jobsList.keys()

    @classmethod
    def get_jobId_by_name(self, name):
        """
        Return job id by name.
        :param1 name: name of job
        return ref if OK
        return None if ruleset not found or not unique
        """
        reflist = self.get_jobId_by_name_worker(name)
        # convert list to single value
        # as there will be only one element in list
        if reflist:
            return reflist[0]
        else:
            return None

    @classmethod
    def get_all_jobId_by_name(self, name):
        """
        Return ruleset id by name.
        :param1 name: name of job
        return list of references if OK
        return None if ruleset not found
        """
        return self.get_jobId_by_name_worker(name, None)

    @classmethod
    def get_jobId_by_name_worker(self, name, check_uniqueness=1):
        """
        :param1 name: name of job
        :param2 check_uniqueness: check uniqueness put None if skip this check
        return list of rulesets
        """
        reflist = get_objref_by_val_and_attribute(name, self, 'job_name')
        if len(reflist) == 0:
            self.__logger.error('Job %s not found' % name)
            print_error('Job %s not found' % name)
            return None

        if check_uniqueness:
            if len(reflist) > 1:
                self.__logger.error('Job name %s is not unique' % name)
                print_error('Job name %s is not unique' % name)
                return None

        return reflist


    @classmethod
    def add(self, job):
        """
        Add an Job to a list and Engine
        :param job: job object to add to Engine and list
        return None if OK
        """

        if (job.add() == 0):
            self.__logger.debug("Adding job %s to list" % job)
            self.__jobsList[job.profile_job_id] = job
            return 0
        else:
            return 1

    @classmethod
    def delete(self, profile_job_id):
        """
        Delete a job from a list and Engine
        :param profile_job_id: profile job id to delete from Engine and list
        return None if OK
        """

        job = self.get_by_ref(profile_job_id)
        if job is not None:
            return job.delete()
        else:
            print_error("Job with id %s not found" % profile_job_id)
            return 1


    @classmethod
    def set_report_headers(self, details):
        data_header = [
                ("Engine name", 30),
                ("Environment name", 30),
                ("Job name", 30),  
                ("Ruleset Type", 12),
                ("ExecId", 6),                 
                ("Started", 20),                                                              
                ("Completed", 20),
                ("Status", 20),
                ("Runtime", 20)                  
                ]
        return data_header
    

    @classmethod
    def set_report_output(self, output, engine_name, jobobj, jobexec, details):

        rulesetlist = DxRulesetList
        connectorlist = DxConnectorsList
        envlist = DxEnvironmentList

        rulesetobj = rulesetlist.get_by_ref(jobobj.ruleset_id)
        # those test are requierd for 5.X engies where API is not showing all types of connectors
        if rulesetobj is not None:
            ruleset_type = rulesetobj.type
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
            ruleset_type = "N/A"

        if jobexec is not None:
            status = jobexec.status
            execid = jobexec.execution_id
            if jobexec.start_time is not None:
                starttime = jobexec.start_time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                starttime = 'N/A'
            if (jobexec.end_time is not None) and \
            (jobexec.start_time is not None):
                endtime = jobexec.end_time \
                    .strftime("%Y-%m-%d %H:%M:%S")
                runtimetemp = jobexec.end_time \
                    - jobexec.start_time
                runtime = str(runtimetemp)
            else:
                endtime = 'N/A'
                runtime = 'N/A'
        else:
            status = 'N/A'
            endtime = 'N/A'
            starttime = 'N/A'
            runtime = 'N/A'
            execid = 'N/A'


        output.data_insert(
                        engine_name,
                        envobjname,
                        jobobj.job_name,
                        ruleset_type,
                        execid,
                        starttime,
                        endtime,
                        status,
                        runtime
                        )