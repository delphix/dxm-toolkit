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
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel


def DxDatabaseMaskingOptions():

    swagger_types = {
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

    swagger_map = {
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


    
    return GenericModel({ x:None for x in swagger_map.values()}, swagger_types, swagger_map)

 
def DxOnTheFlyJob():

    swagger_types = {
        'connector_id': 'int',
        'connector_type': 'str'
    }

    swagger_map = {
        'connector_id': 'connectorId',
        'connector_type': 'connectorType'
    }


    return GenericModel({ x:None for x in swagger_map.values()}, swagger_types, swagger_map)


def DxMaskingScriptJob(name, contents):

    swagger_types = {
        'name': 'str',
        'contents': 'str'
    }

    swagger_map = {
        'name': 'name',
        'contents': 'contents'
    }

    obj = GenericModel({ x:None for x in swagger_map.values()}, swagger_types, swagger_map)
    obj.name = name
    obj.contents = contents
    return obj