import base64
import hashlib
import importlib

import ecdsa

from mospy.Account import Account

import cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 as coin
import cosmospy_protobuf.cosmos.tx.v1beta1.tx_pb2 as tx
from google.protobuf import any_pb2 as any
from mospy._transactions import ALL_TRANSACTION_HELPERS

built_in_transactions = {}
for transaction_adapter in ALL_TRANSACTION_HELPERS:
    module = importlib.import_module("mospy._transactions." + transaction_adapter)
    adapter = getattr(module, "Transaction")
    built_in_transactions[adapter.name] = adapter


class Transaction:
    """Class to create and sign a transaction
    Args:
        account (Account): Account object to sign this transaction
        gas (int): Gas unit for this transaction
        fee (coin): The fee to pay for this transaction (This can also be added later through the ``set_fee`` method)
        memo (str): Memo
        chain_id (str): Chain-Id "cosmoshub-4",

    """

    def __init__(
        self,
        *,
        account: Account,
        gas: int,
        fee: coin = None,
        memo: str = "",
        chain_id: str = "cosmoshub-4",
    ) -> None:

        self._account = account
        self._fee = fee
        self._gas = gas
        self._chain_id = chain_id
        self._tx_body = tx.TxBody()
        self._tx_body.memo = memo
        self._tx_raw = tx.TxRaw()

    def add_msg(self, tx_type: str, **kwargs) -> None:
        """
        Add a pre-defined message to the tx body.

        Args:
            tx_type (str): Transaction type to match the transaction with the pre-defined ones
            **kwargs: Depending on the transaction type
        """
        msg_data = built_in_transactions[tx_type](**kwargs).format()
        self.add_raw_msg(msg_data[1], type_url=msg_data[0])

    def add_raw_msg(self, unpacked_msg, type_url: str) -> None:
        """
        Add a message to the tx body manually.

        Args:
            unpacked_msg: Transaction data
            type_url: Type url for the transaction
        """
        msg_any = any.Any()
        msg_any.Pack(unpacked_msg)
        msg_any.type_url = type_url
        self._tx_body.messages.append(msg_any)

    def set_fee(self, amount: int, denom: str = "uatom"):
        """
        Set the fee manually

        Args:
            amount: Amount
            denom: Denom
        """
        self._fee = coin.Coin(amount=str(amount), denom=denom)

    def get_tx_bytes(self) -> str:
        """Sign the transaction and get the tx bytes which can be then used to broadcast the transaction to the network.

        Returns:
            tx_bytes (str): Transaction bytes
        """
        self._tx_raw.body_bytes = self._tx_body.SerializeToString()
        self._tx_raw.auth_info_bytes = self._get_auth_info().SerializeToString()
        self._tx_raw.signatures.append(self._get_signatures())
        raw_tx = self._tx_raw.SerializeToString()
        tx_bytes = bytes(raw_tx)
        tx_b64 = base64.b64encode(tx_bytes).decode("utf-8")
        return tx_b64

    def _get_signatures(self):
        privkey = ecdsa.SigningKey.from_string(
            self._account.private_key, curve=ecdsa.SECP256k1
        )
        signature_compact = privkey.sign_deterministic(
            self._get_sign_doc().SerializeToString(),
            hashfunc=hashlib.sha256,
            sigencode=ecdsa.util.sigencode_string_canonize,
        )
        return signature_compact

    def _get_sign_doc(self):
        sign_doc = tx.SignDoc()
        sign_doc.body_bytes = self._tx_body.SerializeToString()
        sign_doc.auth_info_bytes = self._get_auth_info().SerializeToString()
        sign_doc.chain_id = self._chain_id
        sign_doc.account_number = self._account.account_number
        return sign_doc

    def _get_auth_info(self):
        _auth_info = tx.AuthInfo()
        _auth_info.signer_infos.append(self._get_signer_infos())
        _auth_info.fee.gas_limit = self._gas
        _auth_info.fee.amount.append(self._fee)
        return _auth_info

    def _get_signer_infos(self):
        signer_infos = tx.SignerInfo()
        signer_infos.sequence = self._account.next_sequence
        signer_infos.public_key.Pack(self._account.public_key)
        signer_infos.public_key.type_url = "/cosmos.crypto.secp256k1.PubKey"
        signer_infos.mode_info.single.mode = 1
        return signer_infos
