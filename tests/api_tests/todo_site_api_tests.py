# TODO - Candidate to add Site API Tests when working on the assignment.

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

    """

    #Stores the Org ID that will be created for this test class.
    org_id: str = ""
    #Stores the Site ID created in test_01_create_site for use in later tests.
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

        yield  # all test methods run here

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
        Update the Site name and verify:
        1. Site name is updated.
        2. Site count remains unchanged.
        3. Updated site can be retrieved from API.
        """
        logging.info("*" * 89)
        logging.info("### test_02_update_site ###")

        # Get site count before update
        sites_before = site_obj._get_all_sites(
            env,
            TestSiteAPI.org_id
        )
        before_count = len(sites_before)

        logging.info(
            "Site count before update = %s",
            before_count
        )

        # Generate new site name
        new_name = site_obj.create_random_site_name()

        site_payload = {
            "name": new_name
        }

        # Update site
        updated_site = site_obj._op_update_site(
            env,
            TestSiteAPI.org_id,
            TestSiteAPI.site_id,
            site_payload
        )

        # Validate API response
        assert updated_site["name"] == new_name, (
            f"Expected site name '{new_name}', "
            f"but got '{updated_site['name']}'"
        )

        # Fetch site details again from API
        site_details = site_obj._get_site_details(
            env,
            TestSiteAPI.org_id,
            TestSiteAPI.site_id
        )

        assert site_details["name"] == new_name, (
            f"GET verification failed. "
            f"Expected '{new_name}', "
            f"got '{site_details['name']}'"
        )

        # Get site count after update
        sites_after = site_obj._get_all_sites(
            env,
            TestSiteAPI.org_id
        )

        after_count = len(sites_after)

        logging.info(
            "Site count after update = %s",
            after_count
        )

        # Ensure update did not create/delete sites
        assert before_count == after_count, (
            f"Site count changed after update. "
            f"Before={before_count}, After={after_count}"
        )

        logging.info(
            "Site updated successfully. "
            f"Name={new_name}, "
            f"Count Before={before_count}, "
            f"Count After={after_count}"
        )

    def test_03_get_site_details(self, env):

        site_details = site_obj._get_site_details(
            env,
            TestSiteAPI.org_id,
            TestSiteAPI.site_id
        )

        assert site_details["id"] == TestSiteAPI.site_id

    def test_04_create_site_with_invalid_org_fails(self, env):
        """
        Negative test: creation must fail when the parent Org is invalid.
        """
        with pytest.raises((AssertionError, Exception)):
            site_obj._op_create_site(env, "invalid-org-id-for-negative-test")

    def test_05_update_site_with_invalid_org_fails(self, env):
        """
        Negative test: update must fail when the parent Org is invalid.
        """
        with pytest.raises((AssertionError, Exception)):
            site_obj._op_update_site(env, "invalid-org-id-for-negative-test", "fake-site-id", {"name": "Should Fail"})

    def test_06_delete_site_with_invalid_org_fails(self, env):
        """
        Negative test: delete must fail when the parent Org is invalid.
        """
        with pytest.raises((AssertionError, Exception)):
            site_obj._op_delete_site(env, "invalid-org-id-for-negative-test", "fake-site-id")

    def test_07_update_site_with_wrong_org_fails(self, env):
        """
        Negative test:
        Site should not be updated through a different org.
        """

        # Create another org
        second_org = org_obj._op_create_org(env)
        second_org_id = second_org["id"]

        try:
            with pytest.raises(AssertionError):
                site_obj._op_update_site(
                    env,
                    second_org_id,          # wrong org
                    TestSiteAPI.site_id,    # site belongs to original org
                    {"name": "Invalid Update"}
                )

        finally:
            org_obj._op_delete_org(env, second_org_id)

    def test_08_delete_site_with_wrong_org_fails(self, env):
        """
        Negative test:
        Site should not be deleted through a different org.
        """

        second_org = org_obj._op_create_org(env)
        second_org_id = second_org["id"]

        try:
            with pytest.raises(AssertionError):
                site_obj._op_delete_site(
                    env,
                    second_org_id,
                    TestSiteAPI.site_id
                )

        finally:
            org_obj._op_delete_org(env, second_org_id)
    
    def test_09_delete_site(self, env):
        """
        Delete the Site and confirm it no longer appears in the org listing.
        """
        logging.info("*" * 89)
        logging.info("###  test_09_delete_site  ###")

        site_obj._op_delete_site(env, TestSiteAPI.org_id, TestSiteAPI.site_id)

        assert not site_obj._is_site_present(env, TestSiteAPI.org_id, TestSiteAPI.site_id), \
            f"Site {TestSiteAPI.site_id} still present in org {TestSiteAPI.org_id} after deletion."
