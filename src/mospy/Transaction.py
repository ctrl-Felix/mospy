import base64
import hashlib
import importlib

import ecdsa
from sha3 import keccak_256
from google.protobuf import any_pb2 as any
from mospy._transactions import ALL_TRANSACTION_HELPERS
from mospy.Account import Account

built_in_transactions = {}
for transaction_adapter in ALL_TRANSACTION_HELPERS:
    module = importlib.import_module("mospy._transactions." +
                                     transaction_adapter)
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
        protobuf (str): Define which protobuf files to use. Cosmos, Evmos and Osmosis are built in and otherwise pass the raw package name (cosmospy-protobuf)


    """

    def __init__(
        self,
        *,
        account: Account,
        gas: int,
        fee: object = None,
        memo: str = "",
        chain_id: str = "cosmoshub-4",
        protobuf: str = "cosmos",
        feegrant: str = ""
    ) -> None:

        _protobuf_packages = {
            "cosmos": "cosmospy_protobuf",
            "osmosis": "osmosis_protobuf",
            "evmos": "evmos_protobuf",
        }
        self._protobuf_package = (_protobuf_packages[protobuf.lower()]
                                  if protobuf.lower()
                                  in _protobuf_packages.keys() else protobuf)
        try:
            self.coin_pb2 = importlib.import_module(
                self._protobuf_package + ".cosmos.base.v1beta1.coin_pb2")
            self.tx_pb2 = importlib.import_module(self._protobuf_package +
                                                  ".cosmos.tx.v1beta1.tx_pb2")
        except:
            raise ImportError(
                f"Couldn't import from {self._protobuf_package}. Is the package installed?"
            )

        if fee and not isinstance(fee, (self.coin_pb2.Coin)):
            raise ValueError("The fee is not a valid.")

        self._account = account
        self._fee = fee
        self._gas = gas
        self._chain_id = chain_id
        self._tx_body = self.tx_pb2.TxBody()
        self._tx_body.memo = memo
        self._tx_raw = self.tx_pb2.TxRaw()
        self._feegrant = feegrant

    def add_msg(self, tx_type: str, **kwargs) -> None:
        """
        Add a pre-defined message to the tx body.

        Args:
            tx_type (str): Transaction type to match the transaction with the pre-defined ones
            **kwargs: Depending on the transaction type
        """
        msg_data = built_in_transactions[tx_type](
            protobuf_package=self._protobuf_package, **kwargs).format()
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
        self._fee = self.coin_pb2.Coin(amount=str(amount), denom=denom)

    def set_gas(self, gas: int):
        """
        Update the wanted gas for the transaction

        Args:
            gas: Gas
        """
        self._gas = gas

    def get_tx_bytes(self) -> bytes:
        """Sign the transaction and get the tx bytes which can be used to broadcast the transaction to the network.

        To broadcast the transaction through the REST endpoint use the ``get_tx_bytes_as_string()`` method instead

        Returns:
            tx_bytes (bytes): Transaction bytes
        """
        self._tx_raw = self.tx_pb2.TxRaw()
        self._tx_raw.body_bytes = self._tx_body.SerializeToString()
        self._tx_raw.auth_info_bytes = self._get_auth_info().SerializeToString(
        )
        self._tx_raw.signatures.append(self._get_signatures())
        raw_tx = self._tx_raw.SerializeToString()
        tx_bytes = bytes(raw_tx)
        return tx_bytes

    def get_tx_bytes_as_string(self) -> str:
        """Sign the transaction and get the base64 encoded tx bytes which can be used to broadcast the transaction to the network.

        Returns:
            tx_bytes (str): Transaction bytes
        """
        tx_bytes = self.get_tx_bytes()
        tx_b64 = base64.b64encode(tx_bytes).decode("utf-8")
        return tx_b64

    def _get_signatures(self):
        privkey = ecdsa.SigningKey.from_string(self._account.private_key,
                                               curve=ecdsa.SECP256k1)

        # Cosmos uses sha256 as main hashing function while ethereum uses keccak256
        hashfunc = hashlib.sha256 if not self._account.eth else keccak_256

        signature_compact = privkey.sign_deterministic(
            self._get_sign_doc().SerializeToString(),
            hashfunc=hashfunc,
            sigencode=ecdsa.util.sigencode_string_canonize,
        )
        return signature_compact

    def _get_sign_doc(self):
        sign_doc = self.tx_pb2.SignDoc()
        sign_doc.body_bytes = self._tx_body.SerializeToString()
        sign_doc.auth_info_bytes = self._get_auth_info().SerializeToString()
        sign_doc.chain_id = self._chain_id
        sign_doc.account_number = self._account.account_number
        return sign_doc

    def _get_auth_info(self):
        _auth_info = self.tx_pb2.AuthInfo()
        _auth_info.signer_infos.append(self._get_signer_infos())
        _auth_info.fee.gas_limit = self._gas
        _auth_info.fee.amount.append(self._fee)
        if self._feegrant:
            _auth_info.fee.granter = self._feegrant
        return _auth_info

    def _get_signer_infos(self):
        signer_infos = self.tx_pb2.SignerInfo()
        signer_infos.sequence = self._account.next_sequence
        signer_infos.public_key.Pack(self._account.public_key)
        if self._account.eth:
            signer_infos.public_key.type_url = "/ethermint.crypto.v1.ethsecp256k1.PubKey"
        else:
            signer_infos.public_key.type_url = "/cosmos.crypto.secp256k1.PubKey"
        signer_infos.mode_info.single.mode = 1
        return signer_infos
