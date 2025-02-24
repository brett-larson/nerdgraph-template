
from typing import Optional, Dict, Any
import requests
import os
from nerdgraph.utils.logger import setup_logger

logger = setup_logger(__name__)

class GraphQLClient:
    """Client for interacting with New Relic's GraphQL API (NerdGraph)"""
    
    def __init__(self, api_key: Optional[str] = None, region: str = 'US'):
        """
        Initialize GraphQL client
        
        Args:
            api_key: New Relic API key. If not provided, will look for NEW_RELIC_API_KEY env var
            region: API region (US or EU)
        """
        self.api_key = api_key or os.getenv('NEW_RELIC_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided or set in NEW_RELIC_API_KEY environment variable")
            
        self.base_url = "https://api.newrelic.com/graphql" if region.upper() == 'US' else "https://api.eu.newrelic.com/graphql"
        
        self.headers = {
            "Content-Type": "application/json",
            "API-Key": self.api_key
        }

    def execute(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query
        
        Args:
            query: GraphQL query string
            variables: Optional dictionary of variables for the query
            
        Returns:
            Dictionary containing the query response
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If the response contains GraphQL errors
        """
        try:
            logger.info("Executing GraphQL query")
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={"query": query, "variables": variables}
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Check for GraphQL errors
            if 'errors' in result:
                error_messages = [error.get('message', 'Unknown error') 
                                for error in result['errors']]
                raise ValueError(f"GraphQL errors: {'; '.join(error_messages)}")
                
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
        except ValueError as e:
            logger.error(f"GraphQL error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def batch_execute(self, queries: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
        """
        Execute multiple queries in sequence
        
        Args:
            queries: List of dictionaries containing 'query' and optional 'variables'
            
        Returns:
            List of query responses
        """
        results = []
        for query_info in queries:
            result = self.execute(
                query_info['query'],
                query_info.get('variables')
            )
            results.append(result)
        return results