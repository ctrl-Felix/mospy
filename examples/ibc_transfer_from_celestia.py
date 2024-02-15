import time
from cosmospy_protobuf.ibc.applications.transfer.v1.tx_pb2 import MsgTransfer
from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin
from cosmospy_protobuf.ibc.core.client.v1.client_pb2 import Height
from mospy import Account, Transaction
from mospy.clients import HTTPClient

account = Account(
    seed_phrase=MNEMONIC,
    hrp = "celestia"
)

osmosis_account = Account(
    seed_phrase=MNEMONIC,
    hrp = "osmo"
)

client = HTTPClient(
    api="https://celestia-lcd.enigma-validator.com"
)

client.load_account_data(account=account)

# IBC transfer message
token = Coin(
    denom="utia",
    amount="1"
)

ibc_msg = MsgTransfer(
    source_port="transfer",
    source_channel="channel-2",
    sender=account.address,
    receiver=osmosis_account.address,
)

timeout_height = Height(
    revision_height=0,
    revision_number=0 # This can be 0 too to disable it
)

ibc_msg.timeout_height.CopyFrom(timeout_height)

ibc_msg.token.CopyFrom(token)
ibc_msg.timeout_timestamp = time.time_ns() + 600 * 10 ** 9

# Transaction
fee = Coin(
    denom="utia",
    amount="100"
)
tx = Transaction(
    account=account,
    fee=fee,
    gas=1000,
    chain_id="celestia"
)
tx.add_raw_msg(ibc_msg, type_url="/ibc.applications.transfer.v1.MsgTransfer")

# Estimate gas
client.estimate_gas(transaction=tx, update=True, multiplier=1.3)

# Submit
result = client.broadcast_transaction(transaction=tx)
print(result)
