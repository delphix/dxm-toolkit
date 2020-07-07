from unittest import TestCase
from unittest import main
from mock import call, mock_open, patch
import mock
import sys
import datetime
from dxm.lib.DxLogging import logging_est
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from masking_api_60.models.page_info import PageInfo
from masking_api_60.api.domain_api import DomainApi
from masking_api_60.models.domain import Domain
from dxm.lib.DxDomain.domain_worker import domain_list
from dxm.lib.DxDomain.domain_worker import domain_add
from dxm.lib.DxDomain.domain_worker import domain_delete

from engine import retok
from engine import domain_load


@mock.patch.object(
    DxMaskingEngine, 'get_session', return_value=None)
@mock.patch.object(
    DomainApi, 'get_all_domains', new=domain_load
)
@mock.patch.object(
    DomainApi, 'delete_domain', new=retok
)
class TestDomain(TestCase):
    def test_domain_list(self, get_session):
        ret = domain_list(None, "csv", None)
        self.assertEquals(ret, 0)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        self.assertEquals(
            output, '#Engine name,Domain name\r\n'
            'testeng,DOMAIN2\r\n'
            'testeng,DOMAIN1')

    def test_domain_add(self, get_session):
        with mock.patch.object(
                DomainApi, 'create_domain',
                return_value=Domain(domain_name="NEWDOMAIN", default_algorithm_code="ALG")) \
                as mock_method:

            ret = domain_add(None, 'NEWDOMAIN', 'CUSTOMER', 'ALG')
            name, args, kwargs = mock_method.mock_calls[0]
            print args
            self.assertEqual("NEWDOMAIN", args[0].domain_name)
            self.assertEqual("CUSTOMER", args[0].classification)
            self.assertEqual(0, ret)

    def test_delete_domain(self, get_session):
        ret = domain_delete(None, "DOMAIN2")
        self.assertEqual(0, ret)




if __name__ == '__main__':
    logging_est('test.log', False)
    main(buffer=True, verbosity=2)
