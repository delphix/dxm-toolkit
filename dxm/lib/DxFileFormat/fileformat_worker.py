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


from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
import logging
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.Output.DataFormatter import DataFormatter
from dxm.lib.DxTools.DxTools import get_list_of_engines
from dxm.lib.DxFileFormat.DxFileFormatList import DxFileFormatList
from dxm.lib.DxFileFormat.DxFileFormat import DxFileFormat


def fileformat_add(p_engine, fileformat_type, fileformat_file):
    """
    Add application to Masking engine
    param1: p_engine: engine name from configuration
    param2: params: job parameters
    return 0 if added, non 0 for error
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:

        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        fileformatList = DxFileFormatList()
        fileformat = DxFileFormat(engine_obj)

        fileformat.file_format_type = fileformat_type.upper()
        fileformat.file_format_name = fileformat_file.name

        if fileformatList.add(fileformat):
            ret = ret + 1

    return ret


def fileformat_delete(p_engine, fileformat_name):
    """
    Delete application from Masking engine
    param1: p_engine: engine name from configuration
    param2: fileformat_name: file format name
    return 0 if added, non 0 for error
    """

    ret = 0

    logger = logging.getLogger()

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        fileformatList = DxFileFormatList()
        fileformatid = fileformatList.get_file_format_id_by_name(fileformat_name)

        if fileformatList.delete(fileformatid):
            ret = ret + 1

    return ret



def fileformat_list(p_engine, format, fileformat_type, fileformat_name):
    """
    Print list of file formats
    param1: p_engine: engine name from configuration
    param2: format: output format
    param3: fileformat_type: file format type
    param4: fileformat_name: file format name
    return 0 if environment found
    """

    ret = 0

    logger = logging.getLogger()
    logger.debug("fileformat type %s fileformat name %s"
                 % (fileformat_type, fileformat_name))

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("File format type", 30),
                    ("File format name", 30)
                  ]
    data.create_header(data_header)
    data.format_type = format
    for engine_tuple in enginelist:

        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        fileformatList = DxFileFormatList()
        # load all objects

        if fileformat_name:
            fileformats_name = fileformatList.get_all_file_format_id_by_name(
                                            fileformat_name)
            if fileformats_name is None:
                ret = ret + 1
                fileformats_name = []
        else:
            fileformats_name = fileformatList.get_allref()

        if fileformat_type:
            fileformats_type = fileformatList.get_all_file_format_id_by_type(
                                            fileformat_type)
            if fileformats_type is None:
                ret = ret + 1
                fileformats_type = []
        else:
            fileformats_type = fileformats_name

        fileformats = list(set(fileformats_name) & set(fileformats_type))

        if fileformats:
            for fileformatref in fileformats:
                fileformatobj = fileformatList.get_by_ref(fileformatref)
                data.data_insert(
                                  engine_tuple[0],
                                  fileformatobj.file_format_type,
                                  fileformatobj.file_format_name
                                )
        else:
            if fileformat_type and fileformat_name:
                ret = ret + 1

    print("")
    print (data.data_output(False))
    print("")
    return ret
