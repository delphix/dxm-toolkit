from unittest import TestCase
from unittest import main
from mock import call, mock_open, patch
import mock
import sys
import datetime
from dxm.lib.DxLogging import logging_est
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from masking_apis.models.page_info import PageInfo
from masking_apis.apis.file_format_api import FileFormatApi
from masking_apis.models.file_format import FileFormat
from masking_apis.models.file_format_list import FileFormatList
from dxm.lib.DxFileFormat.fileformat_worker import fileformat_list
from dxm.lib.DxFileFormat.fileformat_worker import fileformat_add
from dxm.lib.DxFileFormat.fileformat_worker import fileformat_delete

def retok(*args, **kwargs):
    return None


def fileformat_load(a, **kwargs):
    """
    Create an output for get_all_file_formats call
    """
    pi = PageInfo(number_on_page=2, total=2)
    ff = [
            FileFormat(file_format_id=1, file_format_name="testformat",
                       file_format_type="DELIMITED"),
            FileFormat(file_format_id=2, file_format_name="testexcel",
                       file_format_type="EXCEL"),
         ]
    ffrpo = FileFormatList(page_info=pi, response_list=ff)
    return ffrpo



@mock.patch.object(
    DxMaskingEngine, 'get_session', return_value=None)
@mock.patch.object(
    FileFormatApi, 'get_all_file_formats', new=fileformat_load
)
@mock.patch.object(
    FileFormatApi, 'delete_file_format', new=retok
)
class TestFileFormat(TestCase):
    def test_1_fileformat_list(self, get_session):
        ret = fileformat_list(None, "csv", None, None)
        self.assertEquals(ret, 0)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        self.assertEquals(
            output, '#Engine name,File format type,File format name\r\n'
            'testeng,DELIMITED,testformat\r\n'
            'testeng,EXCEL,testexcel')

    def test_2_fileformat_list_by_name(self, get_session):
        ret = fileformat_list(None, "csv", None, "testformat")
        self.assertEquals(ret, 0)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        self.assertEquals(
            output, '#Engine name,File format type,File format name\r\n'
            'testeng,DELIMITED,testformat')

    def test_3_fileformat_list_by_name_error(self, get_session):
        ret = fileformat_list(None, "csv", None, "notfound")
        self.assertEquals(ret, 1)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        self.assertEquals(
            output, 'File format notfound not found\n\n'
            '#Engine name,File format type,File format name')


    def test_4_fileformat_add(self, get_session):
        with mock.patch.object(
                FileFormatApi, 'create_file_format',
                return_value=FileFormat(file_format_id=3,
                                        file_format_type='DELIMITED',
                                        file_format_name='newfile')) \
                as mock_method:

            f = open("newfile", "w+")

            ret = fileformat_add(None, 'DELIMITED', f)
            name, args, kwargs = mock_method.mock_calls[0]
            self.assertEqual("DELIMITED", args[1])
            self.assertEqual("newfile", args[0])
            self.assertEqual(0, ret)

    def test_5_fileformat_delete(self, get_session):
        ret = fileformat_delete(None, "newfile")
        self.assertEqual(0, ret)




if __name__ == '__main__':
    logging_est('test.log', False)
    main(buffer=True, verbosity=2)
