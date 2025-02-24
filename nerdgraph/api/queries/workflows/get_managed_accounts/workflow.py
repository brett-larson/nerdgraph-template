from nerdgraph.api.queries.common import get_managed_accounts
from nerdgraph.data.csv_handler import CSVHandler


class ManagedAccountsWorkflow:
    def __init__(self, client, csv_handler: CSVHandler = None):
        self.client = client
        self.csv_handler = csv_handler or CSVHandler()

    def get_all_accounts(self):
        """Get both active and canceled accounts"""
        try:
            # Get active accounts
            active_accounts = get_managed_accounts(self.client, canceled=False)

            # Get canceled accounts
            canceled_accounts = get_managed_accounts(self.client, canceled=True)

            # Write to separate CSVs
            self.csv_handler.write_data('active_accounts.csv', active_accounts)
            self.csv_handler.write_data('expired_accounts.csv', canceled_accounts)

            return {
                'active': active_accounts,
                'expired': canceled_accounts
            }

        except Exception as e:
            print(f"Error getting accounts: {e}")
            raise