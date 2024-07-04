from typing import Any
from .base_api_client import BaseHarborApiClient

class RepositoryApiClient(BaseHarborApiClient):
    async def list_repositories(self, project_name: str) -> Any:
        return await self.get(f'/projects/{project_name}/repositories')
