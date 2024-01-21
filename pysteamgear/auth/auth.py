from time import time
from base64 import b64encode
import requests
from requests import HTTPError, Session, Response
from .steam_id import SteamID
from ..core.crypto import rsa_public_key, pkcs1v15_encrypt
from ..utils.web import create_session, generate_session_id
from ..exceptions import AuthExceptions as ex

BAS_URL = 'https://steamcommunity.com/login'
DOMAIN = ['store.steampowered.com', 'help.steampowered.com', 'steamcommunity.com']

class Auth():
    def __init__(self,
        username:str,
        language:str,
        password:str=None,
        code_two_factor:str=None,
        captcha:str=None,
        code_email:str=None):

        self.username = username
        self.password = password
        self.steam_id = None
        self.key = None
        self.timestamp = None
        self.active = False
        self.session_id = None
        self.captcha = captcha
        self.captcha_gid = -1
        self.captcha_code = None
        self.code_two_factor = code_two_factor
        self.code_email = code_email
        self.language = language
        self.session: Session = create_session()

    @property
    def captcha_url(self):
        if self.captcha_gid == -1:
            return None
        return f'{BAS_URL}/rendercaptcha/?gid={self.captcha}'

    def login(self):
        if not self.active:
            if not self.password:
                raise ex.MissingPassword(f'Missing password: {self.password}')
            self._load_key()
            resp = self._request_login()
            if resp.get('success') and resp.get('login_complete'):
                self.active = True
                self.password = None
                self.captcha_gid = -1
                for cookie in list(self.session.cookies):
                    for domain in DOMAIN:
                        self.session.cookies.set(
                            cookie.name,
                            cookie.value,
                            domain=domain,
                            secure=cookie.secure)
                self.session_id = generate_session_id()
                for domain in DOMAIN:
                    self.session.cookies.set('Steam_Language', self.language, domain=domain)
                    self.session.cookies.set('birthtime', '-3333', domain=domain)
                    self.session.cookies.set('sessionid', self.session_id, domain=domain)
                login_resp = resp.get('transfer_parameters').get('steamid')
                if not login_resp:
                    raise ex.MissingSteamID(f'Missing Steam id: {self.steam_id}')
                self.steam_id = SteamID(login_resp)
            else:
                self._login_failed(resp=resp)

    def _rsa_key(self) -> Response:
        try:
            resp = self.session.post(
                url=f'{BAS_URL}/getrsakey/',
                timeout=15,
                data={
                    'username': self.username,
                    'donotcache': int(time() * 1000),
                },
            ).json()
        except requests.exceptions.RequestException as e:
            raise HTTPError(str(e)) from e
        return resp

    def _load_key(self):
        if not self.key:
            resp = self._rsa_key()
            self.key = rsa_public_key(
                int(resp['publickey_mod'], 16),
                int(resp['publickey_exp'], 16))
            self.timestamp = resp['timestamp']

    def _request_login(self) -> Response:
        data = {
            'username': self.username,
            "password": b64encode(pkcs1v15_encrypt(self.key, self.password.encode('ascii'))),
            "emailauth": self.code_email,
            "emailsteamid": str(self.steam_id) if self.code_email else None,
            "twofactorcode": self.code_two_factor,
            "captchagid": self.captcha_gid,
            "captcha_text": self.captcha,
            "loginfriendlyname": "python-steam webauth",
            "rsatimestamp": self.timestamp,
            "remember_login": 'true',
            "donotcache": int(time() * 100000),
        }

        try:
            return self.session.post(f'{BAS_URL}/dologin/', data=data, timeout=15).json()
        except requests.exceptions.RequestException as e:
            raise HTTPError(str(e)) from e

    def _login_failed(self, resp: Response):
        error_conditions = {
            'captcha_needed': (ex.CaptchaRequired, ex.CaptchaRequiredLoginIncorrect),
            'emailauth_needed': (ex.EmailCodeRequired, None),
            'requires_twofactor': (ex.TwoFactorCodeRequired, None),
            'too_many_failures': (ex.TooManyLoginFailures, None)
        }
        for condition, exceptions in error_conditions.items():
            if condition == 'too_many_failures':
                if 'too many login failures' in resp.get('message', ''):
                    raise exceptions[0](resp.get('message'))
            elif resp.get(condition, False):
                if condition == 'captcha_needed':
                    self.captcha_gid = resp.get('captcha_gid')
                    self.captcha_code = None
                    exception_class = exceptions[1] if resp.get(
                        'clear_password_field', False) else exceptions[0]
                    if exception_class is ex.CaptchaRequiredLoginIncorrect:
                        self.password = None
                elif condition == 'emailauth_needed':
                    self.steam_id = SteamID(resp.get('emailsteamid'))
                raise exceptions[0](resp.get('message'))
        self.password = None
        raise ex.LoginIncorrect(resp.get('message'))
