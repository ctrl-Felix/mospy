import json

import requests
from mospy import Account, Transaction
from cosmospy_protobuf.cosmos.distribution.v1beta1.tx_pb2 import MsgSetWithdrawAddress
import httpx

SEED: str
ADDRESS: str
API = "https://rest.cosmos.directory/agoric"
RPC = "https://rpc.cosmos.directory/agoric"


account = Account(
    seed_phrase=SEED,
    slip44=564,
    next_sequence=290,
    account_number=1,
    hrp="agoric"
)
tx = Transaction(
    account=account,
    chain_id="agoric-3",
    gas=10000000
)

wmsg = MsgSetWithdrawAddress(
    delegator_address=account.address,
    withdraw_address=ADDRESS

)
tx.add_raw_msg(wmsg, type_url="/cosmos.distribution.v1beta1.MsgSetWithdrawAddress")

tx.set_fee(
    amount=0,
    denom="uist"
)

tx_bytes = tx.get_tx_bytes_as_string()

pushable_tx = json.dumps(
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "broadcast_tx_sync",
        # Available methods: broadcast_tx_sync, broadcast_tx_async, broadcast_tx_commit
        "params": {
            "tx": tx_bytes
        }
    }
)
r = httpx.post(RPC, data=pushable_tx)
print(r.text)