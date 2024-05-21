import pprint

class User_mixin:
    swagger_types = { 
     'user_id' : 'integer',  
     'user_name' : 'string',  
     'password' : 'string',  
     'first_name' : 'string',  
     'last_name' : 'string',  
     'email' : 'string',  
     'is_admin' : 'boolean',  
     'show_welcome' : 'boolean',  
     'user_status' : 'string',  
     'disable_reason' : 'string',  
     'non_admin_properties' : 'non_admin_properties',  
     'api_access' : 'boolean',  
     'principal' : 'string' 
     }

    swagger_map = { 
     'user_id' : 'userId',  
     'user_name' : 'userName',  
     'password' : 'password',  
     'first_name' : 'firstName',  
     'last_name' : 'lastName',  
     'email' : 'email',  
     'is_admin' : 'isAdmin',  
     'show_welcome' : 'showWelcome',  
     'user_status' : 'userStatus',  
     'disable_reason' : 'disableReason',  
     'non_admin_properties' : 'nonAdminProperties',  
     'api_access' : 'apiAccess',  
     'principal' : 'principal' 
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
    def user_id(self):
        if self.obj is not None and hasattr(self.obj,'user_id'):
            return self.obj.user_id
        else:
            return None

    @user_id.setter
    def user_id(self, user_id):
        if self.obj is not None:
            self.obj.user_id = user_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def user_name(self):
        if self.obj is not None and hasattr(self.obj,'user_name'):
            return self.obj.user_name
        else:
            return None

    @user_name.setter
    def user_name(self, user_name):
        if self.obj is not None:
            self.obj.user_name = user_name
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
    def first_name(self):
        if self.obj is not None and hasattr(self.obj,'first_name'):
            return self.obj.first_name
        else:
            return None

    @first_name.setter
    def first_name(self, first_name):
        if self.obj is not None:
            self.obj.first_name = first_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def last_name(self):
        if self.obj is not None and hasattr(self.obj,'last_name'):
            return self.obj.last_name
        else:
            return None

    @last_name.setter
    def last_name(self, last_name):
        if self.obj is not None:
            self.obj.last_name = last_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def email(self):
        if self.obj is not None and hasattr(self.obj,'email'):
            return self.obj.email
        else:
            return None

    @email.setter
    def email(self, email):
        if self.obj is not None:
            self.obj.email = email
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def is_admin(self):
        if self.obj is not None and hasattr(self.obj,'is_admin'):
            return self.obj.is_admin
        else:
            return None

    @is_admin.setter
    def is_admin(self, is_admin):
        if self.obj is not None:
            self.obj.is_admin = is_admin
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def show_welcome(self):
        if self.obj is not None and hasattr(self.obj,'show_welcome'):
            return self.obj.show_welcome
        else:
            return None

    @show_welcome.setter
    def show_welcome(self, show_welcome):
        if self.obj is not None:
            self.obj.show_welcome = show_welcome
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def user_status(self):
        if self.obj is not None and hasattr(self.obj,'user_status'):
            return self.obj.user_status
        else:
            return None

    @user_status.setter
    def user_status(self, user_status):
        if self.obj is not None:
            self.obj.user_status = user_status
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def disable_reason(self):
        if self.obj is not None and hasattr(self.obj,'disable_reason'):
            return self.obj.disable_reason
        else:
            return None

    @disable_reason.setter
    def disable_reason(self, disable_reason):
        if self.obj is not None:
            self.obj.disable_reason = disable_reason
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def non_admin_properties(self):
        if self.obj is not None and hasattr(self.obj,'non_admin_properties'):
            return self.obj.non_admin_properties
        else:
            return None

    @non_admin_properties.setter
    def non_admin_properties(self, non_admin_properties):
        if self.obj is not None:
            self.obj.non_admin_properties = non_admin_properties
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def api_access(self):
        if self.obj is not None and hasattr(self.obj,'api_access'):
            return self.obj.api_access
        else:
            return None

    @api_access.setter
    def api_access(self, api_access):
        if self.obj is not None:
            self.obj.api_access = api_access
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def principal(self):
        if self.obj is not None and hasattr(self.obj,'principal'):
            return self.obj.principal
        else:
            return None

    @principal.setter
    def principal(self, principal):
        if self.obj is not None:
            self.obj.principal = principal
        else:
            raise ValueError("Object needs to be initialized first")
          