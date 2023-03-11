# MosPy

MosPy is a fork of the cosmospy library and aims to be a versatile transaction signing library for the whole cosmos ecosystem.
It depends [cosmospy-protobuf](https://github.com/ctrl-Felix/cosmospy-protobuf) for the protos. Through this library you also can add your own transaction types and sign them through Mospy.

## Documentation

A documentation with according examples can be found at https://mospy.ctrl-felix.de

## Get Started

You can find a tutorial series on medium: https://medium.com/@ctrl-felix/mospy-tutorial-1-the-basics-95ec757047dc

## Installation

Mospy is available through (pypi)[https://pypi.org/project/mospy-wallet]

`python -m pip install mospy-wallet`

_Note: The package name in python is mospy even if it is called mospy-wallet on pypi as mospy already existed_

## Quickstart

More examples on: https://mospy.ctrl-felix.de/examples/

```python
import httpx # optional
from mospy import Account, Transaction

account = Account(
    seed_phrase="law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style",
    address_index=12
)

tx = Transaction(
    account=account,
    gas=1000,
)
tx.set_fee(
    amount=100,
    denom="uatom"
)
# Add a transfer message to the transaction (multiple messages can be added)
tx.add_msg(
    tx_type='transfer',
    sender=account,
    receipient="cosmos1tkv9rquxr88r7snrg42kxdj9gsnfxxg028kuh9",
    amount=1000,
    denom="uatom"
)

# Sign and encode transaction to submit it to the network manually

# REST endpoint (RPC or API)
tx_bytes = tx.get_tx_bytes_as_string()

# Submit the transaction through the Tendermint RPC
rpc_url = "https://rpc.cosmos.network/"
pushable_tx = json.dumps(
              {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "broadcast_tx_sync", # Available methods: broadcast_tx_sync, broadcast_tx_async, broadcast_tx_commit
                "params": {
                    "tx": tx_bytes
                }
              }
            )
r = httpx.post(rpc_url, data=pushable_tx)

# Submit the transaction through the Cosmos REST API
rpc_api = "https://api.cosmos.network/cosmos/tx/v1beta1/txs"
pushable_tx = json.dumps(
                {
                  "tx_bytes": tx_bytes,
                  "mode": "BROADCAST_MODE_SYNC" # Available modes: BROADCAST_MODE_SYNC, BROADCAST_MODE_ASYNC, BROADCAST_MODE_BLOCK
                }
              )
r = httpx.post(rpc_api, data=pushable_tx)
```
## Different transaction types

Mospy is created to support every possible external transaction type.
To make it easier some transaction types are built in and can be added directly to a transaction object.
But it's not difficult to add your own transaction types! More about transaction types can be found in the docs.
