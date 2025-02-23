from dotenv import load_dotenv
from nerdgraph.utils import setup_logger

logger = setup_logger(__name__)

def main():

    logger.info("Application started")

    try:
        # Load environment variables
        load_dotenv()
    except Exception as e:
        logger.exception("Failed to load environment variables")
        raise e

    workflow = APMModificationWorkflow("output.csv")
    workflow.run()

    logger.info("Application finished")

if __name__ == "__main__":
    main()