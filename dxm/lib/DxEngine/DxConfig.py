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
# Author  : Marcin Przepiorowski
# Date    : April 2018


import json
import logging
import sqlite3 as lite
import sys
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxConfig(object):

    __conn = None
    __cursor = None
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        """
        self.__logger = logging.getLogger()
        self.__logger.debug("Creating Config object")

        try:
            self.__conn = lite.connect('dxmtoolkit.db')
            self.__cursor = self.__conn.cursor()
        except lite.Error as e:
            msg = "Error %s:" % e.args[0]
            self.__logger.debug(msg)

    @classmethod
    def close(self):
        if self.__conn:
            self.__conn.commit()
            self.__cursor.close()
            self.__conn.close()

    @classmethod
    def __enter__(self):
        return self

    @classmethod
    def __exit__(self):
        self.close()

    @classmethod
    def init_metadata(self):
        if self.__conn:
            self.__logger.debug("Creating table in config")
            sql_dxm_engine_info = \
                """CREATE TABLE IF NOT EXISTS dxm_engine_info
                (
                engine_name varchar(60),
                ip_address varchar(15),
                username varchar(60),
                password varchar(60),
                protocol char(6),
                port integer,
                auth_id varchar(30),
                defengine char(1),
                unique(engine_name, username)
                )"""
            try:
                self.__cursor.execute(sql_dxm_engine_info)
            except lite.Error as e:
                self.__logger.debug("Error %s" % e.args[0])
                print_error("Error %s" % e.args[0])
                sys.exit(-1)

    @classmethod
    def insert_engine_info(self, data):
        """
        insert engine data into sqllite database
        :param data: List of 6 parameters describing engine
                     engine_name
                     ip_address
                     username
                     password
                     protocol
                     port
                     default
        """

        if not all(data):
            self.__logger.debug("Some arguments are empty %s" % str(data))
            return -1

        if len(data) != 7:
            self.__logger.debug("Wrong number of values %s" % str(data))
            return -1

        if self.__conn:
            try:
                sql = "INSERT INTO dxm_engine_info(engine_name," \
                      "ip_address, username, password, protocol," \
                      "port, defengine) VALUES (?,?,?,?,?,?,?)"
                self.__cursor.execute(sql, data)
                self.__conn.commit()
                return None
            except lite.IntegrityError as e:
                self.__logger.debug("Error %s" % e.args)
                print_error("Engine %s and username %s already added." %
                            (data[0], data[2]))
                return -1
            except lite.Error as e:
                self.__logger.debug("Error %s" % e.args)
                return -1
        else:
            self.__logger.debug("No connection open")
            return -1

    @classmethod
    def get_engine_info(self, engine_name, user_name):
        """
        Get engine data from sqllist database for database name
        and user
        :param engine_name: Engine name
        :param user_name: User name
        return list of tuples for each row
        """
        if self.__conn:
            try:
                sql = "SELECT engine_name," \
                      "ip_address, username, password, protocol," \
                      "port, defengine, auth_id from dxm_engine_info " \
                      "where 1=1 "

                data = []

                if engine_name is None:
                    sql = sql + " and defengine = 'Y'"
                else:
                    if (str(engine_name).lower() != 'all'):
                        sql = sql + "and engine_name like ?"
                        data.append(engine_name)

                    if (user_name is not None):
                        sql = sql + "and username like ?"
                        data.append(user_name)

                self.__logger.debug(sql)
                self.__logger.debug(tuple(data))

                self.__cursor.execute(sql, tuple(data))
                rows = self.__cursor.fetchall()
                self.__logger.debug(rows)
                return (rows)
            except lite.Error as e:
                self.__logger.debug("Error %s:" % e.args)
                return None
        else:
            print_error("No connection to local sqllist database")
            sys.exit(-1)

    @classmethod
    def delete_engine_info(self, engine_name, user_name):
        """
        Delete engine data from sqllist database for database name
        and user
        :param engine_name: Engine name
        :param user_name: User name
        return None if OK or integer is error
        """
        if self.__conn:
            try:
                sql = "DELETE from dxm_engine_info " \
                      "where engine_name = ?"

                data = []

                if engine_name is None:
                    print_error("Engine name has to be specify")
                    return -1

                if (str(engine_name).lower() == 'all'):
                    print_error("Engine name can't be all. Sorry")
                    return -1

                data.append(engine_name)

                if (user_name is not None):
                    sql = sql + "and username like ?"
                    data.append(user_name)

                self.__logger.debug(sql)
                self.__logger.debug(tuple(data))
                ret = self.__cursor.execute(sql, tuple(data))
                if ret.rowcount == 0:
                    self.__logger.debug("Engine %s not found"
                                        % engine_name)
                    print_error("Engine %s not found" % engine_name)
                    return 1
                else:
                    self.__conn.commit()
                    self.__logger.debug("Engine %s deleted" % engine_name)
                    print_message("Engine %s deleted" % engine_name)
                    return None
            except lite.Error as e:
                self.__logger.debug("Error %s:" % e.args)
                return -1
        else:
            print_error("No connection to local sqllist database")
            sys.exit(-1)

    @classmethod
    def update_engine(self, engine_name,
                      ip_address,
                      username,
                      password,
                      protocol,
                      port,
                      default):
        """
        update an engine entry
        :param1 engine_name: engine name
        :param2 user_name: user name
        """

        update = None

        if self.__conn:
            try:
                sql = "UPDATE dxm_engine_info " \
                      "set "

                if engine_name is None:
                    print_error("Engine name has to be specify")
                    return -1

                if (str(engine_name).lower() == 'all'):
                    print_error("Engine name can't be all. Sorry")
                    return -1

                data = []

                if ip_address:
                    sql = sql + ' ip_address = ?, '
                    data.append(ip_address)
                    update = 1

                if username:
                    sql = sql + ' username = ?, '
                    data.append(username)
                    update = 1

                if password:
                    sql = sql + ' password = ?, '
                    data.append(password)
                    update = 1

                if protocol:
                    sql = sql + ' protocol = ?, '
                    data.append(protocol)
                    update = 1

                if port:
                    sql = sql + ' port = ?, '
                    data.append(port)
                    update = 1

                if default:
                    sql = sql + ' defengine = ?, '
                    data.append(default)
                    update = 1

                if update:
                    data.append(engine_name)
                    sql = sql + ' engine_name = engine_name ' \
                                ' where engine_name = ? '
                    self.__logger.debug(sql)
                    self.__logger.debug(tuple(data))
                    ret = self.__cursor.execute(sql, tuple(data))
                    self.__logger.debug("number of updated %s"
                                        % ret.rowcount)
                    if ret.rowcount == 0:
                        self.__logger.debug("Engine %s not found"
                                            % engine_name)
                        print_error("Engine %s not found" % engine_name)
                        return 1
                    else:
                        self.__conn.commit()
                        self.__logger.debug("Configuration for engine %s"
                                            " updated in database"
                                            % engine_name)
                        print_message("Configuration for engine %s"
                                      " updated in database"
                                      % engine_name)
                        return None
            except lite.Error as e:
                self.__logger.debug("Error %s:" % e.args)
                return -1
        else:
            print "No connection"
            sys.exit(-1)

    @classmethod
    def set_key(self, engine_name, user_name, auth_key):
        """
        set auth key for engine and user
        :param1 engine_name: engine name
        :param2 user_name: user name
        """

        if self.__conn:
            try:
                sql = "UPDATE dxm_engine_info " \
                      "set auth_id = ? " \
                      "where engine_name = ? "

                data = []

                if engine_name is None:
                    print_error("Engine name has to be specify")
                    return -1

                if (str(engine_name).lower() == 'all'):
                    print_error("Engine name can't be all. Sorry")
                    return -1

                data.append(auth_key)
                data.append(engine_name)

                if (user_name is not None):
                    sql = sql + "and username like ?"
                    data.append(user_name)

                self.__logger.debug(sql)
                self.__logger.debug(tuple(data))
                ret = self.__cursor.execute(sql, tuple(data))
                if ret.rowcount == 0:
                    self.__logger.debug("Engine %s not found"
                                        % engine_name)
                    print_error("Engine %s not found" % engine_name)
                    return 1
                else:
                    self.__conn.commit()
                    self.__logger.debug("Key for engine %s"
                                        " set in database"
                                        % engine_name)
                    return None
            except lite.Error as e:
                self.__logger.debug("Error %s:" % e.args)
                return -1
        else:
            print "No connection"
            sys.exit(-1)

    @classmethod
    def get_key(self, engine_name, user_name):
        """
        Get engine auth key for engine name and user
        and user
        :param engine_name: Engine name
        :param user_name: User name
        return auth_key
        """
        if self.__conn:
            try:
                sql = "SELECT auth_id " \
                      "from dxm_engine_info " \
                      "where engine_name = ? "

                if engine_name is None:
                    print_error("Engine name has to be specify")
                    return -1

                if (str(engine_name).lower() == 'all'):
                    print_error("Engine name can't be all. Sorry")
                    return -1

                data = []
                data.append(engine_name)

                if (user_name is not None):
                    sql = sql + "and username like ?"
                    data.append(user_name)

                self.__logger.debug(sql)
                self.__logger.debug(tuple(data))

                self.__cursor.execute(sql, tuple(data))
                row = self.__cursor.fetchone()
                self.__logger.debug(row)
                return row[0]
            except lite.Error as e:
                self.__logger.debug("Error %s:" % e.args)
                return None
        else:
            print "No connection"
            sys.exit(-1)
