import httpx

from src.settings import config
from src.api.paths import PATHS
from src.schemas import Agent

headers = {"Authorization": f"Bearer {config.get('api', 'key')}"}

client = httpx.Client(headers=headers)


def test_connectivity() -> Agent:
    """
    Test connectivity by returning
    """
    api_response = client.get(PATHS.AGENT)
    api_response.raise_for_status()
    return Agent(**api_response.json()["data"])
