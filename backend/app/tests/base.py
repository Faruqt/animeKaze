"""
base.py : This module contains a base test case class that provides helper methods for making requests and asserting responses.
"""

import os


class BaseTestCase:
    response = None
    client = None
    payload = {}
    url = None

    def assert_status_code(self, status_code):
        """
        Assert that the response status code matches the specified value.
        """
        assert self.response, "Response is None. Make a request first."
        assert (
            self.response.status_code == status_code
        ), f"Expected status code {status_code}, but got {self.response.status_code}"

    def assert_in_api_response(self, *args):
        """
        Assert that the response contains the specified values.
        """
        assert self.response, "Response is None. Make a request first."
        data = self.response.json

        for value in args:
            assert value in data, f"{value} not found in response"

    def assert_in_html_response(self, *args):
        """
        Assert that the response contains the specified HTML elements.
        """
        assert self.response, "Response is None. Make a request first."
        data = self.response.data.decode("utf-8").lower()

        for element in args:
            assert element.lower() in data, f"{element} not found in response"

    def assert_not_in_html_response(self, *args):
        """
        Assert that the response does not contain the specified HTML elements.
        """
        assert self.response, "Response is None. Make a request first."
        data = self.response.data.decode("utf-8").lower()

        for element in args:
            assert element.lower() not in data, f"{element} found in response"

    def assert_equal(self, first, second, error_message=None):
        """
        Assert that the two values are equal.
        """
        assert first == second, error_message or f"{first} not equal to {second}"

    def assert_in_list(self, value, lst, error_message=None):
        """
        Assert that the value is present in the list.
        """
        assert value in lst, error_message or f"{value} not in list"

    def assert_not_in_list(self, value, lst, error_message=None):
        """
        Assert that the value is not present in the list.
        """
        assert value not in lst, error_message or f"{value} in list"

    def assert_not_equal(self, first, second, error_message=None):
        """
        Assert that the two values are not equal.
        """
        assert first != second, error_message or f"{first} equal to {second}"

    def assert_less_than(self, first, second, error_message=None):
        """
        Assert that the first value is less than the second value.
        """
        assert first < second, error_message or f"{first} not less than {second}"

    def make_get_request(self):
        """
        Make a GET request to the specified URL.
        """
        assert self.client, "Client is None. Initialize the client first."
        assert self.url, "URL is None. Set the URL first."

        self.response = self.client.get(self.url)

    def make_post_request(self):
        """
        Make a POST request to the specified URL.
        """
        assert self.client, "Client is None. Initialize the client first."
        assert self.url, "URL is None. Set the URL first."

        self.response = self.client.post(self.url, data=self.payload)
