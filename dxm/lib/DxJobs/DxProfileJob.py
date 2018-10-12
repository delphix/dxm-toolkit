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
        self.__logger.debug("creating DxDxProfileJobJob object")
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
            exec_api = ExecutionApi(self.__engine.api_client)
            self.__logger.debug("Stopping execution %s" % str(self.__lastExec))
            res = exec_api.cancel_execution(self.__lastExec.execution_id)
            print res

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
        execjob.job_id = self.masking_job_id

        if (self.multi_tenant):
            # target is mandatory
            if target_connector_id:
                execjob.target_connector_id = target_connector_id
            else:
                print_error("Target connector is required for multitenant job")
                return 1

        if (self.on_the_fly_masking):
            if not self.on_the_fly_masking_source:
                if source_connector_id:
                    execjob.source_connector_id = source_connector_id
                else:
                    print_error(
                        "Source connector is required for on the fly job")
                    return 1

        try:
            self.__logger.debug("start job input %s" % str(execjob))
            response = exec_api.create_execution(
                execjob,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("start job response %s"
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
        first = True
        bar = None

        exec_api = ExecutionApi(self.__engine.api_client)
        last = 0

        self.__logger.debug('Waiting for job %s to start processing rows'
                            % self.job_name)

        if not self.monitor:
            print_message('Waiting for job %s to start processing rows'
                          % self.job_name)

        while execjob.status == 'RUNNING':
            time.sleep(10)
            execjob = exec_api.get_execution_by_id(execid)
            if first and (execjob.rows_total is not None):
                first = False
                if self.monitor and (bar is None):
                    bar = tqdm(
                        total=execjob.rows_total,
                        desc=self.job_name,
                        position=posno,
                        bar_format="{desc}: {percentage:3.0f}%|{bar}|"
                                   " {n_fmt}/{total_fmt}")
                else:
                    print_message('Job %s is processing rows'
                                  % self.job_name)

            if execjob.rows_masked is not None:
                if self.monitor and (bar is not None):
                    self.__logger.debug(execjob.rows_masked)
                    self.__logger.debug(last)
                    step = execjob.rows_masked-last
                    # if step == 0:
                    #     step = 1
                    self.__logger.debug(step)
                    bar.update(step)
                    last = execjob.rows_masked

        if execjob.status == 'SUCCEEDED':
            if not self.monitor:
                print_message('Masking job %s finished.' % self.job_name)
                print_message('%s rows masked' % (execjob.rows_masked or 0))
            else:
                if bar:
                    bar.close()
                self.__logger.debug('Masking job %s finished' % self.job_name)
                self.__logger.debug('%s rows masked' % execjob.rows_masked)
            return 0
        else:
            if not self.monitor:
                print_error('Problem with masking job %s' % self.job_name)
                print_error('%s rows masked' % (execjob.rows_masked or 0))
            else:
                if bar:
                    bar.close()
                self.__logger.error('Problem with masking job %s'
                                    % self.job_name)
                self.__logger.error('%s rows masked' % execjob.rows_masked)

            lock.acquire()
            dxm.lib.DxJobs.DxJobCounter.ret = \
                dxm.lib.DxJobs.DxJobCounter.ret + 1
            lock.release()
            self.__logger.error('return value %s'
                                % dxm.lib.DxJobs.DxJobCounter.ret)
            return 1
