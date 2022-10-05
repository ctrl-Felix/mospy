# Transaction Types
Nearly every cosmos chain has its transaction types usually on top of the standard cosmos ones. Mospy supports some standard transaction types that should be the same on every chain.
However, every chain can modify these and you would then need to implement that change by yourself. But this will be explained here.

## Data structures
In general, the cosmos sdk uses the protobuf data format to define data structures. These protobuf files serve as documentation and help to serialize the data directly in your code.

To make protobufs more accessible for python I am maintaining the `cosmospy-protobuf` library 
which contains all cosmos protobuf files compiled for python. Mospy is using cosmospy-protobuf.

The naming scheme is following the official cosmos naming scheme. This is especially useful when working with different transaction types.

## Included transaction types
Mospy ships some standard transaction types for easier implementation. Currently, following transaction types are supported:
* MsgSend
* MsgDelegate
* MsgUndelegate
* MsgWithdrawDelegatorReward

Each transaction type takes different keyword arguments. You can check out the examples to see how to use each type. The following example will use the MsgSend type as it is the most common one:

```python
from mospy import Transaction, Account

account = Account(...)
tx = Transaction(...)

tx.add_msg(
    tx_type='transfer',
    sender=account,
    receipient="cosmos1tkv9rquxr88r7snrg42kxdj9gsnfxxg028kuh9",
    amount=1000,
    denom="uatom"
)

# Sign and broadcast
```

The first argument always defines the transaction type. The following required arguments are then defined by each adapter. 
You have to use keyword arguments.

## Custom transaction types
Transaction types that aren't integrated can be added to the transaction class through the `add_raw_msg` method. This function takes two arguments.
The method takes two arguments. The first one is the msg data in the protobuf format and the second one is the type url. 

For instance, if you want to make a transaction that changes the reward withdraw address you will need to implement the transaction with the type `/cosmos.distribution.v1beta1.MsgSetWithdrawAddress`.

The compiled protobuf files are available at `cosmospy_protobuf.cosmos.distribution.v1beta1.tx_pb2`.

To see what data you need to pass you can check out the according protobuf file in the cosmospy-protobuf repository:
https://github.com/ctrl-Felix/cosmospy-protobuf/blob/main/src/cosmospy_protobuf/cosmos/distribution/v1beta1/tx.proto#L31

The full example will look like this:
````python
from mospy import Transaction
from cosmospy_protobuf.cosmos.distribution.v1beta1.tx_pb2 import MsgSetWithdrawAddress

tx = Transaction(...)

wmsg = MsgSetWithdrawAddress(
    delegator_address="cosmos1...",
    withdraw_address="cosmos1..."

)
tx.add_raw_msg(wmsg, type_url="/cosmos.distribution.v1beta1.MsgSetWithdrawAddress")

# Sign and broadcast

````

You see! It's not complicated at all.


## Transaction body

A transaction can have many messages with different transaction types. You can save a lot of fees by aggregating your messages into one big transaction.
But keep in mind. If one message fails the whole transaction and all messages fail.
