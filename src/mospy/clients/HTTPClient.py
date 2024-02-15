import copy
import time

import httpx
from mospy.Account import Account
from mospy.Transaction import Transaction

from mospy.exceptions.clients import NodeException
from mospy.exceptions.clients import NodeTimeoutException, TransactionNotFound, TransactionTimeout, NotAnApiNode


class HTTPClient:
    """
    Wrapper class to interact with a cosmos chain through their API endpoint

    Args:
        api (str): URL to a Api node
        check_api (bool): Check if the Api node is reachable. Returns either NotAnApiNode or NodeException if the node is not healthy.
    """

    def __init__(self, *, api: str = "https://rest.cosmos.directory/cosmoshub", check_api: bool = False):
        self._api = api.rstrip("/")

        # Check API if reachable
        if check_api:
            self.check_api()

    def check_api(self):
        """
        Checks if the API is reachable. Returns a NodeException or a NotAnApiNode Exception when the check failed.
        """
        try:
            check_response = httpx.get(self._api + "/node_info")
        except httpx.HTTPError:
            raise NodeException(
                "The passed url is not reachable. To disable the health check pass check_api=false to the HTTPClient constructor.")

        if check_response.status_code != 200:
            # Check if the returned text matches the one returned by an RPC
            if "404 page not found" in check_response.text:
                raise NotAnApiNode("Please pass an API endpoint to the HTTPClient. You probably passed an RPC.")
            else:
                raise NodeException(
                    "Health couldn't be verified. To disable the health check pass check_api=false to the HTTPClient constructor.")

    def _make_post_request(self, path, payload, timeout):
        try:
            req = httpx.post(self._api + path, json=payload, timeout=timeout)
        except httpx.TimeoutException:
            raise NodeTimeoutException(f"Node {self._api} timed out after {timeout} seconds")

        if req.status_code != 200:
            try:
                data = req.json()
                message = f"({data['message']}"
            except:
                message = ""
            raise NodeException(f"Error while doing request to api endpoint {message}")

        data = req.json()
        return data

    def _make_get_request(self, path, timeout):
        try:
            req = httpx.get(self._api + path, timeout=timeout)
        except httpx.TimeoutException:
            raise NodeTimeoutException(f"Node {self._api} timed out after {timeout} seconds")
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

    def get_tx(self, *, tx_hash: str, timeout: int = 5):
        """
        Query a transaction by passing the hash

        Note:
            Takes only positional arguments.

        Args:
            tx_hash (Transaction): The transaction hash
            timeout (int): Timeout for the request before throwing a NodeException

        Returns:
            transaction (dict): Transaction dict as returned by the chain


        """
        path = "/cosmos/tx/v1beta1/txs/" + tx_hash

        try:
            data = self._make_get_request(path=path, timeout=timeout)
        except NodeException:
            raise TransactionNotFound(f"The transaction {tx_hash} couldn't be found")

        return data


    def wait_for_tx(self, *, tx_hash: str, timeout: float = 60, poll_period: float = 10):
        """
        Waits for a transaction hash to hit the chain.

        Note:
            Takes only positional arguments

        Args:
            tx_hash (Transaction): The transaction hash
            timeout (bool): Time to wait before throwing a TransactionTimeout. Defaults to 60
            poll_period (float): Time to wait between each check. Defaults to 10

        Returns:
            transaction (dict): Transaction dict as returned by the chain
        """
        start = time.time()
        while time.time() < (start + timeout):
            try:
                return self.get_tx(tx_hash=tx_hash)
            except TransactionNotFound:
                time.sleep(poll_period)

        raise TransactionTimeout(f"The transaction {tx_hash} couldn't be found on chain within {timeout} seconds.")