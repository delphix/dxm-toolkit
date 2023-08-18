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
from dxm.lib.DxJobs.ExecutionComponent_mixin import ExecutionComponent_mixin


class DxExecutionComponent(ExecutionComponent_mixin):


    def __init__(self):
        self._obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)


    def load_object(self, exe):
        self._obj = exe
        self._obj.swagger_types = self.swagger_types
        self._obj.swagger_map = self.swagger_map


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