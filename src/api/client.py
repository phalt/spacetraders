from typing import Union, Dict, Optional
import httpx

from src.settings import config
from time import sleep
from src.schemas.errors import Error

headers = {"Authorization": f"Bearer {config.get('api', 'key')}"}

client = httpx.Client(headers=headers)
# Mostly for making registration calls
bare_client = httpx.Client()


def safe_get(*, path: str) -> Union[Dict, Error]:
    """
    Like client.get but handles API limits safely
    by sleeping for the amount of time set by the API before trying again.
    """
    response = client.get(path)
    api_data = response.json()
    if api_data.get("error"):
        error = Error(**api_data["error"])
        if error.code == "429":
            # We've hit a rate limit, sleep a bit and call the API again
            sleep(error.data["retryAfter"])
            return safe_get(path=path)
        # Return other errors
        return error
    else:
        api_data = api_data["data"]
        return api_data


def safe_post(*, path: str, data: Optional[Dict] = None) -> Union[Dict, Error]:
    """
    Like client.post but handles API limits safely
    by sleeping for the amount of time set by the API before trying again.
    """
    response = client.post(path, data=data)
    api_data = response.json()
    if api_data.get("error"):
        error = Error(**api_data["error"])
        if error.code == "429":
            # We've hit a rate limit, sleep a bit and call the API again
            sleep(error.data["retryAfter"])
            return safe_post(path=path, data=data)
        # Return other errors
        return error
    else:
        api_data = api_data["data"]
        return api_data
