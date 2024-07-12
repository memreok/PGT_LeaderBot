import sys
import os
import json
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
from log_config import get_logger

logger = get_logger(__name__)

from commit_scraper import get_user_commits_in_repo
from process_commits import process_commits

async def main(username, repo_link, since_date, until_date):
    commit_infos = await get_user_commits_in_repo(
        username,
        repo_link,
        since_date,
        until_date,
    )

    if commit_infos:
        processed_commits = await process_commits(commit_infos)
        for processed_commit in processed_commits:
            logger.debug(processed_commit)
    else:
        logger.info("No commits found or failed to fetch commits.")

    for commit_info in processed_commits:
        logger.debug(json.dumps(commit_info, indent=5))
        
    return processed_commits

if __name__ == "__main__":
    username = "berkingurcan"
    repo_link = "https://github.com/UmstadAI/discord-umstad"
    since_date = "2024-07-01T00:00:00Z"  # ISO 8601 format
    until_date = "2024-07-04T00:00:00Z"

    asyncio.run(main(
        username,
        repo_link,
        since_date,
        until_date
    ))
