import importlib

class Transaction:
    name = "withdraw_reward"  # Name to reference this transaction type
    _type_url = "/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward"

    def __init__(
        self,
        protobuf_package: str,
        delegator: str,
        validator: str,
    ):
        try:
            self._coin_pb2 = importlib.import_module(
                protobuf_package + ".cosmos.base.v1beta1.coin_pb2")
            self._tx_pb2 = importlib.import_module(
                protobuf_package + ".cosmos.distribution.v1beta1.tx_pb2")
        except:
            raise ImportError(
                f"Couldn't import from {protobuf_package}. Is the package installed?"
            )

        self._delegator_address = delegator
        self._validator = validator

    def format(self) -> (str, object):
        msg = self._tx_pb2.MsgWithdrawDelegatorReward(
            delegator_address=self._delegator_address,
            validator_address=self._validator,
        )

        return (self._type_url, msg)
