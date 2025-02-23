"""
    This file contains the logic for fetching authentication domains.

"""
def get_authentication_domains_query(cursor=None):
    """
    Returns the GraphQL query for fetching authentication domains

    Args:
        cursor (str, optional): Cursor for pagination
    """
    query = """
    {
        actor {
            organization {
                authorizationManagement {
                    authenticationDomains {
                        authenticationDomains {
                            id
                            name
                        }
                        nextCursor
                        totalCount
                    }
                }
            }
        }
    }
    """

    if cursor:
        query = """
        query GetAuthDomains($cursor: String!) {
            actor {
                organization {
                    authorizationManagement {
                        authenticationDomains(cursor: $cursor) {
                            authenticationDomains {
                                id
                                name
                            }
                            nextCursor
                            totalCount
                        }
                    }
                }
            }
        }
        """

    return query


def process_auth_domains_response(response):
    """
    Process the NerdGraph response for authentication domains

    Args:
        response (dict): The raw NerdGraph response

    Returns:
        dict: Contains domains list, next cursor, and total count

    Raises:
        ValueError: If the response structure is unexpected
    """
    result = {
        'domains': [],
        'next_cursor': None,
        'total_count': 0
    }

    try:
        auth_domains_data = response['data']['actor']['organization'][
            'authorizationManagement']['authenticationDomains']

        result['domains'] = [
            {
                'id': domain['id'],
                'name': domain['name']
            }
            for domain in auth_domains_data['authenticationDomains']
        ]
        result['next_cursor'] = auth_domains_data.get('nextCursor')
        result['total_count'] = auth_domains_data.get('totalCount', 0)

    except KeyError as e:
        raise ValueError(f"Unexpected response structure: missing {e}")

    return result


def get_authentication_domains(client):
    """
    Fetch all authentication domains using the provided GraphQL client

    Args:
        client: The GraphQL client instance

    Returns:
        dict: Contains complete list of domains and total count
    """
    result = {
        'domains': [],
        'total_count': 0
    }

    cursor = None

    while True:
        query = get_authentication_domains_query(cursor)
        variables = {"cursor": cursor} if cursor else None

        response = client.execute(query, variables)
        page_result = process_auth_domains_response(response)

        result['domains'].extend(page_result['domains'])
        result['total_count'] = page_result['total_count']

        cursor = page_result['next_cursor']
        if not cursor:  # No more pages
            break

    return result