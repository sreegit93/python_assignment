import asyncio
import os
from dotenv import load_dotenv
from src.project_api_client import ProjectApiClient
from src.repository_api_client import RepositoryApiClient
from src.artifact_api_client import ArtifactApiClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

HARBOR_API_URL = os.getenv('HARBOR_API_URL')
HARBOR_USERNAME = os.getenv('HARBOR_USERNAME')
HARBOR_PASSWORD = os.getenv('HARBOR_PASSWORD')

async def main():
    project_client = ProjectApiClient(HARBOR_API_URL, HARBOR_USERNAME, HARBOR_PASSWORD)
    repository_client = RepositoryApiClient(HARBOR_API_URL, HARBOR_USERNAME, HARBOR_PASSWORD)
    artifact_client = ArtifactApiClient(HARBOR_API_URL, HARBOR_USERNAME, HARBOR_PASSWORD)

    projects = await project_client.list_projects()
    logger.info(f"Projects: {projects}")

    for project in projects:
        logger.info(f"Processing project: {project['name']}")
        repositories = await repository_client.list_repositories(project['name'])
        logger.info(f"Repositories in {project['name']}: {repositories}")
        
        for repository in repositories:
            logger.info(f"Processing repository: {repository['name']}")
            artifacts = await artifact_client.list_artifacts(project['name'], repository['name'])
            logger.info(f"Artifacts in {project['name']}/{repository['name']}: {artifacts}")

            await artifact_client.delete_old_tags(project['name'], repository['name'])

if __name__ == "__main__":
    asyncio.run(main())
