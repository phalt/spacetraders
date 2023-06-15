import httpx

from src.settings import config

headers = {"Authorization": f"Bearer {config.get('api', 'key')}"}

client = httpx.Client(headers=headers)
# Mostly for making registration calls
bare_client = httpx.Client()
