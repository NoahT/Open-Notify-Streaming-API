# Pre-commit hook

The [pre-commit](./pre-commit) hook script does the following:
1. Runs the unit tests for streaming and ingestion services
2. Runs pylint across streaming and ingestion services.

To set up the pre-commit script, copy the pre-commit script into the `.git/hooks/` directory of your local repository.
