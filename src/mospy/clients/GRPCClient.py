import base64

import grpc
import httpx
from google.protobuf.json_format import MessageToDict
from mospy.Account import Account
from mospy.Transaction import Transaction

from cosmospy_protobuf.cosmos.tx.v1beta1.service_pb2 import BroadcastTxRequest
import cosmospy_protobuf.cosmos.auth.v1beta1.query_pb2 as account_query
import cosmospy_protobuf.cosmos.auth.v1beta1.query_pb2_grpc as account_query_grpc
import cosmospy_protobuf.cosmos.tx.v1beta1.service_pb2_grpc as tx_grpc

class GRPCClient:
    """
    Wrapper class to interact with a cosmos chain through their grpc endpoint

    Args:
        host (str): URL to a Cosmos api node
        port (int): Port to connect to
        ssl (bool): Whether an ssl encrypted endpoint should be used
    """

    def __init__(self, *, host: str = "cosmoshub.strange.love", port: int = 9090, ssl: bool = False ):
        self._host = host
        self._port = port
        self._ssl = ssl

    def _connect(self):
        if self._ssl:
            con = grpc.secure_channel(
                f'{self._host}:{self._port}',
                credentials=grpc.ChannelCredentials
            )
        else:
            con = grpc.insecure_channel(
                f'{self._host}:{self._port}'
            )
        return con

    def load_account_data(self, account: Account):
        """
        Load the ``next_sequence`` and ``account_number`` into the account object.

        Args:
            account (Account): Account
        """
        con = self._connect()
        address = account.address

        query_stub = account_query_grpc.QueryStub(con)
        account_request = account_query.QueryAccountRequest(
            address=address
        )

        req = query_stub.Account(account_request)
        data = dict(MessageToDict(req.account))

        sequence = 0 if not 'sequence' in data else int(data['sequence'])
        account_number = int(data["accountNumber"])

        account.next_sequence = sequence
        account.account_number = account_number
        con.close()

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

        Returns:
            hash: Transaction hash
            code: Result code
            log: Log (None if transaction successful)
        """
        con = self._connect()
        tx_bytes = transaction.get_tx_bytes()

        tx_request = BroadcastTxRequest(
            tx_bytes=tx_bytes,
            mode=2  # BROADCAST_MODE_SYNC
        )

        tx_stub = tx_grpc.ServiceStub(con)
        tx_data = tx_stub.BroadcastTx(tx_request)

        hash = tx_data.tx_response.txhash
        code = tx_data.tx_response.code
        log = None if code == 0 else tx_data.tx_response.raw_log

        return [hash, code, log]
