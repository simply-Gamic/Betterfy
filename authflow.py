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
    with open('Resource.json', 'r') as f:
        data = json.load(f)
        enums.clientId = data["Betterfy"]["creds"]["id"]
        enums.redirectAdr = ("127.0.0.1", 8000)
        enums.redirectUri = data["Betterfy"]["creds"]["redirect"]
        enums.tokenUrl = data["Betterfy"]["creds"]["tokenUrl"]
        enums.scope = data["Betterfy"]["creds"]["scopes"]
        enums.grant = data["Betterfy"]["creds"]["grant"]
        #enums.headers = data["Betterfy"]["creds"]["headers"]
        enums.authUrl = data["Betterfy"]["creds"]["authUrl"]


def gen_verifier():
    verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    verifier = re.sub('[^a-zA-Z0-9]+', '', verifier)
    enums.codeVerifier = verifier
    return verifier


def gen_challenge():
    challenge = hashlib.sha256(enums.codeVerifier.encode('utf-8')).digest()
    challenge = base64.urlsafe_b64encode(challenge).decode('utf-8')
    challenge = challenge.replace('=', '')
    enums.codeChallenge = challenge
    return challenge


def get_code():
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
    query_s = urlparse(url).query
    form = dict(parse_qsl(query_s))
    if form.__contains__("code"):
        return form.get("code")
    else:
        print("Error: User denied access")
        return form.get("error")


def get_token():
    body = (
        f"&client_id={enums.clientId}"
        f"&grant_type={enums.grant}"
        f"&code={enums.authCode}"
        f"&redirect_uri={enums.redirectUri}"
        f"&code_verifier={enums.codeVerifier}")
    response = requests.post(url=enums.tokenUrl, headers=enums.headers, data=body)
    enums.token_resp = parse_response(response.content)


def parse_response(resp):
    data = str(resp).split(",")
    token = data[0].removeprefix("b'{\"access_token\":\"").removesuffix('"')
    token_type = data[1].removeprefix("\"token_type\":\"").removesuffix('"')
    refresh_token = data[3].removeprefix("\"refresh_token\":\"").removesuffix('"')
    scope = data[4].removeprefix("\"scope\":\"").removesuffix('"}\'')
    resp_json = (token, token_type, refresh_token, scope)
    return resp_json


def auth():
    create_enums()
    gen_verifier()
    gen_challenge()
    get_code()
    get_token()
    return enums.token_resp[0]
