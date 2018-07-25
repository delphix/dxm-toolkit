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


import re
import pytz
import logging
from datetime import datetime, timedelta
from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxLogging import print_error


def get_list_of_engines(p_engine):
    logger = logging.getLogger()
    # read engine from config or read all and put into list
    config = DxConfig()
    enginelist = config.get_engine_info(p_engine, None)
    logger.debug("p_engine %s enginelist %s" % (p_engine, enginelist))

    if len(enginelist) == 0:
        print_error("Engine name %s not found in configuration" % p_engine)
        logger.error("Engine name %s not found in configuration" % p_engine)
        return None
    else:
        return enginelist


def get_objref_by_name(name, object_list):
    """
    return a list of objects reference for name
    """
    logger = logging.getLogger()
    logger.debug("name %s" % name)
    return_list = []

    for ref in object_list.get_allref():
        obj = object_list.get_by_ref(ref)
        if obj.getname() == name:
            return_list.append(ref)

    logger.debug("list of found objects ref %s" % str(return_list))
    return return_list


def get_objref_by_val_and_function(val, object_list, compare_method):
    """
    return a list of objects reference for name
    """
    logger = logging.getLogger()
    logger.debug("name %s compare_method %s" % (val, compare_method))
    return_list = []

    for ref in object_list.get_allref():
        obj = object_list.get_by_ref(ref)
        retname = getattr(obj, compare_method)()
        logger.debug("returned value %s" % retname)
        if retname == val:
            return_list.append(ref)

    logger.debug("list of found objects ref %s" % str(return_list))
    return return_list


def get_objref_by_val_and_attribute(val, object_list, attribute):
    """
    return a list of objects reference for name
    """
    logger = logging.getLogger()
    logger.debug("name %s attribute %s" % (val, attribute))
    return_list = []

    for ref in object_list.get_allref():
        obj = object_list.get_by_ref(ref)
        retname = getattr(obj, attribute)
        logger.debug("returned value %s" % retname)
        if retname == val:
            return_list.append(ref)

    logger.debug("list of found objects ref %s" % str(return_list))
    return return_list


def make_iso_timestamp(timestamp):
    """
    Convert timestamp YYYY-MM-DD HH24:MI:SS
    into ISO format
    """
    logger = logging.getLogger()
    logger.debug("timestamp %s" % timestamp)
    if re.match(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d', timestamp):
        ts = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        iso = str(ts.date()) + 'T' + str(ts.time()) + '.000Z'
    else:
        iso = None

    logger.debug("return iso format %s" % iso)
    return iso


def convert_using_offset(timestamp, src, dst, printtz):
    """
    Convert timestamp from src timezone to dst timezone
    using a offset
    limited to/from UTC
    """
    logger = logging.getLogger()
    logger.debug("timestamp %s" % timestamp)
    logger.debug("timezones %s %s" % (src, dst))
    # fix for Heineken GMT+1 is not something we known
    # also depend on DST GMT+1 can be Europe/Amsterdam in Winter
    # or Europe/Dublin in summer

    m = re.match(r'(\d\d\d\d-\d\d-\d\d)T(\d\d:\d\d:\d\d)\.\d\d\dZ', timestamp)
    if m:
        ts = datetime.strptime(m.group(1) + ' ' + m.group(2),
                               '%Y-%m-%d %H:%M:%S')
    else:
        ts = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    if (src == 'UTC'):
        offset = re.match(r'GMT([+|-]\d\d)\:(\d\d)', dst)
        if offset:
            offsethours = offset.group(1)
            dst_ts = ts + timedelta(hours=int(offsethours))
    elif (dst == 'UTC'):
        offset = re.match(r'GMT([+|-]\d\d)\:(\d\d)', src)
        if offset:
            offsethours = offset.group(1)
            dst_ts = ts - timedelta(hours=int(offsethours))
    else:
        return None

    ret_ts = str(dst_ts.date()) + ' ' + \
        str(dst_ts.time())

    if printtz is not None:
        ret_ts = ret_ts + ' ' + 'GMT' + offsethours

    return ret_ts

def convert_timezone(timestamp, src, dst, printtz):
    """
    Convert timestamp from src timezone to dst timezone
    """
    logger = logging.getLogger()
    logger.debug("timestamp %s" % timestamp)
    logger.debug("timezones %s %s" % (src, dst))


    m = re.match(r'(\d\d\d\d-\d\d-\d\d)T(\d\d:\d\d:\d\d)\.\d\d\dZ', timestamp)
    if m:
        ts = datetime.strptime(m.group(1) + ' ' + m.group(2),
                               '%Y-%m-%d %H:%M:%S')
    else:
        ts = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    try:
        srctz = pytz.timezone(src)
        loc_ts = srctz.localize(ts)
        dsttz = pytz.timezone(dst)
        dst_ts = loc_ts.astimezone(dsttz)
        ret_ts = str(dst_ts.date()) + ' ' + \
            str(dst_ts.time())
        if printtz is not None:
            ret_ts = ret_ts + ' ' + str(dst_ts.tzname())

        return ret_ts
    except TypeError:
        return None


def convert_from_utc(timestamp, timezone, printtz=None):
    offset = re.match(r'GMT([+|-]\d\d)\:(\d\d)', timezone)
    if offset:
        return convert_using_offset(timestamp, 'UTC', timezone, printtz)
    else:
        return convert_timezone(timestamp, 'UTC', timezone, printtz)


def convert_to_utc(timestamp, timezone, printtz=None):
    offset = re.match(r'GMT([+|-]\d\d)\:(\d\d)', timezone)
    if offset:
        return convert_using_offset(timestamp, timezone, 'UTC', printtz)
    else:
        return convert_timezone(timestamp, timezone, 'UTC', printtz)
