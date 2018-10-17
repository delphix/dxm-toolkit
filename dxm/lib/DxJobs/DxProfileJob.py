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
import time
from tqdm import tqdm
from masking_apis.models.profile_job import ProfileJob
from masking_apis.apis.profile_job_api import ProfileJobApi
from masking_apis.apis.execution_api import ExecutionApi
from masking_apis.models.execution import Execution
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
import dxm.lib.DxJobs.DxJobCounter


class DxProfileJob(ProfileJob):

    def __init__(self, engine, lastExec):
        """
        Constructor
        :param1 engine: DxMaskingEngine object
        :param2 execList: list of job executions
        """
        ProfileJob.__init__(self)
        self.__engine = engine
        self.__lastExec = lastExec
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxProfileJob object")
        self.__monitor = False

    @property
    def monitor(self):
        return self.__monitor

    @monitor.setter
    def monitor(self, value):
        self.__monitor = value

    @property
    def lastExec(self):
        return self.__lastExec

    def from_job(self, job):
        """
        Copy properties from ProfileJob object into DxProfileJob
        :param con: ProfileJob object
        """
        self.__dict__.update(job.__dict__)

    def add(self):
        """
        Add profile job to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.job_name is None):
            print_error("Job name is required")
            self.__logger.error("Profile job name is required")
            return 1

        if (self.ruleset_id is None):
            print_error("ruleset_id is required")
            self.__logger.error("ruleset_id is required")
            return 1

        try:
            self.__logger.debug("create profile job input %s" % str(self))
            api_instance = ProfileJobApi(self.__engine.api_client)
            response = api_instance.create_profile_job(
                        self, _request_timeout=self.__engine.get_timeout())
            self.from_job(response)

            self.__logger.debug("profile job response %s"
                                % str(response))

            print_message("Profile job %s added" % self.job_name)
            return None
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete profile job from Engine
        return a 0 if non error
        return 1 in case of error
        """

        try:
            api_instance = ProfileJobApi(self.__engine.api_client)
            response = api_instance.delete_profile_job(
                self.profile_job_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("job response %s"
                                % str(response))
            print_message("Profile job %s deleted" % self.job_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def update(self):
        """
        Update profile job in Engine
        return a 0 if non error
        return 1 in case of error
        """

        try:
            api_instance = ProfileJobApi(self.__engine.api_client)
            self.__logger.debug("update profile job request %s"
                                % str(self))
            response = api_instance.update_profile_job(
                self.profile_job_id,
                self,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("Profile job response %s"
                                % str(response))
            print_message("Profile job %s updated" % self.job_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def cancel(self):
        """
        Cancel running profile job in Engine
        return a 0 if non error
        return 1 in case of error
        """

        try:
            execid = self.__lastExec.execution_id
            exec_api = ExecutionApi(self.__engine.api_client)
            self.__logger.debug("Stopping execution %s" % str(self.__lastExec))
            execjob = exec_api.cancel_execution(self.__lastExec.execution_id)
            while execjob.status == 'RUNNING':
                time.sleep(1)
                execjob = exec_api.get_execution_by_id(execid)

            print execjob
            return 0

        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1



    def start(self, target_connector_id, source_connector_id, nowait, posno,
              lock):
        """
        Start masking job
        :param1 target_connector_id: target connector id for multinentant
        :param2 source_connector_id: source connector for on the fly job
        :param3 wait_for_finish: wait for job to finish
        Return 0 if job started and finished OK, or was in nowait
        Return 1 if errors
        """
        exec_api = ExecutionApi(self.__engine.api_client)

        execjob = Execution()
        execjob.job_id = self.profile_job_id

        try:
            self.__logger.debug("start profilejob input %s" % str(execjob))
            response = exec_api.create_execution(
                execjob,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("start profilejob response %s"
                                % str(response))

            if nowait:
                return 0
            else:
                return self.wait_for_job(response, posno, lock)

        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            lock.acquire()
            dxm.lib.DxJobs.DxJobCounter.ret = \
                dxm.lib.DxJobs.DxJobCounter.ret + 1
            lock.release()
            self.__logger.error('return value %s'
                                % dxm.lib.DxJobs.DxJobCounter.ret)
            return 1

    def wait_for_job(self, execjob, posno, lock):
        """
        Wait for job to finish execution
        :param1 execjob: Execution job response
        Return 0 finished OK
        Return 1 if errors
        """

        execid = execjob.execution_id

        exec_api = ExecutionApi(self.__engine.api_client)

        self.__logger.debug('Waiting for profilejob %s to finish'
                            % self.job_name)

        if not self.monitor:
            print_message('Waiting for profilejob %s to finish'
                          % self.job_name)

        while execjob.status == 'RUNNING':
            time.sleep(10)
            execjob = exec_api.get_execution_by_id(execid)

        if execjob.status == 'SUCCEEDED':
            if not self.monitor:
                print_message('Profile job %s finished.' % self.job_name)
            else:
                self.__logger.debug('Profile job %s finished' % self.job_name)
                self.__logger.debug('%s rows masked' % execjob.rows_masked)
            return 0
        else:
            if not self.monitor:
                print_error('Problem with profile job %s' % self.job_name)
            else:
                self.__logger.error('Problem with profile job %s'
                                    % self.job_name)
            lock.acquire()
            dxm.lib.DxJobs.DxJobCounter.profileret = \
                dxm.lib.DxJobs.DxJobCounter.profileret + 1
            lock.release()
            self.__logger.error('return value %s'
                                % dxm.lib.DxJobs.DxJobCounter.profileret)
            return 1
