# Examples

Here you'll find some useful code snippets to get started with MosPy

## Account

Examples showing the use of the account class

### Account creation

```python

from mospy import Account

# Generate a new Account with a new seed phrase
account1 = Account()

# Create an account object through a seed phrase and
# get a sub-account of that seed by passing the address index (optional)

account2 = Account(
    seed_phrase="law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style",
    address_index=12
)

# Instantiate the Account by using a private key and
# set a different address prefix to use another cosmos based chain as well as
# the nex account sequence and account number (example values)

account3 = Account(
    private_key="8c2ae3f9c216f714c0a877e7a4952ec03462496e01452bd5ee79ef79d707ff6c",
    hrp="osmo",
    next_sequence=1,
    account_number=187486
)


```

## Transaction

Showcase how to create use the Transaction class

```python
from mospy import Transaction
from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin # Optional

# Create the fee object from the protobufs and pass it when instantiating the Transaction
# or add it later through the set_fee function
fee = Coin(
    denom="uatom",
    amount="1000"
)

# Create the transaction object by passing the account object from the step above
tx = Transaction(
    account=account3,
    fee=fee,
    gas=1000,
)

# Add a transfer message to the transaction (multiple messages can be added)
tx.add_msg(
    tx_type='transfer',
    sender=account3,
    receipient="cosmos1tkv9rquxr88r7snrg42kxdj9gsnfxxg028kuh9",
    amount=1000,
    denom="uatom"
)

# Sign and encode transaction to submit it to the network manually then
tx_bytes = tx.get_tx_bytes()
```

## Client

Examples howing the usage of the included clients

```python
from mospy.clients import HTTPClient

# Instantiate a HTTPClient object by passing a custom API endpoint.
# https://api.cosmos.network is chosen if no api provider is provided
client = HTTPClient(
    api="https://api.cosmos.interbloc.org"
)

# Update the account object to set the current on chain sequence and account_number
client.load_account_data(account=account)

# Broadcast a transaction
# Note: Do not call 'get_tx_bytes' on the transaction object before
# as it will be signed twice then
hash, log = client.broadcast_transaction(transaction=tx)
```
