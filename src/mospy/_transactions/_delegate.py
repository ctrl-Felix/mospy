import importlib

class Transaction:
    name = "delegate"  # Name to reference this transaction type
    _type_url = "/cosmos.staking.v1beta1.MsgDelegate"

    def __init__(
        self,
        protobuf_package: str,
        delegator: str,
        validator: str,
        amount: int,
        denom: str,
    ):
        try:
            self._coin_pb2 = importlib.import_module(
                protobuf_package + ".cosmos.base.v1beta1.coin_pb2")
            self._tx_pb2 = importlib.import_module(
                protobuf_package + ".cosmos.staking.v1beta1.tx_pb2")
        except:
            raise ImportError(
                f"Couldn't import from {protobuf_package}. Is the package installed?"
            )

        _tx_coin = self._coin_pb2.Coin()
        _tx_coin.denom = denom
        _tx_coin.amount = str(amount)

        self._amount = _tx_coin
        self._delegator_address = delegator
        self._validator = validator

    def format(self) -> (str, object):
        msg = self._tx_pb2.MsgUndelegate(
            delegator_address=self._delegator_address,
            validator_address=self._validator,
            amount=self._amount
        )

        return (self._type_url, msg)
