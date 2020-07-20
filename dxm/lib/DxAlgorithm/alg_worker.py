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

from dxm.lib.DxAlgorithm.DxAlgorithmList import DxAlgorithmList
from dxm.lib.DxAlgorithm.DxAlgorithm import DxAlgorithm
from dxm.lib.DxDomain.DxDomainList import DxDomainList
import sys


def algorithm_list(p_engine, format, algname):
    """
    Print list of algorithms
    param1: p_engine: engine name from configuration
    param2: format: output format
    param2: algname: algname name to list, all if None
    return 0 if algname found
    """

    ret = 0

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Algorithm name", 30),
                    ("Domain name", 32),
                    ("Syncable", 9),
                    ("Algorithm type", 30),
                  ]
    data.create_header(data_header)
    data.format_type = format
    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        
        #domainlist.LoadDomains()


        alglist = DxAlgorithmList()
        #alglist.LoadAlgorithms()

        algref_list = []

        if algname:
            algobj = alglist.get_by_ref(algname)
            if algobj:
                algref_list.append(algobj.algorithm_name)
        else:
            algref_list = alglist.get_allref()

        for algref in algref_list:
            algobj = alglist.get_by_ref(algref)

            if algobj.sync:
                syncable = 'Y'
            else:
                syncable = 'N'

            data.data_insert(
                              engine_tuple[0],
                              algobj.algorithm_name,
                              algobj.domain_name,
                              syncable,
                              algobj.algorithm_type
                            )

            #algobj.export()

        print("")
        print (data.data_output(False))
        print("")

    return ret


def algorithm_worker(p_engine, algname, **kwargs):
    """
    Select an algorithm and run action on it
    param1: p_engine: engine name from configuration
    param2: algname: algorithm name
    kwargs: parameters to pass including function name to call
    return 0 if algname found
    """

    ret = 0

    function_to_call = kwargs.get('function_to_call')

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        domainlist = DxDomainList()
        domainlist.LoadDomains()

        alglist = DxAlgorithmList()

        algref_list = []


        algobj = alglist.get_by_ref(algname)
        if algobj is None:
            ret = ret + 1
            continue

        dynfunc = globals()[function_to_call]
        if dynfunc(algobj=algobj, engine_obj=engine_obj, **kwargs):
            ret = ret + 1

    return ret

def algorithm_export(p_engine, algname, outputfile):
    """
    Save algorithm to file
    param1: p_engine: engine name from configuration
    param2: algname: algname name to export
    param3: outputfile: output file
    return 0 if OK
    """
    return algorithm_worker(p_engine, algname, outputfile=outputfile,
                            function_to_call='do_export')


def do_export(**kwargs):
    algobj = kwargs.get('algobj')
    algobj.export()

def algorithm_import(p_engine, inputfile):
    """
    Load algorithm from file
    param1: p_engine: engine name from configuration
    param2: inputfile: input file
    return 0 if OK
    """
    ret = 0


    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        algobj = DxAlgorithm(engine_obj)
        algobj.importalg(None)
