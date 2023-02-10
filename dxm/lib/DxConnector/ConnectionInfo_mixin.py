class ConnectionInfo_mixin:
    swagger_types = {
    'connection_mode' : 'string',
    'path' : 'string',
    'mount_id' : 'integer',
    'host' : 'string',
    'login_name' : 'string',
    'password' : 'string',
    'port' : 'integer',
    'ssh_key' : 'string',
    'user_dir_is_root' : 'boolean'
    }

    swagger_map = {
    'connection_mode' : 'connectionMode',
    'path' : 'path',
    'mount_id' : 'mountId',
    'host' : 'host',
    'login_name' : 'loginName',
    'password' : 'password',
    'port' : 'port',
    'ssh_key' : 'sshKey',
    'user_dir_is_root' : 'userDirIsRoot'
    }


    @property
    def connection_mode(self):
        if self.obj is not None and hasattr(self.obj,'connection_mode'):
            return self.obj.connection_mode
        else:
            return None

    @connection_mode.setter
    def connection_mode(self, connection_mode):
        if self.obj is not None:
            self.obj.connection_mode = connection_mode
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def path(self):
        if self.obj is not None and hasattr(self.obj,'path'):
            return self.obj.path
        else:
            return None

    @path.setter
    def path(self, path):
        if self.obj is not None:
            self.obj.path = path
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def mount_id(self):
        if self.obj is not None and hasattr(self.obj,'mount_id'):
            return self.obj.mount_id
        else:
            return None

    @mount_id.setter
    def mount_id(self, mount_id):
        if self.obj is not None:
            self.obj.mount_id = mount_id
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
    def login_name(self):
        if self.obj is not None and hasattr(self.obj,'login_name'):
            return self.obj.login_name
        else:
            return None

    @login_name.setter
    def login_name(self, login_name):
        if self.obj is not None:
            self.obj.login_name = login_name
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
    def ssh_key(self):
        if self.obj is not None and hasattr(self.obj,'ssh_key'):
            return self.obj.ssh_key
        else:
            return None

    @ssh_key.setter
    def ssh_key(self, ssh_key):
        if self.obj is not None:
            self.obj.ssh_key = ssh_key
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def user_dir_is_root(self):
        if self.obj is not None and hasattr(self.obj,'user_dir_is_root'):
            return self.obj.user_dir_is_root
        else:
            return None

    @user_dir_is_root.setter
    def user_dir_is_root(self, user_dir_is_root):
        if self.obj is not None:
            self.obj.user_dir_is_root = user_dir_is_root
        else:
            raise ValueError("Object needs to be initialized first")