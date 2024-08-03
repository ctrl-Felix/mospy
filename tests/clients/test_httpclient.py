import copy

from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin
from mospy import Account
from mospy import Transaction
from mospy.clients import HTTPClient

from mospy.exceptions.clients import NotAnApiNode, NodeException

API = "https://cosmos-rest.publicnode.com"

class TestHTTPClientClass:
    seed_phrase = "law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style"

    def test_account_data_loading(self):
        account = Account(seed_phrase=self.seed_phrase)

        client = HTTPClient(api=API)

        client.load_account_data(account)

        assert account.account_number == 1257460

        assert account.next_sequence >= 0

    def test_node_health_check(self):
        try:
            client = HTTPClient(api="https://cosmos-rpc.publicnode.com", check_api=True)
        except NotAnApiNode:
            assert True
        else:
            assert False

        try:
            client = HTTPClient(api="https://dead-url-awdbnawdbauiowd.com", check_api=True)
        except NodeException:
            assert True
        else:
            assert False

        client = HTTPClient(api="https://dead-url-awdbnawdbauiowd.com", check_api=False)

    def test_transaction_submitting(self):
        account = Account(
            seed_phrase=self.seed_phrase,
            account_number=1,
            next_sequence=0,
        )

        client = HTTPClient(api=API)
        client.load_account_data(account=account)

        fee = Coin(denom="uatom", amount="1500")

        tx = Transaction(
            account=account,
            fee=fee,
            gas=100000,
        )

        tx.add_msg(
            tx_type="transfer",
            sender=account,
            recipient=account.address,
            amount=1000,
            denom="uatom",
        )

        expected_gas = client.estimate_gas(transaction=tx)

        assert expected_gas > 0

        tx_data = client.broadcast_transaction(transaction=tx)

        assert tx_data["code"] == 0

        transaction_dict = client.wait_for_tx(
            tx_hash=tx_data["hash"]
        )

        assert "tx" in transaction_dict and transaction_dict["tx"]["body"]["messages"][0] == {
            "@type": "/cosmos.bank.v1beta1.MsgSend",
            "from_address": account.address,
            "to_address": account.address,
            "amount": [
                {
                    "denom": "uatom",
                    "amount": "1000"
                }
            ]
        }
