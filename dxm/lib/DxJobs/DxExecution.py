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
from tqdm import tqdm
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.masking_api.api.execution_api import ExecutionApi
from dxm.lib.masking_api.api.execution_component_api import ExecutionComponentApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel
from dateutil.parser import parse



class DxExecution(object):

    swagger_types = {
        'execution_id': 'int',
        'job_id': 'int',
        'source_connector_id': 'int',
        'target_connector_id': 'int',
        'status': 'str',
        'rows_masked': 'int',
        'rows_total': 'int',
        'start_time': 'datetime',
        'end_time': 'datetime'
    }

    swagger_map = {
        'execution_id': 'executionId',
        'job_id': 'jobId',
        'source_connector_id': 'sourceConnectorId',
        'target_connector_id': 'targetConnectorId',
        'status': 'status',
        'rows_masked': 'rowsMasked',
        'rows_total': 'rowsTotal',
        'start_time': 'startTime',
        'end_time': 'endTime'
    }


    def __init__(self, job_id):
        self.__obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.__obj.job_id = job_id


    def from_exec(self, exe):
        self.__obj = exe
        self.__obj.swagger_types = self.swagger_types
        self.__obj.swagger_map = self.swagger_map

    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

    @property
    def execution_id(self):
        if self.obj is not None and hasattr(self.obj, 'execution_id'):
            return self.obj.execution_id
        else:
            return None

    @property
    def job_id(self):
        if self.obj is not None and hasattr(self.obj, 'job_id'):
            return self.obj.job_id
        else:
            return None

    @property
    def status(self):
        if self.obj is not None and hasattr(self.obj, 'status'):
            return self.obj.status
        else:
            return None

    @property
    def source_connector_id(self):
        if self.obj is not None and hasattr(self.obj, 'source_connector_id'):
            return self.obj.source_connector_id
        else:
            return None

    @property
    def target_connector_id(self):
        if self.obj is not None and hasattr(self.obj, 'target_connector_id'):
            return self.obj.target_connector_id
        else:
            return None


    @target_connector_id.setter
    def target_connector_id(self, value):
        self.obj.target_connector_id = value


    @property
    def rows_masked(self):
        if self.obj is not None and hasattr(self.obj, 'rows_masked'):
            return self.obj.rows_masked
        else:
            return None

    @property
    def rows_total(self):
        if self.obj is not None and hasattr(self.obj, 'rows_total'):
            return self.obj.rows_total
        else:
            return None


    @property
    def start_time(self):
        if self.obj is not None and hasattr(self.obj, 'start_time'):

            try:
                if self.obj.start_time is None:
                    return None
                return parse(self.obj.start_time)

            except ValueError:
                raise ApiException(
                    status=0,
                    reason=(
                        "Failed to parse `{0}` as datetime object"
                        .format(self.obj.start_time)
                    )
                )


        else:
            return None


    @property
    def end_time(self):
        if self.obj is not None and hasattr(self.obj, 'end_time'):
            try:
                if self.obj.end_time is None:
                    return None
                return parse(self.obj.end_time)

            except ValueError:
                raise ApiException(
                    status=0,
                    reason=(
                        "Failed to parse `{0}` as datetime object"
                        .format(self.obj.end_time)
                    )
                )
        else:
            return None