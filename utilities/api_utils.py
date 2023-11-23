import requests

from utilities.custom_logger import LogGen


class APIUtility:
    """
    A utility class for making API requests.

    This class provides methods to set headers and body for API requests
    and includes methods to make GET and POST requests to specified URLs.

    Usage:
    api_util = APIUtility()
    api_util.set_headers(headers)
    api_util.set_body(body)
    response = api_util.get_request(url)
    response = api_util.post_request(url, use_json=True)

    Author:
        Gaurav Purwar

    Date:
        08 August 2023

    """
    logger = LogGen.loggen()

    def __init__(self):
        self.headers = {}
        self.body = {}

    def set_headers(self, headers: dict):
        self.headers = headers

    def set_body(self, body: dict):
        self.body = body

    def post_request(self, url: str, use_json: bool = False) -> dict:
        """
        Make a POST request to the specified URL.

        :param url: The URL to which the request should be made.
        :param use_json: if True, send the data as JSON in the request body
        :return: A dictionary containing the response JSON.
        """
        response = requests.post(url, json=self.body if use_json else None, data=self.body if not use_json else None,
                                 headers=self.headers)
        response_json = response.json()
        self.logger.info("[POST] API Response: " + str(response_json))
        return response_json

    def get_request(self, url: str) -> dict:
        """
        Make a GET request to the specified URL.

        :param url: The URL to which the request should be made.
        :return: A dictionary containing the response JSON.
        """
        response = requests.get(url, headers=self.headers)
        response_json = response.json()
        self.logger.info("[GET] API Response: " + str(response_json))
        return response_json
