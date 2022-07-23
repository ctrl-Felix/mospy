import hdwallets
from cosmospy_protobuf.cosmos.crypto.secp256k1 import keys_pb2 as keys
from mnemonic import Mnemonic

from mospy.utils import (privkey_to_address, privkey_to_pubkey,
                         seed_to_private_key)


class Account:
    """
    The account class can be instantiated through a seed or a private key. If nothing is provided it will create a new keyring and the params to work with the cosmos chain

    Note:
        * You can't provide a ``seed_phrase`` and a``private_key``
        * A ``readble`` method behaves is the getter for a Attribute (Example: ``hrp = account.hrp``)
        * A ``writable`` method is the setter for the Attribute (Example: ``account.hrp = "cosmos"``)
        * A method can be setter and getter at the same time. The Parameters description always refers to the setter while the Returns section belongs to the getter


    Args:
        seed_phrase (str): Seed phrase to derive private keys from
        private_key (str): Private key to instantiate the Account
        next_sequence (int): Sequence which will be used for transactions signed with this Account
        account_number (int): On-chain account number
        slip44 (int): Slip44 value
        hrp (str): Address Prefix
        address_index (int): Address index to get sub accounts for seed phrases (doesn't work when using a private key)

    """

    address: str
    """the address of the account derived by using the slip44 param, the hrp and the address_index"""

    _RAW_DERIVATION_PATH = "m/44'/{slip44}'/0'/0/{address_index}"

    def __init__(
        self,
        seed_phrase: str = None,
        private_key: str = None,
        next_sequence: int = None,
        account_number: int = None,
        slip44: int = 118,
        hrp: str = "cosmos",
        address_index: int = 0,
    ):
        self._slip44 = slip44
        self._hrp = hrp
        self._address_index = address_index
        self._next_sequence = next_sequence
        self._account_number = account_number

        if not seed_phrase and not private_key:
            self._seed_phrase = Mnemonic(language="english").generate(strength=256)
            self._private_key = seed_to_private_key(
                seed_phrase, self._derivation_path()
            )

        elif seed_phrase and not private_key:
            self._seed_phrase = seed_phrase
            self._private_key = seed_to_private_key(
                seed_phrase, self._derivation_path()
            )

        elif private_key and not seed_phrase:
            self._seed_phrase = None
            self._private_key = bytes.fromhex(private_key)

        else:
            raise AttributeError(
                "Please set only a private key or a seed phrase. Not both!"
            )

    def _derivation_path(self, address_index: int = None):
        adr_id = self._address_index if not address_index else address_index
        params = {"slip44": self._slip44, "address_index": adr_id}
        return self._RAW_DERIVATION_PATH.format(**params)

    @property
    def address(self) -> str:
        """
        Current address which depends on the hrp and the private key

        Returns:
            Private Key
        """
        if not self._seed_phrase:
            address = privkey_to_address(self._private_key, hrp=self._hrp)
        else:
            sub_private_key = seed_to_private_key(
                self._seed_phrase,
                self._derivation_path(address_index=self._address_index),
            )
            address = privkey_to_address(sub_private_key, hrp=self._hrp)

        return address

    @property
    def private_key(self) -> bytes:
        """
        Current private key which depends on the slip 44 param and the address index if the account is instantiated through a seed.

        Returns:
            Private Key
        """
        if self._seed_phrase:
            private_key = seed_to_private_key(
                self._seed_phrase,
                self._derivation_path(address_index=self._address_index),
            )
            return private_key
        else:
            return self._private_key

    @property
    def public_key(self) -> keys.PubKey:
        """
        Current public key which depends on the slip 44 param and the address index if the account is instantiated through a seed.

        Returns:
            Public Key
        """
        pubkey_bytes = privkey_to_pubkey(self.private_key)
        _pubkey = keys.PubKey()
        _pubkey.key = pubkey_bytes
        return _pubkey

    @property
    def account_number(self) -> int:
        """
        On-chain account number which will be assigned when the address receives coins for the first time.

        Args:
            account_number (int): Account Number
        Returns:
            Account number
        """
        return self._account_number

    @account_number.setter
    def account_number(self, account_number: int):
        self._account_number = account_number

    @property
    def next_sequence(self) -> int:
        """
        Sequence which will be used for transactions signed with this Account.

        Args:
            next_sequence (int): Next sequence (only when used as setter)

        Returns:
            Next Sequence
        """
        return self._next_sequence

    @next_sequence.setter
    def next_sequence(self, next_sequence):
        self._next_sequence = next_sequence

    def increase_sequence(self, change: int = 1) -> None:
        """
        Increase the sequence by ``change``

        Args:
            change (int): Value to increase the sequence
        """
        self._next_sequence += change

    @property
    def address_index(self):
        """
        Change the address index to use a sub account. This works only if a seed has been used to instantiate the Account.

        Args:
            address_index (int): New address index

        Returns:
            Address Index
        """
        return self._address_index

    @address_index.setter
    def address_index(self, address_index: int) -> None:

        if self._seed_phrase:
            self._DEFAULT_ADDRESS_INDEX = address_index
        else:
            raise ValueError("Can't the change the address index without provided seed")

    @property
    def hrp(self) -> str:
        """
        Current address prefix used by the Account.

        Returns:
            Address Prefix (hrp)
        """
        return self._hrp

    @hrp.setter
    def hrp(self, hrp: str) -> None:
        self._hrp = hrp

    @property
    def slip44(self, slip44: int) -> None:
        """
        Current slip44 value

        Args:
            slip44 (int): New slip44 value as defined in the [slip44 registry](https://github.com/satoshilabs/slips/blob/master/slip-0044.md)

        Returns:
            Slip44

        """
        return self._slip44

    @slip44.setter
    def set_slip44(self, slip44: int) -> None:
        self._slip44 = slip44
