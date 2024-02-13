import copy

from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin
from mospy import Account
from mospy import Transaction
from mospy.clients import HTTPClient

API = "https://rest-cosmoshub.ecostake.com"

class TestHTTPClientClass:
    seed_phrase = "law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style"

    def test_account_data_loading(self):
        account = Account(seed_phrase=self.seed_phrase)

        client = HTTPClient(api=API)

        client.load_account_data(account)

        assert account.account_number == 1257460

        assert account.next_sequence >= 0

    def test_transaction_submitting(self):
        account = Account(
            seed_phrase=self.seed_phrase,
            account_number=1,
            next_sequence=0,
        )

        client = HTTPClient(api=API)

        fee = Coin(denom="uatom", amount="1000")

        tx = Transaction(
            account=account,
            fee=fee,
            gas=10000000000,
        )

        tx.add_msg(
            tx_type="transfer",
            sender=account,
            receipient="cosmos1tkv9rquxr88r7snrg42kxdj9gsnfxxg028kuh9",
            amount=1000,
            denom="uatom",
        )
        copied_transaction = copy.copy(tx)
        tx_data = client.broadcast_transaction(transaction=copied_transaction)

        assert (
            tx_data["hash"] ==
            "54B845AEB1523803D4EAF2330AE5759A83458CB5F0211159D04CC257428503C4")

        client.load_account_data(account=account)

        gas_used = client.estimate_gas(
            transaction=tx,
            update=False,
        )


        assert gas_used > 0

