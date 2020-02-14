from unittest import TestCase
from unittest import main
import mock
import sys
from masking_apis.apis.application_api import ApplicationApi
from masking_apis.models.application import Application
from masking_apis.models.application_list import ApplicationList
from masking_apis.models.page_info import PageInfo
from dxm.lib.DxApplication.DxApplicationList import DxApplicationList
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxApplication.app_worker import application_add
from dxm.lib.DxApplication.app_worker import application_list



def app_load(a, b, **kwargs):
    """
    Create an output for get_all_application call
    """
    pi = PageInfo(number_on_page=2, total=2)
    applist = [Application(application_name="App1"), Application(application_name="App2"), Application(application_name="App3", application_id=3)]
    apo = ApplicationList(page_info=pi, response_list=applist)
    return apo


class TestApp(TestCase):
    @mock.patch("dxm.lib.DxApplication.DxApplicationList.paginator", app_load)
    def setUp(self):
        self.dal = DxApplicationList()
        self.dal.LoadApplications()

    def test_application_add(self):
        with mock.patch.object(
                ApplicationApi, 'create_application',
                return_value=None) as mock_method, \
             mock.patch.object(
                 DxMaskingEngine, 'get_session',
                 return_value=None):
            application_add(None, "Test1")
            name, args, kwargs = mock_method.mock_calls[0]
            self.assertEqual("Test1", args[0].application_name)

    @mock.patch("dxm.lib.DxApplication.DxApplicationList.paginator", app_load)
    def test_application_list(self):
        with mock.patch.object(
                DxMaskingEngine, 'get_session',
                return_value=None):
            application_list(None, "csv", "App1")
            if not hasattr(sys.stdout, "getvalue"):
                self.fail("need to run in buffered mode")

            output = sys.stdout.getvalue().strip()
            self.assertEquals(
                output, '#Engine name,Application name\r\ntesteng,App1')

    def test_get_applicationId_by_name(self):
        self.assertEqual("App1", self.dal.get_applicationId_by_name("App1")[0])


    def test_get_applicationId_by_name2(self):
        self.assertEqual(3, self.dal.get_applicationId_by_name("App3")[0])


if __name__ == '__main__':
    main(buffer=True, verbosity=2)
