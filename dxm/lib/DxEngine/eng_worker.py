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

from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
import logging
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.Output.DataFormatter import DataFormatter
from dxm.lib.DxTools.DxTools import get_list_of_engines


def engine_add(p_engine, p_ip, p_username, p_password, p_protocol, p_port,
               p_default, p_proxyurl, p_proxyuser, p_proxypassword):
    """
    Add engine to a configuration
    param1: p_engine: name of Masking engine
    param2: p_ip: IP of Masking engine
    param3: p_username: username
    param4: p_password: password
    param5: p_protocol: protocol (http/https)
    param6: p_port: port
    param7: p_default: is engine default - Y/N - default value N
    param8: p_proxyurl: Proxy URL
    param9: p_proxyuser: proxy username
    param10: p_proxypassword: proxy password

    return None if OK or integer with error
    """
    config = DxConfig()
    config.init_metadata()
    if config.insert_engine_info(p_engine, p_ip, p_username, p_password, p_protocol, p_port,
                                 p_default, p_proxyurl, p_proxyuser, p_proxypassword):
        print_error("Problem with adding engine to database")
        config.close()
        return -1
    else:
        print_message("Engine added to configuration")
        config.close()
        return None

def engine_update(p_engine, p_ip, p_username, p_password, p_protocol, p_port,
                  p_default, p_proxyurl, p_proxyuser, p_proxypassword):
    """
    Update engine in configuration
    param1: p_engine: name of Masking engine
    param2: p_ip: IP of Masking engine
    param3: p_username: username
    param4: p_password: password
    param5: p_protocol: protocol (http/https)
    param6: p_port: port
    param7: p_default: is engine default - Y/N - default value N
    return None if OK or integer with error
    """
    config = DxConfig()
    config.init_metadata()
    config.update_engine(p_engine, p_ip, p_username, p_password,
                         p_protocol, p_port, p_default, p_proxyurl, p_proxyuser, p_proxypassword)

def engine_logout(p_engine):
    """
    logout engine in configuration
    param1: p_engine: name of Masking engine
    return None if OK or integer with error
    """
    config = DxConfig()
    config.init_metadata()
    config.set_key(p_engine, None, '')

def engine_delete(p_engine, p_username):
    """
    Delete Masking engines from configuration file
    param1: p_engine: name of Masking engine
    param2: p_username: username
    return None if OK or integer with error, ex. no rows found
    """
    config = DxConfig()
    config.init_metadata()
    if config.delete_engine_info(p_engine, p_username):
        print_error("Problem with deleting engine from database")
        config.close()
        return -1
    else:
        print_message("Engine deleted from configuration")
        config.close()
        return None


def engine_list(p_engine, p_username, p_format):
    """
    List Masking engines from configuration file
    param1: p_engine: name of Masking engine
    param2: p_username: username
    param3: p_format: output format
    return None if OK or integer with error, ex. no rows found
    """
    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("IP", 30),
                    ("username", 30),
                    ("protocol", 8),
                    ("port", 5),
                    ("default", 7),
                    ("proxy URL", 30),
                    ("proxy user", 30)
                  ]
    data.create_header(data_header)
    data.format_type = p_format

    config = DxConfig()
    config.init_metadata()
    if p_engine is None:
        p_engine = 'all'
    rows = config.get_engine_info(p_engine, p_username)

    if rows is None:
        return -1

    for row in rows:
        data.data_insert(
                          row[0],
                          row[1],
                          row[2],
                          row[4],
                          row[5],
                          row[6],
                          row[8],
                          row[9]
                        )
    print("")
    print (data.data_output(False))
    print("")
    return None


def engine_logs(p_engine, outputlog, page_size,level):

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue
        engine_obj.getlogs(outputlog,page_size,level)
