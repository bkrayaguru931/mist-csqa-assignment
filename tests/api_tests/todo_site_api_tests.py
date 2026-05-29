import pytest
import logging
from libs.api_libs.org_api_libs import OrgAPILibs
from libs.api_libs.todo_site_api_libs import SiteAPILibs

org_obj = OrgAPILibs()
site_obj = SiteAPILibs()


class TestSiteAPI:
    """
    End-to-end CRUD tests for the Mist Sites API.

    A fresh Org is created once per class (setup_and_teardown_org fixture)
    and torn down after all tests finish.  The site_id created in test_01
    is stored as a class variable so subsequent tests can reference it —
    the same pattern used by TestOrgAPI.

    Run order is intentional
    """

    org_id: str = ""
    site_id: str = ""

    # Fixtures

    @pytest.fixture(scope="class", autouse=True)
    def setup_and_teardown_org(self, env):
        """
        Class-scoped fixture: create one Org before all Site tests run,
        then delete it afterward (even if tests fail).
        """
        logging.info("*** [TestSiteAPI] Setting up Org ***")
        create_org = org_obj._op_create_org(env)
        TestSiteAPI.org_id = create_org["id"]

        yield  # ← all test methods run here

        logging.info("*** [TestSiteAPI] Tearing down Org ***")
        org_obj._op_delete_org(env, TestSiteAPI.org_id)

    # Test cases

    def test_01_create_site(self, env):
        """
        Create a Site under the test Org with a randomly generated name,
        then verify it appears in the org-level site listing.
        """
        logging.info("*" * 89)
        logging.info("###  test_01_create_site  ###")

        create_site = site_obj._op_create_site(env, TestSiteAPI.org_id)
        TestSiteAPI.site_id = create_site["id"]

        # Verify the newly created site is discoverable via the listing endpoint.
        assert site_obj._is_site_present(env, TestSiteAPI.org_id, TestSiteAPI.site_id), \
            f"Site {TestSiteAPI.site_id} was not found in org {TestSiteAPI.org_id} after creation."

    def test_02_update_site(self, env):
        """
        Update the Site's name to a new randomly generated value and assert
        that the API response reflects the change.
        """
        logging.info("*" * 89)
        logging.info("###  test_02_update_site  ###")

        new_name = site_obj.create_random_site_name()
        site_payload = {"name": new_name}

        updated_site = site_obj._op_update_site(env, TestSiteAPI.site_id, site_payload)

        assert updated_site["name"] == new_name, (
            f"Expected site name '{new_name}', got '{updated_site['name']}'"
        )

    def test_03_delete_site(self, env):
        """
        Delete the Site and confirm it no longer appears in the org listing.
        """
        logging.info("*" * 89)
        logging.info("###  test_03_delete_site  ###")

        site_obj._op_delete_site(env, TestSiteAPI.site_id)

        assert not site_obj._is_site_present(env, TestSiteAPI.org_id, TestSiteAPI.site_id), \
            f"Site {TestSiteAPI.site_id} still present in org {TestSiteAPI.org_id} after deletion."