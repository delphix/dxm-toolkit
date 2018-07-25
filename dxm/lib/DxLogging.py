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

"""
Package DxLogging
"""

import logging
import sys
import traceback
from logging.handlers import TimedRotatingFileHandler
import click
import json

VERSION = 'v.0.0.001'




def print_error(msg):
    try:
        error = json.loads(msg)
    except ValueError:
        click.secho(msg, fg='red')
    else:
        click.secho(error["errorMessage"], fg='red')


def print_message(msg):
    click.echo(msg)


def exception_handler(etype, value, tb):
    """
    exception printing handler
    """
    if logging.getLogger().getEffectiveLevel() < 20:
        print_exception("".join(traceback.format_exception(etype, value, tb)))
    else:
        print_exception("".join(traceback.format_exception_only(etype, value)))


def logging_est(logfile_path, debug=False):
    """
    Establish Logging

    logfile_path: path to the logfile. Default: current directory.
    debug: Set debug mode on (True) or off (False). Default: False
    """

    if logfile_path is None:
        return

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    debugfile = TimedRotatingFileHandler(logfile_path,
                                         when="D",
                                         interval=1)
    # formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')
    formatter = logging.Formatter('[%(asctime)s:%(levelname)s:%(module)s:'
                                  '%(lineno)s - %(funcName)s()] %(message)s')
    debugfile.setFormatter(formatter)

    if debug is True:
        debugfile.setLevel(logging.DEBUG)
    else:
        debugfile.setLevel(logging.ERROR)

    logger.addHandler(debugfile)

    sys.excepthook = exception_handler


def print_exception(print_obj):
    """
    Call this function with a log message to prefix the message with EXCEPTION
    """
    logger = logging.getLogger()
    logger.error('EXCEPTION: %s' % (str(print_obj)))
