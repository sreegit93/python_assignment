import httpx
import asyncio
from tenacity import retry, wait_fixed, stop_after_attempt
from typing import Any, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseHarborApiClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.auth = (username, password)

    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        async with httpx.AsyncClient(auth=self.auth) as client:
            response = await client.request(method, self.base_url + endpoint, **kwargs)
            logger.info(f"Request URL: {response.url}")
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response content: {response.text}")
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                raise
            try:
                return response.json()
            except ValueError:
                logger.error("Failed to decode JSON response")
                raise

    async def get(self, endpoint: str, params: Dict[str, Any] = None) -> Any:
        return await self._request('GET', endpoint, params=params)

    async def post(self, endpoint: str, data: Dict[str, Any] = None) -> Any:
        return await self._request('POST', endpoint, json=data)

    async def put(self, endpoint: str, data: Dict[str, Any] = None) -> Any:
        return await self._request('PUT', endpoint, json=data)

    async def delete(self, endpoint: str) -> Any:
        return await self._request('DELETE', endpoint)
