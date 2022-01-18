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
import keyring
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxEngine.secret import secret


class DxConfig(object):

    __conn = None
    __cursor = None
    __logger = None

    @classmethod
    def __init__(self, config_file):
        """
        Constructor
        """
        self.__logger = logging.getLogger()
        self.__logger.debug("Creating Config object")

        self.__logger.debug("config file provided: {}".format(config_file))

        if config_file is None:
            dbfileloc="{}/dxmtoolkit.db".format(os.path.abspath(os.path.dirname(sys.argv[0])))
        else:
            dbfileloc=config_file

        self.__logger.debug("dbfileloc: {}".format(dbfileloc))

        try:
            self.__conn = lite.connect(dbfileloc)
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
                proxy_url varchar(60),
                proxy_user varchar(60),
                unique(engine_name, username)
                )"""
            try:
                if self.is_table():
                    if self.get_database_version()==0:
                        # we need to add proxy info
                        self.__logger.debug("Adding columns to the table")
                        self.__cursor.execute('alter table dxm_engine_info add proxy_url varchar(60)')
                        self.__cursor.execute('alter table dxm_engine_info add proxy_user varchar(60)')
                        self.set_database_version(1)
                else:
                    self.__cursor.execute(sql_dxm_engine_info)
                    self.set_database_version(1)
            except lite.Error as e:
                self.__logger.debug("Error %s" % e.args[0])
                print_error("Error %s" % e.args[0])
                sys.exit(-1)


    @classmethod
    def insert_engine_info(self, p_engine, p_ip, p_username, p_password, p_protocol, p_port,
                           p_default, p_proxyurl, p_proxyuser, p_proxypassword):
        """
        insert engine data into sqllite database
                     engine_name
                     ip_address
                     username
                     password
                     protocol
                     port
                     default
                     proxy_url,
                     proxy_username,
                     proxy_password
        """

        password = self.encrypt_password(p_password)

        mandatory_data = [p_engine, p_ip, p_username, password, p_protocol, p_port, p_default]

        if not all(mandatory_data):
            self.__logger.error("Some arguments are empty {}".format(mandatory_data))
            return -1

        insert_data = [p_engine, p_ip, p_username, password, p_protocol, p_port, p_default, p_proxyurl, p_proxyuser]

        if self.__conn:
            try:

                if p_default == 'Y' and self.check_default() == -1:
                    return -1

                sql = "INSERT INTO dxm_engine_info(engine_name," \
                      "ip_address, username, password, protocol," \
                      "port, defengine, proxy_url, proxy_user) VALUES (?,?,?,?,?,?,?,?,?)"
                self.__cursor.execute(sql, insert_data)
                if p_proxyuser:
                    self.set_proxy_password(p_proxyuser, p_proxypassword)
                self.__conn.commit()
                return None
            except lite.IntegrityError as e:
                self.__logger.error("Error %s" % e.args)
                print_error("Engine %s and username %s already added." %
                            (p_engine, p_username))
                return -1
            except lite.Error as e:
                print_error("Error %s" % e.args)
                self.__logger.error("Error %s" % e.args)
                return -1
        else:
            self.__logger.error("No connection open")
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
                      "port, defengine, auth_id, proxy_url, proxy_user from dxm_engine_info " \
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
    def check_uniqness(self, engine_name, engineuser):
        # check if engine_name can be identified without a username

        if engineuser is None:
            sql = "select count(*) from dxm_engine_info where engine_name = ?"
            self.__cursor.execute(sql, tuple([engine_name]))
        else:
            sql = "select count(*) from dxm_engine_info where engine_name = ? and username = ?"
            self.__cursor.execute(sql, tuple([engine_name, engineuser]))
        rowscount = self.__cursor.fetchone()

        if rowscount[0] > 1:
            print_error("Please add an engineuser parameter to uniquly identify an engine")
            return -1
        else:
            return rowscount[0]

    @classmethod
    def check_default(self):
        # check there is already default engine - only one can be default


        sql = "select count(*) from dxm_engine_info where defengine = 'Y'"
        self.__cursor.execute(sql)
        rowscount = self.__cursor.fetchone()

        if rowscount[0] > 0:
            print_error("There can be only one default engine. Please select current default to N and add / update next")
            return -1
        else:
            return rowscount[0]

    @classmethod
    def update_engine(self, engine_name, engineuser,
                      ip_address,
                      username,
                      password,
                      protocol,
                      port,
                      default, proxyurl, proxyuser, proxypassword):
        """
        update an engine entry
        :param1 engine_name: engine name
        :param2 user_name: user name
        """

        update = None

        if self.__conn:
            try:
                
                if self.check_uniqness(engine_name, engineuser) == -1:
                    return -1

                if default == 'Y' and self.check_default() == -1:
                    return -1

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
                    encpassword = self.encrypt_password(password)
                    sql = sql + ' password = ?, '
                    data.append(encpassword)
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

                if proxyurl:
                    sql = sql + ' proxy_url = ?, '
                    data.append(proxyurl)
                    update = 1

                if proxyurl == '':
                    sql = sql + ' proxy_url = NULL, '
                    update = 1

                if proxyuser:
                    sql = sql + ' proxy_user = ?, '
                    data.append(proxyuser)
                    update = 1

                if proxyuser == '':
                    sql = sql + ' proxy_user = NULL, '
                    update = 1
                    proxyuser = self.get_proxy_user(engine_name)
                    self.delete_proxy_password(proxyuser)

                if proxypassword:
                    proxyuser = self.get_proxy_user(engine_name)
                    if proxyuser is None:
                        print_error("To change proxy password, you need to specify a user")
                        sys.exit(-1)
                    self.set_proxy_password(proxyuser, proxypassword)

                if update:
                    data.append(engine_name)

                    if engineuser is not None:
                        data.append(engineuser)
                        sql = sql + ' engine_name = engine_name ' \
                                    ' where engine_name = ? and username = ?'
                    else:
                        sql = sql + ' engine_name = engine_name ' \
                                    ' where engine_name = ?'
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
                self.__logger.error("Error %s:" % e.args)
                print(sql)
                return -1
        else:
            print_error("No connection")
            sys.exit(-1)

    @classmethod
    def set_database_version(self, dbver):
        """
        set internal version of the sqllite
        :param1 dbver: database version
        """

        if self.__conn:
            try:   
                self.__cursor.execute('PRAGMA user_version={}'.format(dbver))
            except lite.Error as e:
                self.__logger.debug("Error %s:" % e.args)
                return -1
        else:
            print_error("No connection")
            sys.exit(-1)


    @classmethod
    def get_database_version(self):
        """
        get internal version of the sqllite
        return database version
        """

        if self.__conn:
            try:   
                self.__cursor.execute('PRAGMA user_version')
                row = self.__cursor.fetchone()
            except lite.Error as e:
                self.__logger.debug("Error %s:" % e.args)
                return -1
        else:
            print_error("No connection")
            sys.exit(-1)

        return row[0]

    @classmethod
    def is_table(self):
        """
        Check if table exists
        return true if table exists
        """

        if self.__conn:
            try:   
                self.__cursor.execute('PRAGMA table_info(dxm_engine_info)')
                row = self.__cursor.fetchone()
                if row:
                    return True
                else:
                    return False
            except lite.Error as e:
                self.__logger.debug("Error %s:" % e.args)
                sys.exit(-1)
        else:
            print_error("No connection")
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
            print_error("No connection")
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
            print_error("No connection")
            sys.exit(-1)

    @classmethod
    def set_proxy_password(self, username, password):
        """
        set proxy user in keyring ( supported only on OSX, Windows and Linux with packages)
        :param1 username: proxy username
        :param2 password: password password
        """

        try:   
            keyring.set_password('dxmc',username,password)
            
        except keyring.errors.NoKeyringError as e:
            print_error("Keyring backend is not configured. Can't use authorized proxy connection from this system")
            self.__logger.debug("Keyring backend is not configured %s:" % e.args)
            sys.exit(-1)

    @classmethod
    def delete_proxy_password(self, username):
        """
        delete proxy password
        :param1 username: proxy username
        """

        try:   
            keyring.delete_password('dxmc',username)
            
        except keyring.errors.NoKeyringError as e:
            print_error("Keyring backend is not configured. Can't use authorized proxy connection from this system")
            self.__logger.debug("Keyring backend is not configured %s:" % e.args)
            sys.exit(-1)

        except keyring.errors.PasswordDeleteError:
            pass


    @classmethod
    def get_proxy_password(self, username):
        """
        get proxy password for an user
        return use password 
        """

        try:   
            password = keyring.get_password('dxmc', username)
            if password is None:
                print_error("Can't find password for proxy user. Try to update engine configuration in dxmc")
                self.__logger.debug("Can't find password for proxy user. Try to update engine configuration in dxmc")
                sys.exit(-1)
            
            return password

        except keyring.errors.NoKeyringError as e:
            print_error("Keyring backend is not configured. Can't use authorized proxy connection from this system")
            self.__logger.debug("Keyring backend is not configured %s:" % e.args)
            sys.exit(-1)

    @classmethod
    def get_proxy_user(self, engine_name):
        """
        Get proxy user
        :param engine_name: Engine name
        return proxyuser
        """
        if self.__conn:
            try:
                sql = "SELECT proxy_user " \
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
            print_error("No connection")
            sys.exit(-1)

    @classmethod
    def encrypt_password(self, password):
        """
        Encrypt password and hash with SHA265
        :param password: password
        return encryted password
        """ 

        hash_object = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hash_object.update(password.encode())
        dhash = hash_object.finalize()
        hashhex = dhash.hex()


        nonce = os.urandom(12)
        cipher = ChaCha20Poly1305(secret)
        enc = cipher.encrypt(nonce, password.encode(), None)
        enchex = enc.hex()

        return nonce.hex() + enchex + hashhex

    @classmethod
    def decrypt_password(self, password):
        """
        Encrypt password and hash with SHA265
        :param password: password
        return encryted password
        """ 

        hashhex = password[-64:]
        enc = password[0:-64]

        try:
            dehex = bytes.fromhex(enc)
            msg_nonce = dehex[:12]
            ciphertext = dehex[12:]
            cipher = ChaCha20Poly1305(secret)
            password = cipher.decrypt(msg_nonce, ciphertext, None)
        except InvalidTag:
            print_error("Wrong encryption key")
            sys.exit(1)

        hash_object = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hash_object.update(password)
        dhash = hash_object.finalize()
        hashhex_check = dhash.hex()

        if hashhex == hashhex_check:
            return password.decode('utf-8')
        else:
            print_error("Password SHA265 value after decrypt is wrong")
            return None