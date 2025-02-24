from nerdgraph.utils.logger import setup_logger

logger = setup_logger(__name__)


def get_managed_accounts_query():
    """Returns the GraphQL query for fetching managed accounts"""
    return """
    query GetManagedAccounts($isCanceled: Boolean!) {
        actor {
            organization {
                accountManagement {
                    managedAccounts(isCanceled: $isCanceled) {
                        id
                        name
                        isCanceled
                        regionCode
                    }
                }
            }
        }
    }
    """

def process_managed_accounts_response(response):
    """
    Process the NerdGraph response for managed accounts

    Args:
        response (dict): The raw NerdGraph response

    Returns:
        list: List of dictionaries containing account information

    Raises:
        ValueError: If the response structure is unexpected
    """
    try:
        accounts = response['data']['actor']['organization']['accountManagement']['managedAccounts']

        account_count = len(accounts)
        logger.info(f"Number of managed accounts: {account_count}")

        return [
            {
                'id': account['id'],
                'name': account['name'],
                'is_canceled': account['isCanceled'],
                'region_code': account['regionCode']
            }
            for account in accounts
        ]
    except KeyError as e:
        raise ValueError(f"Unexpected response structure: missing {e}")


def get_managed_accounts(client, canceled=False):
    """
    Fetch managed accounts using the provided GraphQL client

    Args:
        client: The GraphQL client instance
        canceled (bool): Show active accounts by default

    Returns:
        list: Processed list of account information
    """
    query = get_managed_accounts_query()
    variables = {"isCanceled": canceled}

    response = client.execute(query, variables)
    return process_managed_accounts_response(response)