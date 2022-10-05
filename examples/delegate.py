from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin
from cosmospy_protobuf.cosmos.staking.v1beta1.tx_pb2 import MsgDelegate

from src.mospy import Transaction, Account
from src.mospy.clients import HTTPClient

client = HTTPClient()
account = Account(
    seed_phrase="SEED HERE",
    account_number=1234,
    next_sequence=1234
)
tx = Transaction(
    account=account,
    gas=10000000  # This need to be adapted
)

dmsg = MsgDelegate(
        delegator_address=account.address,
        validator_address="VALOPER HERE",
        amount=Coin(amount=str(1000000), denom="uatom")
    )

tx.set_fee(
    amount=2000,
    denom="uatom"
)


tx.add_raw_msg(dmsg, type_url="/cosmos.staking.v1beta1.tx.MsgDelegate")

client.broadcast_transaction(transaction=tx)