import json
import re
from jinja2 import Environment, BaseLoader

    # swagger_types = {
    #     'algorithm_name': 'str',
    #     'algorithm_type': 'str',
    #     'created_by': 'str',
    #     'description': 'str',
    #     'algorithm_extension': 'dict',
    #     'framework_id': 'int',
    #     'plugin_id': 'int',
    #     'fields': 'dict'
    # }

    # swagger_map = {
    #     'algorithm_name': 'algorithmName',
    #     'algorithm_type': 'algorithmType',
    #     'created_by': 'createdBy',
    #     'description': 'description',
    #     'algorithm_extension': 'algorithmExtension',
    #     'framework_id': 'frameworkId',
    #     'plugin_id': 'pluginId',
    #     'fields' : 'fields'
    # }

def to_snake_case(name: str) -> str:
    name = name.replace('_','')
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

with open("api.json","r") as api_file:
    api_dict = json.load(api_file)


type_file_mapping = {
    'Algorithm': 'DxAlgorithm/Algorithm_mixin.py'
    ,'AlgorithmExtension': 'DxAlgorithm/AlgorithmExtension_mixin.py'
    # ,'AlgorithmFramework' 
    # ,'AlgorithmFrameworkList' 
    # ,'AlgorithmList'
    # ,'AlgorithmIdentifier' 
    # ,'AlgorithmValidation' 
    # ,'AlgorithmAssignmentDetail'
    # ,'AlgorithmMigration'
    # ,'AlgorithmMigrationList'
    # ,'AlgorithmUsageReport'
    # ,'Analytics'
    # ,'Application'
    # ,'ApplicationList'
    # ,'ApplicationSettings'
    # ,'ApplicationSettingsList'
    # ,'AsyncTask'
    # ,'AsyncTaskList'
    # ,'AuditLog'
    # ,'AuditLogList'
    # ,'BinaryLookupExtension'
    # ,'BreakpointInstance'
    # ,'BreakpointStartData'
    # ,'BreakpointTimeout'
    ,'ColumnMetadata': 'DxColumn/ColumnMetadata_mixin.py'
    # ,'ColumnMetadataList'
    ,'ConnectionInfo': 'DxConnector/ConnectionInfo_mixin.py'
    # ,'ConnectionProperties'
    ,'DatabaseConnector': 'DxConnector/DatabaseConnector_mixin.py'
    #,'DatabaseConnectorList'
    # ,'DatabaseMaskingOptions'
    ,'DatabaseRuleset' : 'DxRuleset/DatabaseRuleset_mixin.py'
    # ,'DatabaseRulesetList'
    ,'DatabaseRulesetCopy' : 'DxRuleset/DatabaseRulesetCopy.py'
    # ,'DataCleansingExtension'
    # ,'Domain'
    # ,'DomainList'
    ,'Environment' : 'DxEnvironment/Environment_mixin.py'
    # ,'EnvironmentList'
    # ,'ErrorMessage'
    ,'Execution' : 'DxJobs/Execution_mixin.py'
    # ,'ExecutionList'
    ,'ExecutionComponent' : 'DxJobs/ExecutionComponent_mixin.py'
    # ,'ExecutionComponentLogsList'
    # ,'ExecutionComponentLogByComponentId'
    # ,'ExecutionComponentList'
    ,'ExecutionEvent' : 'DxJobs/ExecutionEvent_mixin.py'
    # ,'ExecutionEventList'
    # ,'ExecutionLogsList'
    # ,'ExecutionLogById'
    #,'ExportObject' : 'DxSync/ExportObject_mixin.py'
    ,'ExportObjectMetadata' : 'DxSync/ExportObjectMetadata_mixin.py'
    # ,'ExportObjectMetadataList'
    # ,'ExportResponseMetadata'
    ,'FileConnector' : 'DxConnector/FileConnector_mixin.py'
    # ,'FileConnectorList'
    ,'FileFieldMetadata': 'DxColumn/FileFieldMetadata_mixin.py'
    # ,'FileFieldMetadataList'
    ,'FileFormat': 'DxFileFormat/FileFormat_mixin.py'
    # ,'FileFormatList'
    # ,'FileMetadata'
    # ,'FileMetadataList'
    # ,'FileMetadataBulkInput'
    ,'FileRuleset' : 'DxRuleset/FileRuleset_mixin.py'
    # ,'FileRulesetList'
    # ,'FileRulesetCopy'
    # ,'FileUpload'
    # ,'FileUploadList'
    # ,'ForgotPassword'
    # ,'FreeTextRedactionExtension'
    # ,'Installation'
    # ,'IntegerIdentifier'
    # ,'JdbcDriver'
    # ,'JdbcDriversList'
    # ,'KeyIdentifier'
    # ,'KnowledgeBaseInfo'
    # ,'KnowledgeBaseInfoList'
    # ,'LogFileInfo'
    # ,'LogFileInfoList'
    # ,'LogStatement'
    # ,'Login'
    # ,'LoginResponse'
    # ,'MainframeDatasetConnector'
    # ,'MainframeDatasetConnectorList'
    # ,'MainframeDatasetFieldMetadata'
    # ,'MainframeDatasetFieldMetadataList'
    # ,'MainframeDatasetFormat'
    # ,'MainframeDatasetFormatList'
    # ,'MainframeDatasetMetadata'
    # ,'MainframeDatasetMetadataList'
    # ,'MainframeDatasetMetadataBulkInput'
    # ,'MainframeDatasetRecordType'
    # ,'MainframeDatasetRecordTypeList'
    # ,'MainframeDatasetRuleset'
    # ,'MainframeDatasetRulesetList'
    # ,'MainframeDatasetRulesetCopy'
    # ,'MappingAlgorithmStats'
    # ,'MappingExtension'
    # ,'MappletExtension'
    ,'MaskingJob' : 'DxJobs/MaskingJob_mixin.py'
    # ,'MaskingJobList'
    # ,'MaskingJobScript'
    # ,'MinMaxExtension'
    # ,'MonitorTask'
    # ,'MonitorTaskList'
    # ,'MountInformation'
    # ,'MountInformationList'
    # ,'NonAdminProperties'
    # ,'NonConformantDataSamples'
    # ,'OAuth2Ready'
    # ,'ObjectIdentifier'
    # ,'OnTheFlyMaskingSource'
    # ,'PageInfo'
    # ,'Plugin'
    # ,'PluginObject'
    # ,'PluginBase'
    # ,'Privilege'
    # ,'ProfileExpression'
    # ,'ProfileTypeExpression'
    # ,'ProfileExpressionList'
    ,'ProfileJob' : 'DxJobs/ProfileJob_mixin.py'
    # ,'ProfileJobList'
    # ,'ProfileSet'
    # ,'ProfileSetList'
    # ,'ReidentificationJob'
    # ,'ReidentificationJobList'
    # ,'RecordType'
    # ,'RecordTypeList'
    # ,'RecordTypeQualifier'
    # ,'RecordTypeQualifierList'
    # ,'ResetPassword'
    # ,'Role'
    # ,'SecureLookupExtension'
    # ,'SegmentMappingExtension'
    # ,'SegmentMappingPreservedRange'
    # ,'SegmentMappingSegment'
    # ,'SshKey'
    # ,'SsoReady'
    # ,'StringIdentifier'
    # ,'SystemInformation'
    ,'TableMetadata' : 'DxTable/TableMetadata_mixin.py'
    # ,'TableMetadataList'
    # ,'TableMetadataBulkInput'
    # ,'TableMetadataCustomSQL'
    # ,'TestConnectorResponse'
    # ,'TokenizationExtension'
    # ,'TokenizationJob'
    # ,'TokenizationJobList'
    # ,'User'
    # ,'UserList'
    # ,'AlgorithmField'
    # ,'ConnectionPropertiesList'
    # ,'ExecutionComponentLog'
    # ,'ExecutionLog'
    # ,'ImportObjectMetadata'
    # ,'JobTask'
    # ,'TaskEvents'
    # ,'NonConformantDataSampleList'
    # ,'NonConformantDataSample'
    # ,'PluginList'
    # ,'ProfileTypeExpressionList'
    # , 'RoleList'
}




findref = re.compile('#/definitions/(.*)$')



for classname, filename in type_file_mapping.items():
    list_swagger_map = []
    list_swagger_types = []
    list_properties = []

    if "properties" in api_dict["definitions"][classname]:
        for k,v in api_dict["definitions"][classname]["properties"].items():
            snake_case_name = to_snake_case(k)
            #print(snake_case_name)
            #print(v)
            if 'type' in v:
                paramtype = v['type']
            else:
                groups = re.match(findref, v['$ref'])
                print(groups)
                if groups:
                    paramtype = to_snake_case(groups.groups()[0])
                else:
                    paramtype = ''
            list_swagger_map.append(f"'{snake_case_name}' : '{k}'")
            list_swagger_types.append(f"'{snake_case_name}' : '{paramtype}'")
            list_properties.append(snake_case_name)


        with open("build.j2","r") as t:
                template_str = t.read()
            

        template = Environment(loader=BaseLoader()).from_string(template_str)

        with open(f'dxm/lib/{filename}', "w") as outf:
            outf.write(template.render(
                classname = f"{classname}_mixin",
                list_swagger_types = list_swagger_types,
                list_swagger_map = list_swagger_map,
                list_properties = list_properties
                )        
            )