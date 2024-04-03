import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings():
  auth0_domain: str = os.getenv("AUTH0_DOMAIN")
  auth0_api_audience: str = os.getenv("AUTH0_API_AUDIENCE")
  auth0_issuer: str = os.getenv("AUTH0_ISSUER")
  auth0_algorithms: str = os.getenv("AUTH0_ALGORITHMS")


@lru_cache()
def get_settings():
  return Settings()
