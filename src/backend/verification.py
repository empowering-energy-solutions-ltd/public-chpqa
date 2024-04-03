from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              SecurityScopes)

from src.backend.config import get_settings


class UnauthorizedException(HTTPException):

  def __init__(self, detail: str, **kwargs):
    """Returns HTTP 403"""
    super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):

  def __init__(self):
    super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                     detail="Requires authentication")


class VerifyToken:
  """Does all the token verification using PyJWT
  
  Attributes:
    config Settings: The settings object.  
    jwks_client PyJWKClient: The PyJWKClient object.  
  
  Methods:
    verify: Takes the users bearer token, decodes it and verifies it using PyJWT. \
      If the token is valid it then checks if the user has the required permissions (scopes).
  """

  def __init__(self):
    self.config = get_settings()

    jwks_url = f'{self.config.auth0_domain}/.well-known/jwks.json'
    self.jwks_client = jwt.PyJWKClient(jwks_url)

  async def verify(
      self,
      security_scopes: SecurityScopes,
      token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())
  ) -> dict[str, str]:
    """ Takes the users bearer token, decodes it and verifies it using PyJWT. \
          If the token is valid it then checks if the user has the required permissions (scopes).
    
    Args:
        security_scopes (SecurityScopes): The required permissions (scopes).  
        token (Optional[HTTPAuthorizationCredentials]): The users bearer token.  
    
    Returns:
        dict[str,str]: The decoded token payload.
    """
    if token is None:
      raise UnauthenticatedException
    try:
      signing_key = self.jwks_client.get_signing_key_from_jwt(
          token.credentials).key
    except jwt.exceptions.PyJWKClientError as error:
      raise UnauthorizedException(str(error))
    except jwt.exceptions.DecodeError as error:
      raise UnauthorizedException(str(error))
    try:
      payload = jwt.decode(
          token.credentials,
          signing_key,
          algorithms=[self.config.auth0_algorithms],
          audience=self.config.auth0_api_audience,
          issuer=self.config.auth0_issuer,
      )
      if security_scopes.scopes:
        if not payload['permissions'] in security_scopes.scopes:
          raise UnauthorizedException(
              f"Insufficient permissions. Required: {security_scopes.scopes}")
    except Exception as error:
      raise UnauthorizedException(str(error))
    return payload
