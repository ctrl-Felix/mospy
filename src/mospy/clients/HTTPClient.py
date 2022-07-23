from mospy.Account import Account
from mospy.Transaction import Transaction

import httpx

class HTTPClient:
    """
    Wrapper class to interact with a cosmos chain through their API endpoint

    Args:
        api (str): URL to a Cosmos api node
    """
    def __init__(
            self,
            *,
            api: str = "https://api.cosmos.network"
    ):
        self._api = api

    def load_account_data(self, account: Account):
        """
        Load the ``next_sequence`` and ``account_number`` into the account object.

        Args:
            account (Account): Account
        """

        address = account.address
        url = self._api + "/cosmos/auth/v1beta1/accounts/" + address
        req = httpx.get(url=url)
        if req.status_code != 200:
            raise RuntimeError("Error while doing request to api endpoint")

        data = req.json()
        sequence = int(data['account']['sequence'])
        account_number = int(data['account']['account_number'])

        account.next_sequence = sequence + 1
        account.account_number = account_number


    def broadcast_transaction(self, *, tx: Transaction, account: Account) -> str:
        """
        Sign and broadcast a transaction.

        Note:
            Takes only positional arguments

        Args:
            tx (Transaction): The transaction object
            account (Account): The sender account

        Returns:
            hash: Transaction hash
        """


