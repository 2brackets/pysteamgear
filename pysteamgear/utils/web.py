from binascii import hexlify
from os import urandom
import requests
from requests import Session
from ..core.crypto import sha1_hash

def create_session() -> Session:
    session = requests.Session()
    version = __import__('pysteamgear').__version__
    user_agent = f'python-steam/{version} {session.headers.get("User-Agent")}'
    session.headers['User-Agent'] = user_agent
    return session

def generate_session_id() -> bytes:
    return hexlify(sha1_hash(urandom(32)))[:32].decode('ascii')
