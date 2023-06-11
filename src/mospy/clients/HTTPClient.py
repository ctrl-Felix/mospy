import copy

import httpx
from mospy.Account import Account
from mospy.Transaction import Transaction

from mospy.exceptions.clients import NodeException


class HTTPClient:
    """
    Wrapper class to interact with a cosmos chain through their API endpoint

    Args:
        api (str): URL to a Api node
    """

    def __init__(self, *, api: str = "https://api.cosmos.interbloc.org"):
        self._api = api

    def _make_post_request(self, path, payload, timeout):
        req = httpx.post(self._api + path, json=payload, timeout=timeout)

        if req.status_code != 200:
            try:
                data = req.json()
                message = f"({data['message']}"
            except:
                message = ""
            raise NodeException(f"Error while doing request to api endpoint {message}")

        data = req.json()
        return data

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
            raise NodeException("Error while doing request to api endpoint")

        data = req.json()
        sequence = int(data["account"]["sequence"])
        account_number = int(data["account"]["account_number"])

        account.next_sequence = sequence
        account.account_number = account_number

    def broadcast_transaction(self,
                              *,
                              transaction: Transaction,
                              timeout: int = 10) -> [str, int, str]:
        """
        Sign and broadcast a transaction.

        Note:
            Takes only positional arguments

        Args:
            transaction (Transaction): The transaction object
            timeout (int): Timeout

        Returns:
            hash: Transaction hash
            code: Result code
            log: Log (None if transaction successful)
        """
        path = "/cosmos/tx/v1beta1/txs"
        tx_bytes = transaction.get_tx_bytes_as_string()
        payload = {"tx_bytes": tx_bytes, "mode": "BROADCAST_MODE_SYNC"}

        data = self._make_post_request(path, payload, timeout)

        hash = data["tx_response"]["txhash"]
        code = data["tx_response"]["code"]
        log = None if code == 0 else data["tx_response"]["raw_log"]

        return {"hash": hash, "code": code, "log": log}

    def estimate_gas(self,
                              *,
                              transaction: Transaction,
                              update: bool = True,
                              multiplier: float = 1.2,
                              timeout: int = 10) ->int:
        """
        Simulate a transaction to get the estimated gas usage.

        Note:
            Takes only positional arguments

        Args:
            transaction (Transaction): The transaction object
            update (bool): Update the transaction with the estimated gas amount
            multiplier (float): Multiplier for the estimated gas when updating the transaction. Defaults to 1.2
            timeout (int): Timeout

        Returns:
            expedted_gas: Expected gas
        """
        path = "/cosmos/tx/v1beta1/simulate"
        tx_bytes = transaction.get_tx_bytes_as_string()
        payload = {"tx_bytes": tx_bytes}

        data = self._make_post_request(path, payload, timeout)

        gas_used = int(data["gas_info"]["gas_used"])

        if update:
            transaction.set_gas(int(gas_used * multiplier))

        return gas_used