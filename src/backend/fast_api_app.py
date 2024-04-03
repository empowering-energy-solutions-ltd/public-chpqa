import os
from typing import Annotated

import uvicorn
from auth0.authentication import GetToken
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Security
from fastapi.security import HTTPBearer

from src.backend.verification import VerifyToken

load_dotenv()
# Scheme for the Authorization header
token_auth_scheme = HTTPBearer()

# Creates app instance
app = FastAPI()
auth = VerifyToken()

# @app.get("/")
# def public():
#   """No access token required to access this route"""

#   result = {
#       "status": "success",
#       "msg": ("Welcome to our FastAPI authentication app.")
#   }
#   return result


def retrieve_token() -> GetToken:
  """ Enables requests to the /oauth/token endpoint to retrieve a token.
  
  Returns:
      GetToken: A auth0 GetToken object."""
  token = GetToken(os.getenv('AUTH0_DOMAIN_QUOTED'),
                   os.getenv('AUTH0_CLIENT_ID'),
                   client_secret=os.getenv('AUTH0_CLIENT_SECRET'))

  return token


@app.get("/streamlit/login")
def login(username: str, password: str) -> str:
  """ Uses Auth0 to verify the user's credentials and return a short-term access token.
  
  Args:
      username (str): The user's email.  
      password (str): The user's password.  
    
  Returns:
      str: A short-term access token."""
  try:
    token = retrieve_token()
    get_token = token.login(username=username,
                            password=password,
                            realm='Username-Password-Authentication',
                            audience=os.getenv('AUTH0_API_AUDIENCE'))
    return get_token['access_token']
  except Exception as e:
    return str(e)


async def check_permission(
    auth_result: Annotated[str, Security(auth.verify, scopes=[])]) -> str:
  """This function checks if the user has the required permissions using `utils.VerifyToken.verify()`.
  
  Args:
      auth_result (str): The access token.
      
  Returns:
      str: The access token."""
  return auth_result


@app.get("/streamlit/verify")
async def verification(
    auth_result: Annotated[str, Depends(check_permission)]) -> str:
  """This function verifies the user's access token using `utils.VerifyToken.verify()`.

  Args:
      auth_result (str): The access token.
  
  Returns:
      str: A string indicating if the user is verified."""
  return 'Approved'


### Example of how to use scopes ###

# @app.get("/streamlit/verify_with_scopes")
# async def harder_verification(
#     auth_result: Annotated[str,
#                            Security(check_permission, scopes=['read:data'])]):
#     return 'Approved'

if __name__ == "__main__":
  uvicorn.run(app)  # type: ignore
