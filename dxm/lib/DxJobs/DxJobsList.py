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


import logging
import sys
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxJobs.DxJob import DxJob
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxLogging import print_error
from dxm.lib.DxTools.DxTools import paginator


class DxJobsList(object):

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
        self.__logger.debug("creating DxJobsList object")

    @classmethod
    def LoadJobs(self, environment_name=None):
        """
        Load list of rule sets
        Return None if OK
        """

        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.api.masking_job_api import MaskingJobApi
            from masking_api_60.api.execution_api import ExecutionApi
            from masking_api_60.rest import ApiException
        else:
            from masking_api_53.api.masking_job_api import MaskingJobApi
            from masking_api_53.api.execution_api import ExecutionApi
            from masking_api_53.rest import ApiException

        self.__api = MaskingJobApi
        self.__apiexec = ExecutionApi
        self.__apiexc = ApiException

        try:

            api_instance = self.__api(self.__engine.api_client)

            execapi = self.__apiexec(self.__engine.api_client)
            execList = paginator(
                        execapi,
                        "get_all_executions")

            if execList.response_list:
                for e in execList.response_list:
                    self.__executionList[e.job_id] = e

            if environment_name:
                environment_id = DxEnvironmentList.get_environmentId_by_name(
                                 environment_name)

                if environment_id:
                    jobs = paginator(
                            api_instance,
                            "get_all_masking_jobs",
                            environment_id=environment_id,
                            _request_timeout=self.__engine.get_timeout())
                else:
                    return 1
            else:

                jobs = paginator(
                    api_instance,
                    "get_all_masking_jobs",
                    _request_timeout=self.__engine.get_timeout())

            if jobs.response_list:
                for c in jobs.response_list:
                    if c.masking_job_id in self.__executionList:
                        lastExec = self.__executionList[c.masking_job_id]
                    else:
                        lastExec = None

                    job = DxJob(self.__engine, lastExec)
                    job.from_job(c)
                    self.__jobsList[c.masking_job_id] = job
            else:
                if environment_name is None:
                    print_error("No jobs found")
                    self.__logger.error("No jobs found")

            self.__logger.debug("All jobs loaded")

        except self.__apiexc as e:
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
            #sys.exit(1)

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
        :param ruleset: Ruleset object to add to Engine and list
        return None if OK
        """

        if (job.add() is None):
            self.__logger.debug("Adding job %s to list" % job)
            self.__jobsList[job.masking_job_id] = job
            return None
        else:
            return 1

    @classmethod
    def delete(self, masking_job_id):
        """
        Delete a job from a list and Engine
        :param masking_job_id: masking job id to delete from Engine and list
        return None if OK
        """

        job = self.get_by_ref(masking_job_id)
        if job is not None:
            if job.delete() is None:
                return None
            else:
                return 1
        else:
            print_error("Job with id %s not found" % masking_job_id)
            return 1
