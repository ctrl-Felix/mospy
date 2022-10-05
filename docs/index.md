# MosPy

MosPy is a cosmospy fork and aims to be a versatile transaction signing library for the whole cosmos ecosystem.

## Installation

Mospy is available on [pypi](https://pypi.org/project/mospy-wallet/):

`python -m pip install mospy-wallet `

_Note: Even though the name is mospy-wallet on pypi the library itself is called mospy_

## Dependencies

By default mospy will import the protobuf files from cosmospy-protobuf and therefore work with the Cosmos chain.
If you want to use it on another chain I highly recommend to use thee according protobufs to avoid version conflicts.
The `Account` and `Transaction` class both take a `protobuf` argument to specify the protobufs. Note: You have to install
them manually as mospy ships woth cosmospy_protobuf. You can use:

- `evmos` for `evmos-protobuf`
- `osmosis` for `osmosis-protobuf`
- `cosmos` for `cosmospy-protobuf` (default)
- `<your module here>` for your own protobuf module following the cosmos name schema

## Get started

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

## Support

When facing issues feel free to open a [github issue](https://github.com/ctrl-felix/mospy/issues)
or reach out to the creators on the [Osmosis Discord](https://discord.gg/E2vkD6W8Xe).
