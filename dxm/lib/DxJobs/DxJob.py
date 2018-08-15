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
import time
import click
from masking_apis.models.masking_job import MaskingJob
from masking_apis.apis.masking_job_api import MaskingJobApi
from masking_apis.apis.execution_api import ExecutionApi
from masking_apis.models.execution import Execution
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
import dxm.lib.DxJobs.DxJobCounter


class DxJob(MaskingJob):

    def __init__(self, engine, lastExec):
        """
        Constructor
        :param1 engine: DxMaskingEngine object
        :param2 execList: list of job executions
        """
        MaskingJob.__init__(self)
        self.__engine = engine
        self.__lastExec = lastExec
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxJob object")

    @property
    def lastExec(self):
        return self.__lastExec

    def from_job(self, job):
        """
        Copy properties from MaskingJob object into DxJob
        :param con: MaskingJob object
        """
        self.__dict__.update(job.__dict__)

    def add(self):
        """
        Add job to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.job_name is None):
            print_error("Job name is required")
            self.__logger.error("Job name is required")
            return 1

        if (self.ruleset_id is None):
            print_error("ruleset_id is required")
            self.__logger.error("ruleset_id is required")
            return 1

        try:
            self.__logger.debug("create job input %s" % str(self))
            api_instance = MaskingJobApi(self.__engine.api_client)
            self.__logger.debug("API instance created")
            response = api_instance.create_masking_job(self)
            self.from_job(response)

            self.__logger.debug("job response %s"
                                % str(response))

            print_message("Job %s added" % self.job_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete job from Engine
        return a 0 if non error
        return 1 in case of error
        """

        try:
            api_instance = MaskingJobApi(self.__engine.api_client)
            response = api_instance.delete_masking_job(
                self.masking_job_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("job response %s"
                                % str(response))
            print_message("Job %s deleted" % self.job_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def update(self):
        """
        Update job in Engine
        return a 0 if non error
        return 1 in case of error
        """

        try:
            api_instance = MaskingJobApi(self.__engine.api_client)
            self.__logger.debug("update job request %s"
                                % str(self))
            response = api_instance.update_masking_job(
                self.masking_job_id,
                self,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("job response %s"
                                % str(response))
            print_message("Job %s updated" % self.job_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def cancel(self):
        """
        Cancel running job in Engine
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



    def start(self, target_connector_id, source_connector_id, nowait, lock):
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
            if source_connector_id:
                execjob.source_connector_id = source_connector_id
            else:
                print_error("Source connector is required for on the fly job")
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
                return self.wait_for_job(response, lock)

        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def wait_for_job(self, execjob, lock):
        """
        Wait for job to finish execution
        :param1 execjob: Execution job response
        Return 0 finished OK
        Return 1 if errors
        """

        execid = execjob.execution_id
        first = True

        exec_api = ExecutionApi(self.__engine.api_client)
        last = 0
        print_message('Waiting for job %s to start processing rows'
                      % self.job_name)
        while execjob.status == 'RUNNING':
            time.sleep(10)
            execjob = exec_api.get_execution_by_id(execid)
            if first and (execjob.rows_total is not None):
                lock.acquire()
                dxm.lib.DxJobs.DxJobCounter.rows_total = dxm.lib.DxJobs.DxJobCounter.rows_total + execjob.rows_total
                lock.release()
                first = False
                # if bar is None:
                #     bar = click.progressbar(show_eta=False,
                #                             length=execjob.rows_total)
            if execjob.rows_masked is not None:
                self.__logger.debug(execjob.rows_masked)
                self.__logger.debug(last)
                step = execjob.rows_masked-last
                # if step == 0:
                #     step = 1
                self.__logger.debug(step)
                lock.acquire()
                dxm.lib.DxJobs.DxJobCounter.rows_masked = dxm.lib.DxJobs.DxJobCounter.rows_masked + step
                lock.release()
                last = execjob.rows_masked
                # if bar is not None:
                #     self.__logger.debug(execjob.rows_masked)
                #     self.__logger.debug(last)
                #     step = execjob.rows_masked-last
                #     if step == 0:
                #         step = 1
                #     self.__logger.debug(step)
                #     bar.update(step)
                #     last = execjob.rows_masked

        if execjob.status == 'SUCCEEDED':
            print_message('')
            print_message('Masking job %s finished.' % self.job_name)
            print_message('%s rows masked' % (execjob.rows_masked or 0))
            self.__logger.debug('Masking job %s finished' % self.job_name)
            self.__logger.debug('%s rows masked' % execjob.rows_masked)
            return 0
        else:
            print_message('')
            self.__logger.error('Problem with masking job %s' % self.job_name)
            self.__logger.error('%s rows masked' % execjob.rows_masked)
            print_error('Problem with masking job %s' % self.job_name)
            print_error('%s rows masked' % (execjob.rows_masked or 0))
            return 1
