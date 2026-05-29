import logging
from datetime import datetime
from libs.api_libs.constants import api_constants
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
    Class that wraps the Mist Sites REST API.

    Endpoint reference:
        POST   /api/v1/orgs/{org_id}/sites          - create
        GET    /api/v1/sites/{site_id}               - read
        PUT    /api/v1/sites/{site_id}               - update
        DELETE /api/v1/sites/{site_id}               - delete
        GET    /api/v1/orgs/{org_id}/sites           - list (used for existence check)
    """

    def __init__(self):
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

        url = api_constants.CONST_EXT_API_URLs[env] + \
              api_constants.CONST_API_ORG_SITES.format(org_id)

        payload = self.get_sample_site_config()
        if site_payload is not None:
            payload.update(site_payload)
        else:
            payload["name"] = self.create_random_site_name()

        logging.info("%s :: %s :: Site name → %s",
                     self.__class__.__name__, "_op_create_site", payload["name"])

        response = CommonAPIUtils().post_request_with_status_code_validation(url, payload, 200)

        logging.info("%s :: %s :: Site created successfully",
                     self.__class__.__name__, "_op_create_site")
        return response

    def _get_site_details(self, env, site_id):
        """
        Fetch the full detail record for a single Site.

        Returns the parsed JSON response body (dict).
        """
        logging.info("%s :: %s :: Fetching details for site_id=%s",
                     self.__class__.__name__, "_get_site_details", site_id)

        url = api_constants.CONST_EXT_API_URLs[env] + \
              api_constants.CONST_API_SITE_DETAILS.format(site_id)

        return CommonAPIUtils().get_request_with_status_code_validation(url, 200)

    def _op_update_site(self, env, site_id, site_payload):
        """
        Apply a partial update to an existing Site via HTTP PUT.
        """
        logging.info("%s :: %s :: Updating site_id=%s",
                     self.__class__.__name__, "_op_update_site", site_id)

        url = api_constants.CONST_EXT_API_URLs[env] + \
              api_constants.CONST_API_SITE_DETAILS.format(site_id)

        response = CommonAPIUtils().put_request_with_status_code_validation(url, site_payload, 200)

        logging.info("%s :: %s :: Site updated successfully",
                     self.__class__.__name__, "_op_update_site")
        return response

    def _op_delete_site(self, env, site_id):
        """
        Permanently delete a Site by its ID.

        Returns nothing; raises on non-200 HTTP status (handled by
        CommonAPIUtils).
        """
        logging.info("%s :: %s :: Deleting site_id=%s",
                     self.__class__.__name__, "_op_delete_site", site_id)

        url = api_constants.CONST_EXT_API_URLs[env] + \
              api_constants.CONST_API_SITE_DETAILS.format(site_id)

        CommonAPIUtils().delete_request_with_status_code_validation(url, 200)

        logging.info("%s :: %s :: Site deleted successfully",
                     self.__class__.__name__, "_op_delete_site")

    # Existence helper

    def _is_site_present(self, env, org_id, site_id):
        """
        Return True if site_id appears in the org-level site listing.
        """
        logging.info("%s :: %s :: Checking presence of site_id=%s in org_id=%s",
                     self.__class__.__name__, "_is_site_present", site_id, org_id)

        url = api_constants.CONST_EXT_API_URLs[env] + \
              api_constants.CONST_API_ORG_SITES.format(org_id)

        sites = CommonAPIUtils().get_request_with_status_code_validation(url, 200)
        present = site_id in {site["id"] for site in sites}

        logging.info("%s :: %s :: site present=%s",
                     self.__class__.__name__, "_is_site_present", present)
        return present