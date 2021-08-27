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
# Date    : August 2021


from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
import logging
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.Output.DataFormatter import DataFormatter
from dxm.lib.DxTools.DxTools import get_list_of_engines
from dxm.lib.DxTools.DxTools import feature_support
from dxm.lib.DxJDBC.DxJDBC import DxJDBC
from dxm.lib.DxJDBC.DxJDBCList import DxJDBCList
from dxm.lib.DxEngine.DxEngineFiles import DxEngineFiles


def driver_add(p_engine, p_username,  driver_name, driver_class_name, driver_file_name):
    """
    Add application to Masking engine
    param1: p_engine: engine name from configuration
    param2: driver_file_name: driver file name
    return 0 if added, non 0 for error
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:

        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        if not feature_support(engine_obj, "5.3.9"):
            ret = ret + 1
            continue
        
        files_obj = DxEngineFiles()
        uploadid = files_obj.upload_file(driver_file_name)

        driverList = DxJDBCList()
        driver = DxJDBC(engine_obj)
        driver.create_driver(driver_name=driver_name, driver_class_name=driver_class_name, file_reference_id=uploadid)

        if driverList.add(driver):
            ret = ret + 1

    return ret


def driver_delete(p_engine, p_username,  driver_name):
    """
    Delete driver from engine
    """

    ret = 0

    logger = logging.getLogger()

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        if not feature_support(engine_obj, "5.3.9"):
            ret = ret + 1
            continue

        driver_list = DxJDBCList()
        driver_ref = driver_list.get_driver_id_by_name(driver_name)

        if driver_list.delete(driver_ref):
            ret = ret + 1

    return ret



def driver_list(p_engine, p_username,  format, driver_name):
    """
    Print list of file formats
    param1: p_engine: engine name from configuration
    param2: format: output format
    param3: drver_name: driver name
    return 0 if environment found
    """

    ret = 0

    logger = logging.getLogger()
    logger.debug("driver_name {}".format(driver_name))

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Driver name", 30),
                    ("Driver class name", 50),
                    ("Built-in", 10)
                  ]
    data.create_header(data_header)
    data.format_type = format
    for engine_tuple in enginelist:

        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        if not feature_support(engine_obj, "5.3.9"):
            ret = ret + 1
            continue

        driver_list = DxJDBCList()
        # load all objects

        if driver_name:
            drivers = driver_list.get_all_driver_id_by_name(driver_name)
            if drivers is None:
                ret = ret + 1
        else:
            drivers = driver_list.get_allref()



        for driver_ref in drivers:
            driver_obj = driver_list.get_by_ref(driver_ref)

            if driver_obj.built_in:
                builtin = "True"
            else:
                builtin = "False"

            data.data_insert(
                                engine_tuple[0],
                                driver_obj.driver_name,
                                driver_obj.driver_class_name,
                                builtin
                            )


    print("")
    print (data.data_output(False))
    print("")
    return ret
