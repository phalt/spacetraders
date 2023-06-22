import asyncio
from typing import Dict, Optional, Union

import httpx
from rich.pretty import pprint

from src.schemas.errors import Error
from src.settings import config

headers = {"Authorization": f"Bearer {config.get('api', 'key')}"}

client = httpx.Client(headers=headers)
async_client = httpx.AsyncClient(headers=headers)
# Mostly for making registration calls
bare_client = httpx.Client()


async def safe_get(*, path: str) -> Union[Dict, Error]:
    """
    Like client.get but handles API limits safely by sleeping
    for the amount of time set by the API before trying again.
    """
    try:
        response = await async_client.get(path)
    except httpx.HTTPError as exc:
        pprint(f"HTTP Exception for {exc.request.url} - {exc}")
        await asyncio.sleep(1)
        return await safe_get(path=path)
    api_data = response.json()
    if api_data.get("error"):
        error = Error(**api_data["error"])
        if error.code == 429 and error.data:
            # We've hit a rate limit, sleep a bit and call the API again
            await asyncio.sleep(error.data["retryAfter"])
            return await safe_get(path=path)
        # Return other errors
        return error
    else:
        api_data = api_data["data"]
        return api_data


async def safe_post(*, path: str, data: Optional[Dict] = None) -> Union[Dict, Error]:
    """
    Like client.post but handles API limits safely
    by sleeping for the amount of time set by the API before trying again.
    """
    try:
        response = await async_client.post(path, json=data)
    except httpx.HTTPError as exc:
        pprint(f"HTTP Exception for {exc.request.url} - {exc}")
        await asyncio.sleep(1)
        return await safe_post(path=path, data=data)
    api_data = response.json()
    if api_data.get("error"):
        error = Error(**api_data["error"])
        if error.code == 429 and error.data:
            # We've hit a rate limit, sleep a bit and call the API again
            await asyncio.sleep(error.data["retryAfter"])
            return await safe_post(path=path, data=data)
        # Return other errors
        return error
    else:
        api_data = api_data["data"]
        return api_data


async def safe_patch(*, path: str, data: Optional[Dict] = None) -> Union[Dict, Error]:
    """
    Like client.patch but handles API limits safely
    by sleeping for the amount of time set by the API before trying again.
    """
    try:
        response = await async_client.patch(path, json=data)
    except httpx.HTTPError as exc:
        pprint(f"HTTP Exception for {exc.request.url} - {exc}")
        await asyncio.sleep(1)
        return await safe_patch(path=path, data=data)
    api_data = response.json()
    if api_data.get("error"):
        error = Error(**api_data["error"])
        if error.code == 429 and error.data:
            # We've hit a rate limit, sleep a bit and call the API again
            await asyncio.sleep(error.data["retryAfter"])
            return await safe_patch(path=path, data=data)
        # Return other errors
        return error
    else:
        api_data = api_data["data"]
        return api_data
