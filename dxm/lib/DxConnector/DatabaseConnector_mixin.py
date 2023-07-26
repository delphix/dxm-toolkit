import pprint

class DatabaseConnector_mixin:
    swagger_types = { 
     'database_connector_id' : 'integer',  
     'connector_name' : 'string',  
     'database_type' : 'string',  
     'environment_id' : 'integer',  
     'custom_driver_name' : 'string',  
     'database_name' : 'string',  
     'host' : 'string',  
     'instance_name' : 'string',  
     'jdbc' : 'string',  
     'password' : 'string',  
     'port' : 'integer',  
     'schema_name' : 'string',  
     'sid' : 'string',  
     'username' : 'string',  
     'kerberos_auth' : 'boolean',  
     'service_principal' : 'string',  
     'jdbc_driver_id' : 'integer',  
     'enable_logger' : 'boolean',  
     'file_reference_id' : 'string',  
     'password_vault_auth' : 'boolean',  
     'credential_path_id' : 'integer' 
     }

    swagger_map = { 
     'database_connector_id' : 'databaseConnectorId',  
     'connector_name' : 'connectorName',  
     'database_type' : 'databaseType',  
     'environment_id' : 'environmentId',  
     'custom_driver_name' : 'customDriverName',  
     'database_name' : 'databaseName',  
     'host' : 'host',  
     'instance_name' : 'instanceName',  
     'jdbc' : 'jdbc',  
     'password' : 'password',  
     'port' : 'port',  
     'schema_name' : 'schemaName',  
     'sid' : 'sid',  
     'username' : 'username',  
     'kerberos_auth' : 'kerberosAuth',  
     'service_principal' : 'servicePrincipal',  
     'jdbc_driver_id' : 'jdbcDriverId',  
     'enable_logger' : 'enableLogger',  
     'file_reference_id' : 'fileReferenceId',  
     'password_vault_auth' : 'passwordVaultAuth',  
     'credential_path_id' : 'credentialPathId' 
     }

    @property
    def obj(self):
        if self._obj is not None:
            return self._obj
        else:
            return None

    @obj.setter
    def obj(self, value):
        self._obj = value

    def to_dict_all(self):
        return { k:getattr(self, k) for k,v in self.swagger_map.items() if hasattr(self, k) }

    def to_str(self):
        return pprint.pformat(self.to_dict_all())

    def __repr__(self):
        return self.to_str()

     
    @property
    def database_connector_id(self):
        if self.obj is not None and hasattr(self.obj,'database_connector_id'):
            return self.obj.database_connector_id
        else:
            return None

    @database_connector_id.setter
    def database_connector_id(self, database_connector_id):
        if self.obj is not None:
            self.obj.database_connector_id = database_connector_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def connector_name(self):
        if self.obj is not None and hasattr(self.obj,'connector_name'):
            return self.obj.connector_name
        else:
            return None

    @connector_name.setter
    def connector_name(self, connector_name):
        if self.obj is not None:
            self.obj.connector_name = connector_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def database_type(self):
        if self.obj is not None and hasattr(self.obj,'database_type'):
            return self.obj.database_type
        else:
            return None

    @database_type.setter
    def database_type(self, database_type):
        if self.obj is not None:
            self.obj.database_type = database_type
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def environment_id(self):
        if self.obj is not None and hasattr(self.obj,'environment_id'):
            return self.obj.environment_id
        else:
            return None

    @environment_id.setter
    def environment_id(self, environment_id):
        if self.obj is not None:
            self.obj.environment_id = environment_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def custom_driver_name(self):
        if self.obj is not None and hasattr(self.obj,'custom_driver_name'):
            return self.obj.custom_driver_name
        else:
            return None

    @custom_driver_name.setter
    def custom_driver_name(self, custom_driver_name):
        if self.obj is not None:
            self.obj.custom_driver_name = custom_driver_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def database_name(self):
        if self.obj is not None and hasattr(self.obj,'database_name'):
            return self.obj.database_name
        else:
            return None

    @database_name.setter
    def database_name(self, database_name):
        if self.obj is not None:
            self.obj.database_name = database_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def host(self):
        if self.obj is not None and hasattr(self.obj,'host'):
            return self.obj.host
        else:
            return None

    @host.setter
    def host(self, host):
        if self.obj is not None:
            self.obj.host = host
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def instance_name(self):
        if self.obj is not None and hasattr(self.obj,'instance_name'):
            return self.obj.instance_name
        else:
            return None

    @instance_name.setter
    def instance_name(self, instance_name):
        if self.obj is not None:
            self.obj.instance_name = instance_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def jdbc(self):
        if self.obj is not None and hasattr(self.obj,'jdbc'):
            return self.obj.jdbc
        else:
            return None

    @jdbc.setter
    def jdbc(self, jdbc):
        if self.obj is not None:
            self.obj.jdbc = jdbc
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def password(self):
        if self.obj is not None and hasattr(self.obj,'password'):
            return self.obj.password
        else:
            return None

    @password.setter
    def password(self, password):
        if self.obj is not None:
            self.obj.password = password
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def port(self):
        if self.obj is not None and hasattr(self.obj,'port'):
            return self.obj.port
        else:
            return None

    @port.setter
    def port(self, port):
        if self.obj is not None:
            self.obj.port = port
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def schema_name(self):
        if self.obj is not None and hasattr(self.obj,'schema_name'):
            return self.obj.schema_name
        else:
            return None

    @schema_name.setter
    def schema_name(self, schema_name):
        if self.obj is not None:
            self.obj.schema_name = schema_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def sid(self):
        if self.obj is not None and hasattr(self.obj,'sid'):
            return self.obj.sid
        else:
            return None

    @sid.setter
    def sid(self, sid):
        if self.obj is not None:
            self.obj.sid = sid
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def username(self):
        if self.obj is not None and hasattr(self.obj,'username'):
            return self.obj.username
        else:
            return None

    @username.setter
    def username(self, username):
        if self.obj is not None:
            self.obj.username = username
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def kerberos_auth(self):
        if self.obj is not None and hasattr(self.obj,'kerberos_auth'):
            return self.obj.kerberos_auth
        else:
            return None

    @kerberos_auth.setter
    def kerberos_auth(self, kerberos_auth):
        if self.obj is not None:
            self.obj.kerberos_auth = kerberos_auth
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def service_principal(self):
        if self.obj is not None and hasattr(self.obj,'service_principal'):
            return self.obj.service_principal
        else:
            return None

    @service_principal.setter
    def service_principal(self, service_principal):
        if self.obj is not None:
            self.obj.service_principal = service_principal
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def jdbc_driver_id(self):
        if self.obj is not None and hasattr(self.obj,'jdbc_driver_id'):
            return self.obj.jdbc_driver_id
        else:
            return None

    @jdbc_driver_id.setter
    def jdbc_driver_id(self, jdbc_driver_id):
        if self.obj is not None:
            self.obj.jdbc_driver_id = jdbc_driver_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def enable_logger(self):
        if self.obj is not None and hasattr(self.obj,'enable_logger'):
            return self.obj.enable_logger
        else:
            return None

    @enable_logger.setter
    def enable_logger(self, enable_logger):
        if self.obj is not None:
            self.obj.enable_logger = enable_logger
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def file_reference_id(self):
        if self.obj is not None and hasattr(self.obj,'file_reference_id'):
            return self.obj.file_reference_id
        else:
            return None

    @file_reference_id.setter
    def file_reference_id(self, file_reference_id):
        if self.obj is not None:
            self.obj.file_reference_id = file_reference_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def password_vault_auth(self):
        if self.obj is not None and hasattr(self.obj,'password_vault_auth'):
            return self.obj.password_vault_auth
        else:
            return None

    @password_vault_auth.setter
    def password_vault_auth(self, password_vault_auth):
        if self.obj is not None:
            self.obj.password_vault_auth = password_vault_auth
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def credential_path_id(self):
        if self.obj is not None and hasattr(self.obj,'credential_path_id'):
            return self.obj.credential_path_id
        else:
            return None

    @credential_path_id.setter
    def credential_path_id(self, credential_path_id):
        if self.obj is not None:
            self.obj.credential_path_id = credential_path_id
        else:
            raise ValueError("Object needs to be initialized first")
          