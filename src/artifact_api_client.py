from datetime import datetime, timedelta
from typing import Any
from .base_api_client import BaseHarborApiClient
import logging

logger = logging.getLogger(__name__)

class ArtifactApiClient(BaseHarborApiClient):
    async def list_artifacts(self, project_name: str, repository_name: str) -> Any:
        # Split the repository name if it includes the project name
        if '/' in repository_name:
            repository_name = repository_name.split('/')[-1]
        url = f'/projects/{project_name}/repositories/{repository_name}/artifacts'
        logger.info(f"Requesting artifacts from URL: {self.base_url + url}")
        return await self.get(url)

    async def delete_old_tags(self, project_name: str, repository_name: str, days: int = 30) -> None:
        artifacts = await self.list_artifacts(project_name, repository_name)
        cutoff_date = datetime.now() - timedelta(days=days)
        for artifact in artifacts:
            for tag in artifact.get('tags', []):
                tag_date = datetime.strptime(tag['push_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                if tag_date < cutoff_date:
                    await self.delete(f'/projects/{project_name}/repositories/{repository_name}/artifacts/{artifact["digest"]}/tags/{tag["name"]}')
