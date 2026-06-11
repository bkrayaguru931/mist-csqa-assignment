# TODO - Candidate to add Site API Libs when working on the assignment.
import logging
from datetime import datetime
from libs.api_libs.constants import api_constants
from libs.api_libs.org_api_libs import OrgAPILibs
from utils.api_utils.api_utils import CommonAPIUtils
import os
import json


class GenericSiteLibs(object):
    """Class that holds the Generic (non-HTTP) helper functions for Site operations."""

    def create_random_site_name(self):
        """Return a unique Site name based on the current timestamp (minute precision)."""
        return "Automation Site " + str(datetime.now())[0:16]

    def get_sample_site_config(self):
        """Load the default site payload from the bundled JSON fixture file."""
        site_config_file = os.path.abspath(__file__ + "/../") + "/configs/sample_site_config.json"
        with open(site_config_file) as site_default_payload:
            data = json.load(site_default_payload)
        return data


class SiteAPILibs(GenericSiteLibs):
    """
    Wrap the Mist Sites REST API and validate the parent Org before CRUD actions.

    Endpoint reference:
        POST   /api/v1/orgs/{org_id}/sites          - create
        GET    /api/v1/sites/{site_id}               - read
        PUT    /api/v1/sites/{site_id}               - update
        DELETE /api/v1/sites/{site_id}               - delete
        GET    /api/v1/orgs/{org_id}/sites           - list (used for existence check)
    """

    def _ensure_org_exists(self, env, org_id):
        """
        Validate that the parent Org exists before performing Site CRUD operations.

        Returns:
            bool: True when the Org exists.

        Raises:
            AssertionError: If the Org ID is missing or the Org does not exist.
        """
        if not org_id:
            raise AssertionError("Org ID is required for Site CRUD operations.")

        org_client = OrgAPILibs()
        if not org_client._is_org_present(env, org_id):
            raise AssertionError(f"Org {org_id} does not exist for environment '{env}'.")
        return True

    def _validate_site_belongs_to_org(self, env, org_id, site_id):
        """
        Validate that the given site belongs to the provided org.

        Raises:
            AssertionError: If the site is not associated with the org.
        """
        self._ensure_org_exists(env, org_id)
        #https://api.ac2.mist.com/api/v1/orgs/123/sites
        url = (
            api_constants.CONST_EXT_API_URLs[env]                            
            + api_constants.CONST_API_ORG_SITES.format(org_id)
        )

        sites = CommonAPIUtils().get_request_with_status_code_validation(url, 200)

        site_ids = {site["id"] for site in sites}

        if site_id not in site_ids:
            raise AssertionError(
                f"Site {site_id} does not belong to Org {org_id}"
            )

        return True

    def __init__(self):
        """Initialize the Site API helper."""
        pass


    # CRUD operations


    def _op_create_site(self, env, org_id, site_payload=None):
        """
        Create a new Site under *org_id*.

        If *site_payload* is provided it is merged on top of the default
        fixture; otherwise a random name is generated automatically.
        """
        logging.info("%s :: %s :: Creating a new Site",
                     self.__class__.__name__, "_op_create_site")

        self._ensure_org_exists(env, org_id)

        url = api_constants.CONST_EXT_API_URLs[env] + \
              api_constants.CONST_API_ORG_SITES.format(org_id)  #https://api.ac2.mist.com/api/v1/orgs/123/sites

        payload = self.get_sample_site_config()
        if site_payload is not None:
            payload.update(site_payload)
        else:
            payload["name"] = self.create_random_site_name()

        payload = dict(payload)

        logging.info("%s :: %s :: Site name → %s",
                     self.__class__.__name__, "_op_create_site", payload["name"])

        response = CommonAPIUtils().post_request_with_status_code_validation(url, payload, 200)

        logging.info("%s :: %s :: Site created successfully",
                     self.__class__.__name__, "_op_create_site")
        return response

    def _get_site_details(self, env, org_id, site_id):
        """
        Fetch the full detail record for a single Site.

        Returns the parsed JSON response body (dict).
        """
        logging.info("%s :: %s :: Fetching details for site_id=%s",
                     self.__class__.__name__, "_get_site_details", site_id)

        self._validate_site_belongs_to_org(env, org_id, site_id=site_id)

        url = api_constants.CONST_EXT_API_URLs[env] + \
              api_constants.CONST_API_SITE_DETAILS.format(site_id)

        return CommonAPIUtils().get_request_with_status_code_validation(url, 200)

    def _op_update_site(self, env, org_id, site_id, site_payload):
        """
        Apply a partial update to an existing Site via HTTP PUT.
        """
        logging.info("%s :: %s :: Updating site_id=%s",
                     self.__class__.__name__, "_op_update_site", site_id)

        self._validate_site_belongs_to_org(env, org_id, site_id)

        url = api_constants.CONST_EXT_API_URLs[env] + \
              api_constants.CONST_API_SITE_DETAILS.format(site_id)

        response = CommonAPIUtils().put_request_with_status_code_validation(url, site_payload, 200)

        logging.info("%s :: %s :: Site updated successfully",
                     self.__class__.__name__, "_op_update_site")
        return response

    def _op_delete_site(self, env, org_id, site_id):
        """
        Permanently delete a Site by its ID.

        Returns nothing; raises on non-200 HTTP status (handled by
        CommonAPIUtils).
        """
        logging.info("%s :: %s :: Deleting site_id=%s",
                     self.__class__.__name__, "_op_delete_site", site_id)

        self._validate_site_belongs_to_org(env, org_id, site_id)

        url = api_constants.CONST_EXT_API_URLs[env] + \
              api_constants.CONST_API_SITE_DETAILS.format(site_id)

        CommonAPIUtils().delete_request_with_status_code_validation(url, 200)

        logging.info("%s :: %s :: Site deleted successfully",
                     self.__class__.__name__, "_op_delete_site")

    # Existence helper

    def _get_all_sites(self, env, org_id):
        """
        Return all sites belonging to the specified Org.
        """

        logging.info(
            "%s :: %s :: Getting all sites for org_id=%s",
            self.__class__.__name__,
            "_get_all_sites",
            org_id
        )

        self._ensure_org_exists(env, org_id)

        url = (
            api_constants.CONST_EXT_API_URLs[env]
            + api_constants.CONST_API_ORG_SITES.format(org_id)
        )

        return CommonAPIUtils().get_request_with_status_code_validation(
            url,
            200
        )

    def _is_site_present(self, env, org_id, site_id):
        """
        Return True if site_id appears in the org-level site listing.
        """
        logging.info("%s :: %s :: Checking presence of site_id=%s in org_id=%s",
                     self.__class__.__name__, "_is_site_present", site_id, org_id)

        if not self._ensure_org_exists(env, org_id):
            return False

        url = api_constants.CONST_EXT_API_URLs[env] + \
              api_constants.CONST_API_ORG_SITES.format(org_id)

        sites = CommonAPIUtils().get_request_with_status_code_validation(url, 200)
        present = site_id in {site["id"] for site in sites}

        logging.info("%s :: %s :: site present=%s",
                     self.__class__.__name__, "_is_site_present", present)
        return present