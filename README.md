# MosPy
MosPy is a fork of the cosmospy library and aims to be a versatile transaction signing library for the whole cosmos ecosystem.
It depends [cosmospy-protobuf](https://github.com/ctrl-Felix/cosmospy-protobuf) for the protos. Through this library you also can add your own transaction types and sign them through Mospy

## Example
```python
import json
import httpx as httpx

from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin

from mospy.Account import Account
from mospy.Transaction import Transaction


account = Account(
    seed_phrase="law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style",
    account_number=1,
    sequence=0
)


fee = Coin(
    denom="uatom",
    amount="1000"
)

tx = Transaction(
    account=account,
    fee=fee,
    gas=1000,
)

tx.add_msg(
    tx_type='transfer',
    sender=account,
    receipient="cosmos1tkv9rquxr88r7snrg42kxdj9gsnfxxg028kuh9",
    amount=1000,
    denom="uatom"
)

tx_bytes = tx.get_tx_bytes()

# Submit the transaction through the Cosmos REST API
rpc_api = "https://api.cosmos.network/cosmos/tx/v1beta1/txs"
pushable_tx = json.dumps(
                {
                  "tx_bytes": tx_bytes,
                  "mode": "BROADCAST_MODE_SYNC" # Available modes: BROADCAST_MODE_SYNC, BROADCAST_MODE_ASYNC, BROADCAST_MODE_BLOCK
                }
              )
r = httpx.post(rpc_api, json=pushable_tx)
print(r.text)
```