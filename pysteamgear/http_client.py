import requests
from requests.exceptions import Timeout, RequestException
from .modules import SteamData

class HttpClient():
    """
    HttpClient class to handle HTTP GET requests.
    """
    @staticmethod
    def get(url:str, params:dict, timeout:int, headers:dict=None) -> SteamData:
        """
        Perform an HTTP GET request.

        Args:
            url (str): The URL to which the request is sent.
            params (dict): The parameters to be sent in the query string of the request.
            timeout (int): The number of seconds to wait for a response from the server.
            headers (dict, optional): A dictionary of HTTP headers to send with the request.

        Returns:
            SteamData: An instance of SteamData containing the response data.

        Raises:
            Timeout: If the request times out.
            ConnectionError: If a connection error occurs.
            RequestException: For other types of request-related exceptions.
        """
        try:
            resp = requests.get(
                url=url,
                headers=headers,
                params=params,
                timeout=timeout
            )
            resp.raise_for_status()
            return SteamData(resp=resp)
        except Timeout as exc:
            raise Timeout(f'Request to {url} timed out.') from exc
        except ConnectionError as exc:
            raise ConnectionError(f'Connection error occurred while requesting {url}.') from exc
        except RequestException as exc:
            raise RequestException(f'An error occurred while requesting {url}: {exc}') from exc
    