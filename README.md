# MosPy

MosPy is a fork of the cosmospy library and aims to be a versatile transaction signing library for the whole cosmos ecosystem.
It depends [cosmospy-protobuf](https://github.com/ctrl-Felix/cosmospy-protobuf) for the protos. Through this library you also can add your own transaction types and sign them through Mospy.

## Documentation

A documentation with according examples can be founds at https://mospy.ctrl-felix.de

## Quickstart

This is a quick example to showcase the functionality. For more information please check out the [docs](https://mospy.ctrl-felix.de).

```python
from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin

from mospy import Account
from mospy import Transaction
from mospy.clients import HTTPClient

account = Account(
    seed_phrase="law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style",
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

client = HTTPClient(
    api='https://api.cosmos.interbloc.org'
)

client.load_account_data(account=account)
hash, log = client.broadcast_transaction(transaction=tx)
```
