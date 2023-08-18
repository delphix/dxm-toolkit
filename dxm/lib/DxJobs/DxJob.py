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
import pytz
import sys
from tqdm import tqdm
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
import dxm.lib.DxJobs.DxJobCounter
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.masking_api.api.masking_job_api import MaskingJobApi
from dxm.lib.masking_api.api.execution_api import ExecutionApi
from dxm.lib.masking_api.api.execution_component_api import ExecutionComponentApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel
from dxm.lib.DxJobs.DxJobOptions import DxDatabaseMaskingOptions
from dxm.lib.DxJobs.DxJobOptions import DxMaskingScriptJob
from dxm.lib.DxJobs.DxJobOptions import DxOnTheFlyJob
from dxm.lib.DxJobs.DxExecution import DxExecution
from dxm.lib.DxJobs.DxExecutionComponent import DxExecutionComponent
from dxm.lib.DxJobs.MaskingJob_mixin import MaskingJob_mixin

class DxJob(MaskingJob_mixin):


    def __init__(self, engine, execList, eventList):
        """
        Constructor
        :param1 engine: DxMaskingEngine object
        :param2 execList: list of job executions
        """
        #MaskingJob.__init__(self)
        self.__engine = engine
        self.__execList = []

        if execList is not None:
            for exe in execList:
                newexe = DxExecution(exe.job_id)
                newexe.load_object(exe)

                if eventList is not None and newexe.execution_id in eventList:
                    if 'UNMASKED_DATA' in map(lambda x: x.event_type, eventList[newexe.execution_id]):
                        newexe.status = 'WARNING'

                self.__execList.append(newexe)


        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxJob object")
        self.__monitor = False

        self.__eventList = eventList
        self.__api = MaskingJobApi
        self.__apiexec = ExecutionApi
        self.__apicomponent = ExecutionComponentApi
        self.__apiexc = ApiException
        self._obj = None


    @property
    def monitor(self):
        return self.__monitor

    @monitor.setter
    def monitor(self, value):
        self.__monitor = value

    @property
    def lastExec(self):
        if self.__execList:
            return self.__execList[-1]
        else:
            return None

    @property
    def execList(self):
        return self.__execList


    def load_obj(self, job):
        self._obj = job
        self._obj.swagger_types = self.swagger_types
        self._obj.swagger_map = self.swagger_map

        if hasattr(self._obj,'database_masking_options') and self._obj.database_masking_options is not None:

            opt_swagger_types = {
                'batch_update': 'bool',
                'commit_size': 'int',
                'disable_constraints': 'bool',
                'drop_indexes': 'bool',
                'disable_triggers': 'bool',
                'num_output_threads_per_stream': 'int',
                'truncate_tables': 'bool',
                'prescript': 'dict',
                'postscript': 'dict'
            }

            opt_swagger_map = {
                'batch_update': 'batchUpdate',
                'commit_size': 'commitSize',
                'disable_constraints': 'disableConstraints',
                'drop_indexes': 'dropIndexes',
                'disable_triggers': 'disableTriggers',
                'num_output_threads_per_stream': 'numOutputThreadsPerStream',
                'truncate_tables': 'truncateTables',
                'prescript': 'prescript',
                'postscript': 'postscript'
            }

            self._obj.database_masking_options.swagger_map = opt_swagger_map
            self._obj.database_masking_options.swagger_types = opt_swagger_types


            script_swagger_types = {
                'connector_id': 'int',
                'connector_type': 'str'
            }

            script_swagger_map = {
                'connector_id': 'connectorId',
                'connector_type': 'connectorType'
            }

            if hasattr(self._obj.database_masking_options,'prescript') and self._obj.database_masking_options.prescript is not None:
                self._obj.database_masking_options.prescript.swagger_map = script_swagger_map
                self._obj.database_masking_options.prescript.swagger_types = script_swagger_types

            if hasattr(self._obj.database_masking_options,'postscript') and self._obj.database_masking_options.postscript is not None:
                self._obj.database_masking_options.postscript.swagger_map = script_swagger_map
                self._obj.database_masking_options.postscript.swagger_types = script_swagger_types

        if hasattr(self._obj,'on_the_fly_masking_source') and self._obj.on_the_fly_masking_source is not None:
            self._obj.on_the_fly_masking_source.swagger_map = {
                                                                    'name': 'name',
                                                                    'contents': 'contents'
                                                                }
            self._obj.on_the_fly_masking_source.swagger_types = {
                                                                    'name': 'str',
                                                                    'contents': 'str'
                                                                }



    def create_job(self, job_name, ruleset_id):
        """
        Create an connector object
        :param connector_name
        :param database_type
        :param environment_id
        """  

        self.obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.obj.job_name = job_name
        self.obj.ruleset_id = ruleset_id


    def add(self):
        """
        Add job to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.obj.job_name is None):
            print_error("Job name is required")
            self.__logger.error("Job name is required")
            return 1

        if (self.ruleset_id is None):
            print_error("ruleset_id is required")
            self.__logger.error("ruleset_id is required")
            return 1

        try:
            self.__logger.debug("create job input %s" % str(self.obj))
            api_instance = self.__api(self.__engine.api_client)
            self.__logger.debug("API instance created")
            response = api_instance.create_masking_job(self.obj)
            self.load_obj(response)

            self.__logger.debug("job response %s"
                                % str(response))

            print_message("Job %s added" % self.job_name)
            return 0
        except self.__apiexc as e:
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
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.delete_masking_job(
                self.obj.masking_job_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("job response %s"
                                % str(response))
            print_message("Job %s deleted" % self.job_name)
            return 0
        except self.__apiexc as e:
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
            api_instance = self.__api(self.__engine.api_client)
            self.__logger.debug("update job request %s"
                                % str(self.obj))
            response = api_instance.update_masking_job(
                self.obj.masking_job_id,
                self.obj,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("job response %s"
                                % str(response))
            print_message("Job %s updated" % self.job_name)
            return 0
        except self.__apiexc as e:
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
            execid = self.__lastExec.execution_id
            exec_api = self.__apiexec(self.__engine.api_client)
            self.__logger.debug("Stopping execution %s" % str(execid))
            execjob = exec_api.cancel_execution(execid)
            self.__logger.debug("Stopping execution response %s" % str(execjob))
            while execjob.status == 'RUNNING':
                time.sleep(1)
                execjob = self.get_execution(execid)

            print_message(execjob)
            return 0

        except self.__apiexc as e:
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
        exec_api = self.__apiexec(self.__engine.api_client)
        execjob = DxExecution(job_id = self.masking_job_id)

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
                print_message("Job {} started without monitoring".format(self.job_name))
                return 0
            else:
                return self.wait_for_job(response, posno, lock)

        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            lock.acquire()
            dxm.lib.DxJobs.DxJobCounter.ret = \
                dxm.lib.DxJobs.DxJobCounter.ret + 1
            lock.release()
            self.__logger.error('return value %s'
                                % dxm.lib.DxJobs.DxJobCounter.ret)
            return 1

        except Exception:
            print_error("Unhandled exception")
            print_error(str(sys.exc_info()))
            self.__logger.error(str(sys.exc_info()))
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

        last = 0

        self.__logger.debug('Waiting for job %s to start processing rows'
                            % self.job_name)

        if not self.monitor:
            print_message('Waiting for job %s to start processing rows'
                          % self.job_name)

        while execjob.status == 'RUNNING' or execjob.status == 'QUEUED':
            time.sleep(10)
            execjob = self.get_execution(exec_id=execid)
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



    def filter_executions(self, startdate, enddate):
        """
        Filter job executions using start and end date parameters
        :param1 startdate: start date
        :param2 enddate: end date
        Return a list of filtered executions
        """

        if startdate:
            startdate_tz = startdate.replace(tzinfo=pytz.UTC)

        if enddate:
            enddate_tz = enddate.replace(tzinfo=pytz.UTC)

        if self.execList:
            execlist = []

            for x in self.execList:
                if hasattr(x, "start_time") and x.start_time is not None:
                    l_start_time = x.start_time
                else:
                    # this is possible when queued job was cancel before start
                    self.__logger.debug("Start_time doesn't exist or it's None - using submit_time instead: {}".format(str(x)))
                    l_start_time = x.submit_time
                if ( (startdate is None) or (l_start_time >= startdate_tz) ) and ( (enddate is None) or ( (x.end_time is not None) and (x.end_time <= enddate_tz))):
                    execlist.append(x)

        else:
            execlist = self.execList

        return execlist


    def list_execution_component(self, execid):
        """
        List an execution detalis ( tables, rows, etc)
        :param1 execid: execution id to display
        return a None if non error
        return 1 in case of error
        """

        if (execid is None):
            print_error("Execution id is required")
            self.__logger.error("Execution id is required")
            return 1

        try:

            execcomp = []

            self.__logger.debug("execute component")
            api_instance = self.__apicomponent(self.__engine.api_client)
            execomponents = paginator(
                            api_instance,
                            "get_all_execution_components",
                            execution_id=execid,
                            _request_timeout=self.__engine.get_timeout())

            if execomponents.response_list is not None:
                for exe in execomponents.response_list:
                    newexecomp = DxExecutionComponent()
                    newexecomp.load_object(exe)
                    if self.__eventList is not None and newexecomp.execution_id in self.__eventList and \
                       ('UNMASKED_DATA', newexecomp.execution_component_id) in map(lambda x: (x.event_type, x.execution_component_id), self.__eventList[newexecomp.execution_id]):
                        newexecomp.status = 'WARNING'

                    if self.__eventList is not None and newexecomp.execution_id in self.__eventList:
                        event = [ x for x in self.__eventList[newexecomp.execution_id] if x.execution_component_id == newexecomp.execution_component_id ]
                    else:
                        event = list()
                    execcomp.append((newexecomp, event))


            return execcomp


        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return None



    def get_execution(self, exec_id):
        '''
        Create a DxExecution object and read a execution using execution API
        '''
        exec_api = self.__apiexec(self.__engine.api_client)
        exec_obj = exec_api.get_execution_by_id(exec_id)
        exec = DxExecution(exec_obj.job_id)
        exec.load_object(exec_obj)
        return exec