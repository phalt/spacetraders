from typing import Dict, Union

from httpx import Response

from src.schemas.errors import Error


def data_or_error(api_response: Response) -> Union[Dict, Error]:
    """
    If `error` exists on the response, return an Error object
    otherwise returns the `data` attribute from a response if one exists.
    """
    api_data = api_response.json()
    if api_data.get("error"):
        return Error(**api_data["error"])
    api_data = api_data["data"]
    return api_data
