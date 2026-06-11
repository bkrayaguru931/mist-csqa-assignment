#tests\api_tests\org_api_tests.py
import pytest
import logging
from libs.api_libs.org_api_libs import *

org_obj = OrgAPILibs()

class TestOrgAPI():

    org_id = ""  # Class variable for Org ID

    def test_01_create_org(self, env):
        """
        Test to create an organization via API and validate the response.
        """
        logging.info("*********************************************************************************")
        logging.info("###################   IN TEST METHOD {} ################".format("test_01_create_org"))
        create_org = org_obj._op_create_org(env)

        # Making the Org ID available for other test methods.
        TestOrgAPI.org_id = create_org['id']

        assert (org_obj._is_org_present(env, create_org['id']))

    def test_02_update_org(self, env):
        """
        Test to update an existing organization via API and validate the response.
        """
        logging.info("*********************************************************************************")
        logging.info("###################   IN TEST METHOD {} ################".format("test_02_update_org"))

        # Generate new Org Name
        org_payload = {"name": org_obj.create_random_org_name()}

        # Update the Org Name
        updated_org = org_obj._op_update_org(env, TestOrgAPI.org_id, org_payload)

        assert (updated_org['name'] == org_payload['name'])

    def test_03_delete_org(self, env):
        """
        Test to delete an existing organization via API and validate the response.
        """
        logging.info("*********************************************************************************")
        logging.info("###################   IN TEST METHOD {} ################".format("test_03_delete_org"))

        # Delete the Org
        org_obj._op_delete_org(env, TestOrgAPI.org_id)

        assert (not org_obj._is_org_present(env, TestOrgAPI.org_id))