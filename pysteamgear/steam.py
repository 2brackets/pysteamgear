#FORMATS = ['json', 'xml', 'vdf']
FORMATS = {
    'json': 'application/json',
    'xml': 'application/xml', 
    'vdf': 'text/plain'}

class Steam():

    def __init__(self,
            web_api_key: str,
            preferred_output_format: str ='json',
            language: str ='english',
            username: str =None,
            steam_id: str =None,
            time_out: int = 300):

        self._validate_format(preferred_output_format)

        self.key = web_api_key
        self.username = username
        self.format = preferred_output_format
        self.language = language
        self.auth = username
        self.id = steam_id
        self.timeout = time_out

    def _validate_format(self, output_format: str):
        if output_format not in FORMATS:
            raise ValueError(
                f"Invalid format: {output_format}. Valid formats are: {FORMATS}")
    @property
    def headers_format(self) -> str:
        return FORMATS.get(self.format)
 