import os
from dotenv import load_dotenv
from nerdgraph.utils import setup_logger
from nerdgraph.api.api_client import GraphQLClient

# This import statement will vary based on the desired workflow.
from api.queries.workflows.get_managed_accounts.workflow import ManagedAccountsWorkflow

# Setup logger
logger = setup_logger(__name__)

def main():

    logger.info("Starting workflow.")

    # Load environment variables
    load_dotenv()




    client = GraphQLClient(
        api_key=os.getenv("NEW_RELIC_API_KEY"),
        region="US"
    )

    # Run workflow
    workflow = ManagedAccountsWorkflow(client)


    logger.info("Workflow completed successfully.")



if __name__ == "__main__":
    main()
