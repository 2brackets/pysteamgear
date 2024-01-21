import json
from collections import OrderedDict
from itertools import chain
from urllib.parse import urlparse
from requests import Response
import xmltodict
import vdf
from ..helpers import get_extract_items_method

JSON = 'application/json'
XML = 'text/xml'
VDF = 'text/vdf'

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
        self.content_type = resp.headers.get('Content-Type')
        self.response_headers = dict(resp.headers)
        self.content = resp.text
        self.elapsed_time = resp.elapsed.total_seconds()
        self.cookies = resp.cookies.get_dict()
        self.requested_url = resp.url
        self.api = self.extract_last_path_segment(resp.url)
        self.title = None
        self.headers = None
        self.items = None
        self.count = None
        self._parse_data(resp=resp)

    @property
    def len_headers(self) -> int:
        return len(self.headers)

    @property
    def len_items(self) -> int:
        return len(self.items)

    @property
    def len_cookies(self) -> int:
        return len(self.cookies)

    def _parse_data(self, resp: Response):
        """
        Parses the provided HTTP response and sets the object attributes.

        Args:
            resp (Response): The response object from an HTTP request.
        """
        data_dict = self._convert_data_dict(resp)
        if isinstance(data_dict, dict):
            self.title = next(iter(data_dict.keys()), None)
            if isinstance(data_dict.get(self.title), dict):
                self.count = data_dict.get(self.title, {}).get('count', None)
            extract_items = get_extract_items_method(self.api)
            items = extract_items(data_dict[self.title])
        else:
            items = data_dict
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
        if JSON in self.content_type:
            return json.loads(resp.text)
        if XML in self.content_type:
            return xmltodict.parse(resp.text)
        if VDF in self.content_type:
            return vdf.loads(resp.text)
        raise ValueError(f'Unsupported content type: {self.content_type}')

    def _collect_headers(self, items: list) -> list:
        if not isinstance(items, list):
            items = [items]
        return list(OrderedDict.fromkeys(chain.from_iterable(item.keys() for item in items)))

    def _parse_items(self, items: list) -> list:
        if not isinstance(items, list):
            items = [items]
        return [{key: item.get(key) for key in self.headers} for item in items]

    def extract_last_path_segment(self, url: str) -> str:
        segments = [seg for seg in urlparse(url).path.split('/') if seg]
        if segments and segments[-1].startswith('v') and segments[-1][1:].isdigit():
            return segments[-2] if len(segments) > 1 else segments[-1]
        return segments[-1]
    