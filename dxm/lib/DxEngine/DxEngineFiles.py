import logging

from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.masking_api.api.file_download_api import FileDownloadApi
from dxm.lib.masking_api.api.file_upload_api import FileUploadApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.DxLogging import print_error

class DxEngineFiles(object):

    __engine = None
    __logger = None

    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxEngineFiles object")

    def upload_file(self, filename):
        """
        Load list of rule sets
        Return None if OK
        """

        self.__api = FileUploadApi

        try:

            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.upload_file(filename)
            return response.file_reference_id

        except ApiException as e:
            print_error("Can't upload a file %s" % e.body)
            return 1

