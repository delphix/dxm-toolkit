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

# Author  : Edward de los Santos
# Comments: DataFormatter class

import json
import operator
import itertools
import re

class DataFormatter(object):

    def __init__(self, format_type="fixed", separator = "="):
        self.results = {}
        self.results['header_length'] = {}
        self.results['headers'] = []
        self.results['data'] = []
        self.header_sep = []
        self.separator = separator
        self.format_type = format_type

    def create_header(self, headers):
        if isinstance(headers,list) is False:
            print("Error: Type is not list")
            exit (1)

        for pos,hdr in enumerate(headers):
            self.results['header_length'][hdr[0]] = hdr[1]
            self.results['headers'].append(hdr[0])



    def data_insert(self, *args):
        self.results['data'].append(tuple([e.encode('utf-8') for e in args]))



    @property
    def data_format(self):
        fmt = ""
        csv_sep = ","
        format_type = self.format_type

        headers = self.results['header_length']

        for pos, key in enumerate(self.results['headers']):
            col_len = self.results['header_length'][key]

            self.header_sep.append(self.separator * int(col_len))

            if format_type == "fixed":
                fmt += "{" + str(pos) + ":<" + str(col_len) + "}" + "  "
            elif format_type == "csv":
                fmt += "{}"

                if pos < (len(headers)-1):
                    fmt += csv_sep
        return fmt


    def data_output(self, nohead, sortby=None):
        data_results = self.results['data']
        data_out = ""
        format_type = self.format_type
        json_results = {}
        json_results['header'] = []
        json_results['data'] = []

        sortby1 = None
        sortby2 = None

        if sortby:
            sortlist = sortby.split(',')
            if len(sortlist) > 1:
                sortby1 = int(sortlist[0]) - 1
                sortby2 = int(sortlist[1]) - 1
            elif len(sortlist) > 0:
                sortby1 = int(sortlist[0]) - 1

        if sortby1 and sortby2:
            data_results.sort(key=operator.itemgetter(sortby1, sortby2))
        elif sortby1:
            data_results.sort(key=operator.itemgetter(sortby1))

        if format_type == "fixed":

            if nohead is False:
                data_out += self.data_format.format(*self.results['headers']) + "\r\n"
                data_out += self.data_format.format(*self.header_sep) + "\r\n"

            for row, dt in enumerate(data_results):
                data_out += self.data_format.format(*data_results[row]) + "\r\n"

        elif format_type == "csv":

            if nohead is False:
                #data_out += self.data_format.format(*self.results['header_length'].keys()) + "\r\n"
                #data_output += self.data_format.format(*self.header_sep) + "\r\n"
                data_out += '#'
                data_out += self.data_format.format(*self.results['headers']) + "\r\n"
                #data_out += self.data_format.format(*self.header_sep) + "\r\n"

            for row, dt in enumerate(data_results):
                data_out += self.data_format.format(*data_results[row]) + "\r\n"

        elif format_type == "json":
            # json_results['header'].append(self.results['header_length'].keys())

            json_list = []

            for row in self.results['data']:
                 json_list.append(dict(itertools.izip(self.results['headers'], row)))
            #
            # for row, dt in enumerate(data_results):
            #     json_results['data'].append(data_results[row])

            data_out = json.dumps(json_list,indent=4)

        return (data_out)
