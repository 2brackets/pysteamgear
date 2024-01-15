import json
from collections import OrderedDict
from itertools import chain
from requests import Response
import xmltodict
import vdf

JSON = 'application/json'
XML = 'text/xml'
VDF = 'text/vdf'

ID_NEWS_ITEMS = 'newsitems'

class SteamData():
    """
    A class to parse and store data from a Steam Web API response.

    Attributes:
        status_code (int): The HTTP status code of the response.
        response_headers (dict): The headers from the HTTP response.
        content (str): The text content of the HTTP response.
        elapsed_time (float): The total time elapsed during the request, in seconds.
        cookies (dict): The cookies from the HTTP response.
        title (str): The main title of the parsed data.
        headers (list): The list of headers from the parsed items.
        items (list): The parsed items from the response.
        count (int): The count of items in the response.
    """
    def __init__(self, resp: Response) -> None:
        """
        Initializes the SteamData object with the provided HTTP response.

        Args:
            resp (Response): The response object from an HTTP request.
        """
        self.status_code = resp.status_code
        self.response_headers = dict(resp.headers)
        self.content = resp.text
        self.elapsed_time = resp.elapsed.total_seconds()
        self.cookies = resp.cookies.get_dict()
        self.title = None
        self.headers = None
        self.items = None
        self.count = None
        self._parse_data(resp=resp)

    def _parse_data(self, resp: Response):
        """
        Parses the provided HTTP response and sets the object attributes.

        Args:
            resp (Response): The response object from an HTTP request.
        """
        data_dict = self._convert_data_dict(resp)
        self.title = next(iter(data_dict.keys()), None)
        self.count = data_dict.get(self.title, {}).get('count')
        items = data_dict.get(self.title, {}).get(ID_NEWS_ITEMS, [])
        self.headers = self._collect_headers(items)
        self.items = self._parse_items(items)

    def _convert_data_dict(self, resp: Response) -> dict:
        """
        Converts the HTTP response content to a dictionary.

        Args:
            resp (Response): The response object from an HTTP request.

        Returns:
            dict: The response content converted to a dictionary.

        Raises:
            ValueError: If the response content type is unsupported.
        """
        content_type = resp.headers.get('Content-Type')
        if JSON in content_type:
            return json.loads(resp.text)
        if XML in content_type:
            return xmltodict.parse(resp.text)
        if VDF in content_type:
            return vdf.loads(resp.text)
        raise ValueError(f'Unsupported content type: {content_type}')

    def _collect_headers(self, items: list) -> list:
        """
        Collects and returns a list of unique headers from the provided items.

        Args:
            items (list): A list of dictionaries representing items in the response.

        Returns:
            list: A list of unique headers found in the items.
        """
        return list(OrderedDict.fromkeys(chain.from_iterable(item.keys() for item in items)))

    def _parse_items(self, items: list) -> list:
        """
        Parses the provided items and returns a list of dictionaries.

        Args:
            items (list): A list of dictionaries representing items in the response.

        Returns:
            list: A list of dictionaries with keys corresponding to self.headers.
        """
        return [{key: item.get(key) for key in self.headers} for item in items]
