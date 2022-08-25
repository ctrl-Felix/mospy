import importlib

from mospy.Account import Account


class Transaction:
    name = "transfer"  # Name to reference this transaction type
    _type_url = "/cosmos.bank.v1beta1.MsgSend"

    def __init__(
        self,
        protobuf_package: str,
        sender: Account,
        receipient: str,
        amount: int,
        denom: str,
    ):
        try:
            self._coin_pb2 = importlib.import_module(
                protobuf_package + ".cosmos.base.v1beta1.coin_pb2")
            self._tx_pb2 = importlib.import_module(
                protobuf_package + ".cosmos.bank.v1beta1.tx_pb2")
        except:
            raise ImportError(
                f"Couldn't import from {protobuf_package}. Is the package installed?"
            )

        _tx_coin = self._coin_pb2.Coin()
        _tx_coin.denom = denom
        _tx_coin.amount = str(amount)
        self._amount = _tx_coin
        self._sender = sender.address
        self._receipient = receipient

    def format(self) -> (str, object):
        msg = self._tx_pb2.MsgSend(
            from_address=self._sender,
            to_address=self._receipient,
        )
        msg.amount.append(self._amount)

        return (self._type_url, msg)
