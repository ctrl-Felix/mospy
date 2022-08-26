from cosmospy_protobuf.ibc.applications.transfer.v1.tx_pb2 import MsgTransfer
from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin
from cosmospy_protobuf.ibc.core.client.v1.client_pb2 import Height # Optional, see comments below

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

asset = Coin(
    amount="1000000",
    denom="uatom"
)

# Use either a timeout_tiemstamp or timeout_height for your transfer If you want to disable it you can set both to
# zero. But keep in mind that you need one of the two to get the transfer working More information about timeouts:
# https://ibc.cosmos.network/main/ibc/overview.html#receipts-and-timeouts

timeout_height = Height(
    revision_number=4,
    revision_height=1234
)
tmsg = MsgTransfer(
    source_port="transfer",
    source_channel="channel-1",
    token=asset,
    sender=account.address,
    receiver="",
    timeout_timestamp=0,
    timeout_height=timeout_height,

)

tx.set_fee(
    amount=2000,
    denom="uatom"
)


tx.add_raw_msg(tmsg, type_url="/ibc.applications.transfer.v1.MsgTransfer")

client.broadcast_transaction(transaction=tx)