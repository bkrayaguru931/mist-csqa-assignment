# utils\api_utils\api_utils.py
"""API utility functions for CRUD operations."""
import requests
import json
from typing import Dict, Any, Optional, Tuple, Union
from config.settings import Config
import logging

class CommonAPIUtils:
    """Utility class for API operations."""

    def __init__(self):
        self.base_url = Config.BASE_URL
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json'
        }
        if Config.API_TOKEN:
            self.headers['Authorization'] = f'Token {Config.API_TOKEN}'

    def post(self, url, data):
        """
        Create a new resource via POST request.

        Args:
            endpoint: API endpoint (relative to base URL)
            data: Data to send in request body

        Returns:
            Tuple of (response_json, status_code)
        """
        try:
            response = self.session.post(
                url,
                data=json.dumps(data),
                headers=self.headers,
                timeout=Config.TIMEOUT
            )
            logging.info("POST %s completed - Status Code: %d", url, response.status_code)

            logging.info(response.json())
            # Handle different response types
            try:
                return response.json(), response.status_code
            except json.JSONDecodeError:
                return response.text, response.status_code

        except requests.exceptions.RequestException as e:
            logging.error("POST request failed for %s: %s", url, str(e))
            raise

    def post_request_with_status_code_validation(self, url, data, expected_status_code):
        """
        Perform POST request with status code validation.

        Args:
            url: API endpoint
            data: Request data
            expected_status_code: Expected HTTP status code

        Returns:
            Response data if successful

        Raises:
            Exception: If status code doesn't match expected value
        """
        try:
            response, status = self.post(url, data)
            if status == expected_status_code:
                logging.info("CommonAPIUtils():: POST Request executed successfully")
                return response
            else:
                raise Exception(
                    f'E: CommonAPIUtils() :: POST request failed. Expected status {expected_status_code}, got {status}')
        except Exception as e:
            logging.exception(e)
            raise AssertionError(f"Function {self.post_request_with_status_code_validation.__name__} has failed") from e

    def get(self, url):
        """
        Read resource via GET request.

        Args:
            endpoint: API endpoint (relative to base URL)
            params: Query parameters

        Returns:
            Tuple of (response_json, status_code)
        """
        try:
            response = self.session.get(
                url,
                headers=self.headers,
                timeout=Config.TIMEOUT
            )
            logging.info("GET %s completed - Status Code: %d", url, response.status_code)

            # Handle different response types
            try:
                return response.json(), response.status_code
            except json.JSONDecodeError:
                return response.text, response.status_code

        except requests.exceptions.RequestException as e:
            logging.error("GET request failed for %s: %s", url, str(e))
            raise

    def get_request_with_status_code_validation(self, url, expected_status_code):
        """
        Perform GET request with status code validation.

        Args:
            url: API endpoint
            expected_status_code: Expected HTTP status code
            return_json: Whether to return JSON (unused but kept for compatibility)

        Returns:
            Response data if successful

        Raises:
            Exception: If status code doesn't match expected value
        """
        try:
            response, status = self.get(url)
            if status == expected_status_code:
                logging.info("CommonAPIUtils():: GET Request executed successfully")
                return response
            else:
                raise Exception(
                    f'E: CommonAPIUtils() :: GET request failed. Expected status {expected_status_code}, got {status}')
        except Exception as e:
            logging.exception(e)
            raise AssertionError(f"Function {self.get_request_with_status_code_validation.__name__} has failed") from e

    def put(self, url, data):
        """
        Update resource via PUT request.

        Args:
            endpoint: API endpoint (relative to base URL)
            data: Data to send in request body

        Returns:
            Tuple of (response_json, status_code)
        """
        try:
            response = self.session.put(
                url,
                json=data,
                headers=self.headers,
                timeout=Config.TIMEOUT
            )
            logging.info("PUT %s completed - Status Code: %d", url, response.status_code)

            # Handle different response types
            try:
                return response.json(), response.status_code
            except json.JSONDecodeError:
                return response.text, response.status_code

        except requests.exceptions.RequestException as e:
            logging.error("PUT request failed for %s: %s", url, str(e))
            raise

    def put_request_with_status_code_validation(self, url, data, expected_status_code) :
        """
        Perform PUT request and validate status code.

        Args:
            url: API endpoint (relative to base URL)
            data: Data to send in request body
            expected_status_code: Expected HTTP status code

        Returns:
            Response JSON if status code matches

        Raises:
            Exception: If status code doesn't match expected value
        """
        try:
            response, status = self.put(url, data)
            if status == expected_status_code:
                logging.info("CommonAPIUtils():: PUT Request executed successfully")
                return response
            else:
                raise Exception(
                    f'E: CommonAPIUtils() :: PUT request failed. Expected status {expected_status_code}, got {status}')
        except Exception as e:
            logging.exception(e)
            raise AssertionError(f"Function {self.put_request_with_status_code_validation.__name__} has failed") from e

    def delete(self, url):
        """
        Delete resource via DELETE request.

        Args:
            endpoint: API endpoint (relative to base URL)

        Returns:
            Tuple of (response_json, status_code)
        """
        try:
            response = self.session.delete(
                url,
                headers=self.headers,
                timeout=Config.TIMEOUT
            )
            logging.info("DELETE %s completed - Status Code: %d", url, response.status_code)

            # Handle different response types
            try:
                return response.json(), response.status_code
            except json.JSONDecodeError:
                return response.text, response.status_code

        except requests.exceptions.RequestException as e:
            logging.error("DELETE request failed for %s: %s", url, str(e))
            raise

    def delete_request_with_status_code_validation(self, url, expected_status_code):
        """
        Perform DELETE request and validate status code.

        Args:
            url: API endpoint (relative to base URL)
            expected_status_code: Expected HTTP status code

        Returns:
            Response JSON if status code matches

        Raises:
            Exception: If status code doesn't match expected value
        """
        try:
            response, status = self.delete(url)
            if status == expected_status_code:
                logging.info("CommonAPIUtils():: DELETE Request executed successfully")
                return response
            else:
                raise Exception(
                    f'E: CommonAPIUtils() :: DELETE request failed. Expected status {expected_status_code}, got {status}')
        except Exception as e:
            logging.exception(e)
            raise AssertionError(f"Function {self.delete_request_with_status_code_validation.__name__} has failed") from e

    def patch(self, url, data):
        """
        Partially update resource via PATCH request.

        Args:
            endpoint: API endpoint (relative to base URL)
            data: Data to send in request body

        Returns:
            Tuple of (response_json, status_code)
        """
        logging.info("Making PATCH request to: %s", url)
        logging.debug("PATCH request data: %s", json.dumps(data, indent=2))
        try:
            response = self.session.patch(
                url,
                json=data,
                headers=self.headers,
                timeout=Config.TIMEOUT
            )
            logging.info("PATCH %s completed - Status Code: %d", url, response.status_code)

            # Handle different response types
            try:
                return response.json(), response.status_code
            except json.JSONDecodeError:
                return response.text, response.status_code

        except requests.exceptions.RequestException as e:
            logging.error("PATCH request failed for %s: %s", url, str(e))
            raise

    def patch_request_with_status_code_validation(self, url, data, expected_status_code):
        """
        Perform PATCH request and validate status code.

        Args:
            url: API endpoint (relative to base URL)
            data: Data to send in request body
            expected_status_code: Expected HTTP status code

        Returns:
            Response JSON if status code matches

        Raises:
            Exception: If status code doesn't match expected value
        """
        try:
            response, status = self.patch(url, data)
            if status == expected_status_code:
                logging.info("CommonAPIUtils():: PATCH Request executed successfully")
                return response
            else:
                raise Exception(
                    f'E: CommonAPIUtils() :: PATCH request failed. Expected status {expected_status_code}, got {status}')
        except Exception as e:
            logging.exception(e)
            raise AssertionError(f"Function {self.patch_request_with_status_code_validation.__name__} has failed") from e