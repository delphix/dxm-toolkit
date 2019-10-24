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

from dxm.lib.DxDomain.DxDomainList import DxDomainList
from dxm.lib.DxDomain.DxDomain import DxDomain


def domain_list(p_engine, format, domainname):
    """
    Print list of algorithms
    param1: p_engine: engine name from configuration
    param2: domainname: domain name to list, all if None
    return 0 if domain name found
    """

    ret = 0

    logger = logging.getLogger()

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Domain name", 32)
                  ]
    data.format_type = format
    data.create_header(data_header)

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue


        domainlist = DxDomainList()
        domainref_list = []

        if domainname:
            domobj = domainlist.get_by_ref(domainname)
            if domobj:
                domainref_list.append(domobj.domain_name)
            else:
                print_error("Domain {} not found".format(domainname))
                return 1
        else:
            domainref_list = domainlist.get_allref()

        for domainref in domainref_list:
            domobj = domainlist.get_by_ref(domainref)
            data.data_insert(
                              engine_tuple[0],
                              domobj.domain_name,
                            )


        print("")
        print (data.data_output(False))
        print("")

    return ret

def domain_add(p_engine, domain_name, classification, default_algname):
    """
    Add the domain to the Masking Engine
    param1: p_engine: engine name from configuration
    param2: domain_name: domain name
    param3: classification: domain classification
    param4: default_algname: default algorithm name
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

        domainlist = DxDomainList()
        domobj = DxDomain(engine_obj)
        # set required properties
        domobj.domain_name = domain_name
        domobj.classification = classification
        domobj.default_algorithm_code = default_algname

        if domainlist.add(domobj):
            ret = ret + 1

    return ret

def domain_delete(p_engine, domain_name):
    """
    Delete the domain from the Masking Engine
    param1: p_engine: engine name from configuration
    param2: domain_name: domain name
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

        domainlist = DxDomainList()
        if domainlist.delete(domain_name):
            ret = ret + 1

    return ret


def domain_update(p_engine, domain_name, classification, default_algname):
    """
    Update the domain to the Masking Engine
    param1: p_engine: engine name from configuration
    param2: domain_name: domain name
    param3: classification: domain classification
    param4: default_algname: default algorithm name
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

        domainlist = DxDomainList()
        domobj = domainlist.get_domain_by_name(domain_name)

        if not domobj:
            print_error("Domain {} not found".format(domain_name))
            return 1
            
        # set required properties
        if classification:
            domobj.classification = classification

        if default_algname:
            domobj.default_algorithm_code = default_algname

        if domobj.update():
            ret = ret + 1

    return ret
