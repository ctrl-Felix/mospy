from mospy.Account import Account
import cosmospy_protobuf.osmosis.gamm.v1beta1.tx_pb2 as tx


class Transaction:
    _type_url = "/osmosis.gamm.v1beta1.MsgSwapExactAmountIn"

    def __init__(
            self,
            sender: Account,
            receipient: str,
            denom_in: str,
            amount_in: int,
            min_amount_out: int,
            routes: list
    ):
        self._amount_in = str(amount_in)
        self._denom_in = denom_in
        self._min_amount_out = str(min_amount_out)

        self._sender = sender.address()
        self._receipient = receipient
        self._routes = routes

    def format(self) -> (str, tx.MsgSwapExactAmountIn):
        msg = tx.MsgSwapExactAmountIn()
        msg.sender = self._sender
        for route in self._routes:
            _route = tx.SwapAmountInRoute()
            _route.poolId = int(route["pool_id"])
            _route.tokenOutDenom = route["denom"]
            msg.routes.append(_route)
        msg.tokenIn.denom = self._denom_in
        msg.tokenIn.amount = self._amount_in
        msg.tokenOutMinAmount = self._min_amount_out

        return (
            self._type_url,
            msg
        )
