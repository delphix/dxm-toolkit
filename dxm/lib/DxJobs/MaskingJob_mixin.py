import pprint

class MaskingJob_mixin:
    swagger_types = { 
     'masking_job_id' : 'integer',  
     'job_name' : 'string',  
     'ruleset_id' : 'integer',  
     'ruleset_type' : 'string',  
     'created_by' : 'string',  
     'created_time' : 'string',  
     'email' : 'string',  
     'feedback_size' : 'integer',  
     'job_description' : 'string',  
     'max_memory' : 'integer',  
     'min_memory' : 'integer',  
     'multi_tenant' : 'boolean',  
     'num_input_streams' : 'integer',  
     'on_the_fly_masking' : 'boolean',  
     'database_masking_options' : 'database_masking_options',  
     'on_the_fly_masking_source' : 'on_the_fly_masking_source',  
     'fail_immediately' : 'boolean',  
     'enabled_tasks' : 'array',  
     'stream_row_limit' : 'integer' 
     }

    swagger_map = { 
     'masking_job_id' : 'maskingJobId',  
     'job_name' : 'jobName',  
     'ruleset_id' : 'rulesetId',  
     'ruleset_type' : 'rulesetType',  
     'created_by' : 'createdBy',  
     'created_time' : 'createdTime',  
     'email' : 'email',  
     'feedback_size' : 'feedbackSize',  
     'job_description' : 'jobDescription',  
     'max_memory' : 'maxMemory',  
     'min_memory' : 'minMemory',  
     'multi_tenant' : 'multiTenant',  
     'num_input_streams' : 'numInputStreams',  
     'on_the_fly_masking' : 'onTheFlyMasking',  
     'database_masking_options' : 'databaseMaskingOptions',  
     'on_the_fly_masking_source' : 'onTheFlyMaskingSource',  
     'fail_immediately' : 'failImmediately',  
     'enabled_tasks' : 'enabledTasks',  
     'stream_row_limit' : 'streamRowLimit' 
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
    def masking_job_id(self):
        if self.obj is not None and hasattr(self.obj,'masking_job_id'):
            return self.obj.masking_job_id
        else:
            return None

    @masking_job_id.setter
    def masking_job_id(self, masking_job_id):
        if self.obj is not None:
            self.obj.masking_job_id = masking_job_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def job_name(self):
        if self.obj is not None and hasattr(self.obj,'job_name'):
            return self.obj.job_name
        else:
            return None

    @job_name.setter
    def job_name(self, job_name):
        if self.obj is not None:
            self.obj.job_name = job_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def ruleset_id(self):
        if self.obj is not None and hasattr(self.obj,'ruleset_id'):
            return self.obj.ruleset_id
        else:
            return None

    @ruleset_id.setter
    def ruleset_id(self, ruleset_id):
        if self.obj is not None:
            self.obj.ruleset_id = ruleset_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def ruleset_type(self):
        if self.obj is not None and hasattr(self.obj,'ruleset_type'):
            return self.obj.ruleset_type
        else:
            return None

    @ruleset_type.setter
    def ruleset_type(self, ruleset_type):
        if self.obj is not None:
            self.obj.ruleset_type = ruleset_type
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def created_by(self):
        if self.obj is not None and hasattr(self.obj,'created_by'):
            return self.obj.created_by
        else:
            return None

    @created_by.setter
    def created_by(self, created_by):
        if self.obj is not None:
            self.obj.created_by = created_by
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def created_time(self):
        if self.obj is not None and hasattr(self.obj,'created_time'):
            return self.obj.created_time
        else:
            return None

    @created_time.setter
    def created_time(self, created_time):
        if self.obj is not None:
            self.obj.created_time = created_time
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
    def feedback_size(self):
        if self.obj is not None and hasattr(self.obj,'feedback_size'):
            return self.obj.feedback_size
        else:
            return None

    @feedback_size.setter
    def feedback_size(self, feedback_size):
        if self.obj is not None:
            self.obj.feedback_size = feedback_size
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def job_description(self):
        if self.obj is not None and hasattr(self.obj,'job_description'):
            return self.obj.job_description
        else:
            return None

    @job_description.setter
    def job_description(self, job_description):
        if self.obj is not None:
            self.obj.job_description = job_description
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def max_memory(self):
        if self.obj is not None and hasattr(self.obj,'max_memory'):
            return self.obj.max_memory
        else:
            return None

    @max_memory.setter
    def max_memory(self, max_memory):
        if self.obj is not None:
            self.obj.max_memory = max_memory
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def min_memory(self):
        if self.obj is not None and hasattr(self.obj,'min_memory'):
            return self.obj.min_memory
        else:
            return None

    @min_memory.setter
    def min_memory(self, min_memory):
        if self.obj is not None:
            self.obj.min_memory = min_memory
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def multi_tenant(self):
        if self.obj is not None and hasattr(self.obj,'multi_tenant'):
            return self.obj.multi_tenant
        else:
            return None

    @multi_tenant.setter
    def multi_tenant(self, multi_tenant):
        if self.obj is not None:
            self.obj.multi_tenant = multi_tenant
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def num_input_streams(self):
        if self.obj is not None and hasattr(self.obj,'num_input_streams'):
            return self.obj.num_input_streams
        else:
            return None

    @num_input_streams.setter
    def num_input_streams(self, num_input_streams):
        if self.obj is not None:
            self.obj.num_input_streams = num_input_streams
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def on_the_fly_masking(self):
        if self.obj is not None and hasattr(self.obj,'on_the_fly_masking'):
            return self.obj.on_the_fly_masking
        else:
            return None

    @on_the_fly_masking.setter
    def on_the_fly_masking(self, on_the_fly_masking):
        if self.obj is not None:
            self.obj.on_the_fly_masking = on_the_fly_masking
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def database_masking_options(self):
        if self.obj is not None and hasattr(self.obj,'database_masking_options'):
            return self.obj.database_masking_options
        else:
            return None

    @database_masking_options.setter
    def database_masking_options(self, database_masking_options):
        if self.obj is not None:
            self.obj.database_masking_options = database_masking_options
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def on_the_fly_masking_source(self):
        if self.obj is not None and hasattr(self.obj,'on_the_fly_masking_source'):
            return self.obj.on_the_fly_masking_source
        else:
            return None

    @on_the_fly_masking_source.setter
    def on_the_fly_masking_source(self, on_the_fly_masking_source):
        if self.obj is not None:
            self.obj.on_the_fly_masking_source = on_the_fly_masking_source
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def fail_immediately(self):
        if self.obj is not None and hasattr(self.obj,'fail_immediately'):
            return self.obj.fail_immediately
        else:
            return None

    @fail_immediately.setter
    def fail_immediately(self, fail_immediately):
        if self.obj is not None:
            self.obj.fail_immediately = fail_immediately
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def enabled_tasks(self):
        if self.obj is not None and hasattr(self.obj,'enabled_tasks'):
            return self.obj.enabled_tasks
        else:
            return None

    @enabled_tasks.setter
    def enabled_tasks(self, enabled_tasks):
        if self.obj is not None:
            self.obj.enabled_tasks = enabled_tasks
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def stream_row_limit(self):
        if self.obj is not None and hasattr(self.obj,'stream_row_limit'):
            return self.obj.stream_row_limit
        else:
            return None

    @stream_row_limit.setter
    def stream_row_limit(self, stream_row_limit):
        if self.obj is not None:
            self.obj.stream_row_limit = stream_row_limit
        else:
            raise ValueError("Object needs to be initialized first")
          