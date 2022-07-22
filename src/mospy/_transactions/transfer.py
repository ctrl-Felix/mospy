from mospy.Account import Account
import cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 as coin
import cosmospy_protobuf.cosmos.bank.v1beta1.tx_pb2 as tx


class Transaction:
    _type_url = "/cosmos.bank.v1beta1.MsgSend"

    def __init__(
            self,
            sender: Account,
            receipient: str,
            amount: int,
            denom: str
    ):
        _tx_coin = coin.Coin()
        _tx_coin.denom = denom
        _tx_coin.amount = str(amount)
        self._amount = _tx_coin
        self._sender = sender.address()
        self._receipient = receipient

    def format(self) -> (str, tx.MsgSend):
        msg = tx.MsgSend(
            from_address=self._sender,
            to_address=self._receipient,
        )
        msg.amount.append(self._amount)

        return (
            self._type_url,
            msg
        )
