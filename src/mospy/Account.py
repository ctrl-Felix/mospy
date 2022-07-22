from cosmospy_protobuf.cosmos.crypto.secp256k1 import keys_pb2 as keys
from mnemonic import Mnemonic
import hdwallets

from mospy.utils import privkey_to_address, seed_to_private_key, privkey_to_pubkey


class Account:
    _RAW_DERIVATION_PATH = "m/44'/{slip44}'/0'/0/{address_index}"
    _DEFAULT_BECH32_HRP = "cosmos"
    _DEFAULT_ADDRESS_INDEX = 0

    def __init__(
            self,
            seed_phrase: str = None,
            private_key: str = None,
            slip44: int = 118,
            hrp: str = _DEFAULT_BECH32_HRP,
            address_index: int = _DEFAULT_ADDRESS_INDEX,
            next_sequence: int = None,
            account_number: int = None

    ):
        self._slip44 = slip44
        self._hrp = hrp
        self._address_index = address_index
        self._next_sequence = next_sequence
        self._account_number = account_number

        if not seed_phrase and not private_key:
            self._seed_phrase = Mnemonic(language="english").generate(strength=256)
            self._private_key = seed_to_private_key(seed_phrase, self._derivation_path())

        elif seed_phrase and not private_key:
            self._seed_phrase = seed_phrase
            self._private_key = seed_to_private_key(seed_phrase, self._derivation_path())

        elif private_key and not seed_phrase:
            self._seed_phrase = None
            self._private_key = bytes.fromhex(private_key)

        else:
            raise AttributeError("Please set only a private key or a seed phrase. Not both!")

    def _derivation_path(self, address_index: int = None):
        adr_id = self._address_index if not address_index else address_index
        params = {"slip44": self._slip44, "address_index": adr_id}
        return self._RAW_DERIVATION_PATH.format(**params)

    def address(self, hrp: str = None, address_index: int = None) -> str:
        if not self._seed_phrase and address_index: # The address_index flag is only working if a seed is provided
            raise Exception("This is only possible when the account has been initialised through a seed")

        adr_prefix = self._hrp if not hrp else hrp
        adr_id = self._address_index if not address_index else address_index
        if adr_id == 0:
            address = privkey_to_address(self._private_key, hrp=adr_prefix)
        else:
            sub_private_key = seed_to_private_key(self._seed_phrase, self._derivation_path(address_index=adr_id))
            address = privkey_to_address(sub_private_key, hrp=adr_prefix)

        return address

    def private_key(self, address_index: int = None) -> bytes:
        adr_id = self._address_index if not address_index else address_index
        if self._seed_phrase:
            private_key = seed_to_private_key(self._seed_phrase, self._derivation_path(address_index=adr_id))
            return private_key
        else:
            return self._private_key

    def set_address_index(self, address_index: int) -> None:
        """Change the address index to use a sub account. This works only if a seed is used"""
        if self._seed_phrase:
            self._DEFAULT_ADDRESS_INDEX = address_index
        else:
            raise ValueError("Can't the change the address index without provided seed")

    def pub_key(self) -> keys.PubKey:
        pubkey_bytes = privkey_to_pubkey(self._private_key)
        _pubkey = keys.PubKey()
        _pubkey.key = pubkey_bytes
        return _pubkey

    def account_number(self):
        return self._account_number

    def next_sequence(self):
        return self._next_sequence

    def increase_sequence(self, amount: int = 1):
        self._next_sequence += amount
