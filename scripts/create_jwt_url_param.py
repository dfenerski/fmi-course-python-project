#! ./.venv/bin/python3

import os
from dotenv import load_dotenv
from requests import PreparedRequest
from jwt import encode

load_dotenv()

revolut_client_id = os.getenv('REVOLUT_CLIENT_ID')
revolut_redirect_url = os.getenv('REVOLUT_REDIRECT_URL')
revolut_kid = os.getenv('REVOLUT_KID')
revolut_sandbox_url = os.getenv('REVOLUT_SANDBOX_URL')

assert revolut_client_id
assert revolut_redirect_url
assert revolut_kid
assert revolut_sandbox_url

private_key = None
private_key_location = f"{os.getcwd()}/cert/private.key"

with open(private_key_location) as file_private_key:
    private_key = file_private_key.read()

assert private_key


access_scope = 'accounts'
response_type = 'code id_token'

jwt_headers = {
    "alg": "PS256",
    "kid": revolut_kid
}

jwt_body = {
    "response_type": response_type,
    "client_id": revolut_client_id,
    "redirect_uri": revolut_redirect_url,
    "scope": access_scope,
    # "state": "<insert state>", # this value is returned after redirect, allows app state to be regenerated
    "claims": {
        "id_token": {
            "openbanking_intent_id": {
                "value": "4e1e72f5-4796-43e0-9539-de6c1a8f14d2"
            }
        }
    }
}

jwt = encode(
    jwt_body,
    private_key,
    headers=jwt_headers
)

req = PreparedRequest()

req.prepare_url(f"{revolut_sandbox_url}/ui/index.html", {
    'response_type': response_type,
    'scope': access_scope,
    'redirect_uri': revolut_redirect_url,
    'client_id': revolut_client_id,
    'request': jwt
})

print("Confirm app access consent:")
print(req.url)
