"""Authentication flow to authenticate a user with the spotify API."""
#  Copyright (c) 2025.

import base64
import json
import enums
import hashlib
import os
import re
import webbrowser
import requests
from urllib.parse import urlparse, parse_qsl
from http.server import BaseHTTPRequestHandler, HTTPServer


def create_enums():
    r"""Creates the enums for the program instance based on the resources.json"""
    with open('../Resource.json', 'r') as f:
        data = json.load(f)
        enums.clientId = data["Betterfy"]["creds"]["id"]
        enums.redirectAdr = ("127.0.0.1", 8000)
        enums.redirectUri = data["Betterfy"]["creds"]["redirect"]
        enums.tokenUrl = data["Betterfy"]["creds"]["tokenUrl"]
        enums.scope = data["Betterfy"]["creds"]["scopes"]
        enums.grant = data["Betterfy"]["creds"]["grant"]
        enums.refreshGrant = data["Betterfy"]["creds"]["refreshGrant"]
        # enums.headers = data["Betterfy"]["creds"]["headers"]
        enums.authUrl = data["Betterfy"]["creds"]["authUrl"]


def gen_verifier():
    r"""Generates a random alphanumeric string which can be used for the code challenge

            :returns: Random alphanumeric string.
            """
    verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    verifier = re.sub('[^a-zA-Z0-9]+', '', verifier)
    enums.codeVerifier = verifier
    return verifier


def gen_challenge():
    r"""Hash a code verifier with SHA256 and encode the result in URL-safe base64

                :returns: String with the challenge code.
                """
    challenge = hashlib.sha256(enums.codeVerifier.encode('utf-8')).digest()
    challenge = base64.urlsafe_b64encode(challenge).decode('utf-8')
    challenge = challenge.replace('=', '')
    enums.codeChallenge = challenge
    return challenge


def get_code():
    r"""Gets the auth code from Spotify's API"""
    httpd = HTTPServer(enums.redirectAdr, RequestHandlerGet)
    webbrowser.open(
        f"{enums.authUrl}"
        f"?response_type=code"
        f"&client_id={enums.clientId}"
        f"&scope={enums.scope}"
        f"&code_challenge_method=S256"
        f"&code_challenge={enums.codeChallenge}"
        f"&redirect_uri={enums.redirectUri}",
        new=0, autoraise=False)
    httpd.handle_request()


class RequestHandlerGet(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.auth_code = None
        try:
            self.server.auth_code = parse_auth_response_url(self.path)
            enums.authCode = self.server.auth_code
        except:
            print("oh no")

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self._write(f"""<html><script type="text/javascript">window.open('','_self').close();</script></html>""")
        return self.server.auth_code

    def _write(self, text):
        return self.wfile.write(text.encode("utf-8"))


def parse_auth_response_url(url):
    r"""Parses the url for a valid auth code

                    :returns: String with valid auth code.
                    """
    query_s = urlparse(url).query
    form = dict(parse_qsl(query_s))
    if form.__contains__("code"):
        return form.get("code")
    else:
        print("Error: User denied access")
        return form.get("error")


def get_token():
    r"""Gets valid user token from Spotify's API and stores it inside the enums"""
    body = (
        f"&client_id={enums.clientId}"
        f"&grant_type={enums.grant}"
        f"&code={enums.authCode}"
        f"&redirect_uri={enums.redirectUri}"
        f"&code_verifier={enums.codeVerifier}")
    response = requests.post(url=enums.tokenUrl, headers=enums.headers, data=body)
    enums.token_resp = parse_response(response.content)


def refresh_token():
    r"""Refreshes a previously valid user token via the Spotify API and stores the new token in the enums"""
    body = (
        f"&grant_type={enums.refreshGrant}"
        f"&refresh_token={enums.refresh_token}"
        f"&client_id={enums.clientId}")
    response = requests.post(url=enums.tokenUrl, headers=enums.headers, data=body)
    enums.token_resp = parse_response(response.content)


def parse_response(resp):
    r"""Parses a response from Spotify's API for specific data and stores it as JSON

                    :returns: A JSON object containing the response data (User Token, Token_Type, User Refresh Token, Scope).
                    """
    data = str(resp).split(",")
    token = data[0].removeprefix("b'{\"access_token\":\"").removesuffix('"')
    token_type = data[1].removeprefix("\"token_type\":\"").removesuffix('"')
    refresh_token = data[3].removeprefix("\"refresh_token\":\"").removesuffix('"')
    scope = data[4].removeprefix("\"scope\":\"").removesuffix('"}\'')
    resp_json = (token, token_type, refresh_token, scope)
    return resp_json


def cache_token(token):
    r"""Caches the user tokens in a .txt file"""
    try:
        os.remove("../cache.txt")
    except FileNotFoundError as Error:
        print(f"Initial creation of cache.txt | Error: {Error}")
    with open('../cache.txt', 'w') as f:
        f.write(
            f'{token}')
        f.close()
    return


def initial_authflow():
    r"""If it's the first login of the user on this machine, initiate the authflow"""
    gen_verifier()
    gen_challenge()
    get_code()
    get_token()


def auth():
    r"""Authenticates the user with the Spotify API

            :returns: A valid user token for the Spotify API.
            """
    create_enums()
    try:
        with open('../cache.txt', 'r') as f:
            enums.refresh_token = f.read()
        refresh_token()
    except FileNotFoundError:
        initial_authflow()
    cache_token(enums.token_resp[2])
    return enums.token_resp[0]
