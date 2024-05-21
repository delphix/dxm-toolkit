import pprint

class Role_mixin:
    swagger_types = { 
     'role_id' : 'integer',  
     'role_name' : 'string',  
     'environment' : 'privilege',  
     'connector' : 'privilege',  
     'ruleset' : 'privilege',  
     'inventory' : 'privilege',  
     'profile_job' : 'privilege',  
     'masking_job' : 'privilege',  
     'tokenize_job' : 'privilege',  
     'reidentify_job' : 'privilege',  
     'domain' : 'privilege',  
     'algorithm' : 'privilege',  
     'jdbc_driver' : 'privilege',  
     'password_vault' : 'privilege',  
     'plugin' : 'privilege',  
     'profile_expression' : 'privilege',  
     'profile_set' : 'privilege',  
     'file_format' : 'privilege',  
     'user' : 'privilege',  
     'diagnostic' : 'privilege',  
     'inventory_report' : 'privilege',  
     'approve_inventories' : 'privilege' 
     }

    swagger_map = { 
     'role_id' : 'roleId',  
     'role_name' : 'roleName',  
     'environment' : 'environment',  
     'connector' : 'connector',  
     'ruleset' : 'ruleset',  
     'inventory' : 'inventory',  
     'profile_job' : 'profileJob',  
     'masking_job' : 'maskingJob',  
     'tokenize_job' : 'tokenizeJob',  
     'reidentify_job' : 'reidentifyJob',  
     'domain' : 'domain',  
     'algorithm' : 'algorithm',  
     'jdbc_driver' : 'jdbcDriver',  
     'password_vault' : 'passwordVault',  
     'plugin' : 'plugin',  
     'profile_expression' : 'profileExpression',  
     'profile_set' : 'profileSet',  
     'file_format' : 'fileFormat',  
     'user' : 'user',  
     'diagnostic' : 'diagnostic',  
     'inventory_report' : 'inventoryReport',  
     'approve_inventories' : 'approveInventories' 
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
    def role_id(self):
        if self.obj is not None and hasattr(self.obj,'role_id'):
            return self.obj.role_id
        else:
            return None

    @role_id.setter
    def role_id(self, role_id):
        if self.obj is not None:
            self.obj.role_id = role_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def role_name(self):
        if self.obj is not None and hasattr(self.obj,'role_name'):
            return self.obj.role_name
        else:
            return None

    @role_name.setter
    def role_name(self, role_name):
        if self.obj is not None:
            self.obj.role_name = role_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def environment(self):
        if self.obj is not None and hasattr(self.obj,'environment'):
            return self.obj.environment
        else:
            return None

    @environment.setter
    def environment(self, environment):
        if self.obj is not None:
            self.obj.environment = environment
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def connector(self):
        if self.obj is not None and hasattr(self.obj,'connector'):
            return self.obj.connector
        else:
            return None

    @connector.setter
    def connector(self, connector):
        if self.obj is not None:
            self.obj.connector = connector
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def ruleset(self):
        if self.obj is not None and hasattr(self.obj,'ruleset'):
            return self.obj.ruleset
        else:
            return None

    @ruleset.setter
    def ruleset(self, ruleset):
        if self.obj is not None:
            self.obj.ruleset = ruleset
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def inventory(self):
        if self.obj is not None and hasattr(self.obj,'inventory'):
            return self.obj.inventory
        else:
            return None

    @inventory.setter
    def inventory(self, inventory):
        if self.obj is not None:
            self.obj.inventory = inventory
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def profile_job(self):
        if self.obj is not None and hasattr(self.obj,'profile_job'):
            return self.obj.profile_job
        else:
            return None

    @profile_job.setter
    def profile_job(self, profile_job):
        if self.obj is not None:
            self.obj.profile_job = profile_job
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def masking_job(self):
        if self.obj is not None and hasattr(self.obj,'masking_job'):
            return self.obj.masking_job
        else:
            return None

    @masking_job.setter
    def masking_job(self, masking_job):
        if self.obj is not None:
            self.obj.masking_job = masking_job
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def tokenize_job(self):
        if self.obj is not None and hasattr(self.obj,'tokenize_job'):
            return self.obj.tokenize_job
        else:
            return None

    @tokenize_job.setter
    def tokenize_job(self, tokenize_job):
        if self.obj is not None:
            self.obj.tokenize_job = tokenize_job
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def reidentify_job(self):
        if self.obj is not None and hasattr(self.obj,'reidentify_job'):
            return self.obj.reidentify_job
        else:
            return None

    @reidentify_job.setter
    def reidentify_job(self, reidentify_job):
        if self.obj is not None:
            self.obj.reidentify_job = reidentify_job
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def domain(self):
        if self.obj is not None and hasattr(self.obj,'domain'):
            return self.obj.domain
        else:
            return None

    @domain.setter
    def domain(self, domain):
        if self.obj is not None:
            self.obj.domain = domain
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def algorithm(self):
        if self.obj is not None and hasattr(self.obj,'algorithm'):
            return self.obj.algorithm
        else:
            return None

    @algorithm.setter
    def algorithm(self, algorithm):
        if self.obj is not None:
            self.obj.algorithm = algorithm
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def jdbc_driver(self):
        if self.obj is not None and hasattr(self.obj,'jdbc_driver'):
            return self.obj.jdbc_driver
        else:
            return None

    @jdbc_driver.setter
    def jdbc_driver(self, jdbc_driver):
        if self.obj is not None:
            self.obj.jdbc_driver = jdbc_driver
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def password_vault(self):
        if self.obj is not None and hasattr(self.obj,'password_vault'):
            return self.obj.password_vault
        else:
            return None

    @password_vault.setter
    def password_vault(self, password_vault):
        if self.obj is not None:
            self.obj.password_vault = password_vault
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def plugin(self):
        if self.obj is not None and hasattr(self.obj,'plugin'):
            return self.obj.plugin
        else:
            return None

    @plugin.setter
    def plugin(self, plugin):
        if self.obj is not None:
            self.obj.plugin = plugin
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def profile_expression(self):
        if self.obj is not None and hasattr(self.obj,'profile_expression'):
            return self.obj.profile_expression
        else:
            return None

    @profile_expression.setter
    def profile_expression(self, profile_expression):
        if self.obj is not None:
            self.obj.profile_expression = profile_expression
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def profile_set(self):
        if self.obj is not None and hasattr(self.obj,'profile_set'):
            return self.obj.profile_set
        else:
            return None

    @profile_set.setter
    def profile_set(self, profile_set):
        if self.obj is not None:
            self.obj.profile_set = profile_set
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def file_format(self):
        if self.obj is not None and hasattr(self.obj,'file_format'):
            return self.obj.file_format
        else:
            return None

    @file_format.setter
    def file_format(self, file_format):
        if self.obj is not None:
            self.obj.file_format = file_format
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def user(self):
        if self.obj is not None and hasattr(self.obj,'user'):
            return self.obj.user
        else:
            return None

    @user.setter
    def user(self, user):
        if self.obj is not None:
            self.obj.user = user
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def diagnostic(self):
        if self.obj is not None and hasattr(self.obj,'diagnostic'):
            return self.obj.diagnostic
        else:
            return None

    @diagnostic.setter
    def diagnostic(self, diagnostic):
        if self.obj is not None:
            self.obj.diagnostic = diagnostic
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def inventory_report(self):
        if self.obj is not None and hasattr(self.obj,'inventory_report'):
            return self.obj.inventory_report
        else:
            return None

    @inventory_report.setter
    def inventory_report(self, inventory_report):
        if self.obj is not None:
            self.obj.inventory_report = inventory_report
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def approve_inventories(self):
        if self.obj is not None and hasattr(self.obj,'approve_inventories'):
            return self.obj.approve_inventories
        else:
            return None

    @approve_inventories.setter
    def approve_inventories(self, approve_inventories):
        if self.obj is not None:
            self.obj.approve_inventories = approve_inventories
        else:
            raise ValueError("Object needs to be initialized first")
          