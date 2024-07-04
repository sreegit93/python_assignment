from typing import Any
from .base_api_client import BaseHarborApiClient

class ProjectApiClient(BaseHarborApiClient):
    async def list_projects(self) -> Any:
        return await self.get('/projects')
