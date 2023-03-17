import importlib

from mnemonic import Mnemonic
from mospy.utils import privkey_to_address
from mospy.utils import privkey_to_pubkey
from mospy.utils import seed_to_private_key
from mospy.utils import privkey_to_eth_address


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
        protobuf (str): Define which protobuf files to use. Cosmos, Evmos and Osmosis are built in and otherwise pass the raw package name (cosmospy-protobuf)
        eth (bool): Etermint compatibility mpde. If set to true the addresses and signatures will match the ethereum standard. Defaults to false to match the Cosmos standard.
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
        protobuf: str = "cosmos",
        eth: bool = False
    ):
        _protobuf_packages = {
            "cosmos": "cosmospy_protobuf",
            "osmosis": "osmosis_protobuf",
            "evmos": "evmos_protobuf",
        }
        _protobuf_package = (_protobuf_packages[protobuf.lower()]
                             if protobuf.lower() in _protobuf_packages.keys()
                             else protobuf)


        try:
            self.keys_pb2 = importlib.import_module(
                _protobuf_package + ".cosmos.crypto.secp256k1.keys_pb2")
        except AttributeError:
            raise ImportError(
                "It seems that you are importing conflicting protobuf files. Have sou set the protobuf attribute to specify your coin? Check out the documentation for more information."
            )
        except:
            raise ImportError(
                f"Couldn't import from {_protobuf_package}. Is the package installed? "
            )

        self._eth = eth
        self._slip44 = slip44
        self._hrp = hrp
        self._address_index = address_index
        self._next_sequence = next_sequence
        self._account_number = account_number

        if not seed_phrase and not private_key:
            self._seed_phrase = Mnemonic(language="english").generate(
                strength=256)
            self._private_key = seed_to_private_key(self._seed_phrase,
                                                    self._derivation_path())

        elif seed_phrase and not private_key:
            self._seed_phrase = seed_phrase
            self._private_key = seed_to_private_key(seed_phrase,
                                                    self._derivation_path())

        elif private_key and not seed_phrase:
            self._seed_phrase = None
            self._private_key = bytes.fromhex(private_key)

        else:
            raise AttributeError(
                "Please set only a private key or a seed phrase. Not both!")

    def _derivation_path(self, address_index: int = None):
        adr_id = self._address_index if not address_index else address_index
        params = {"slip44": self._slip44, "address_index": adr_id}
        return self._RAW_DERIVATION_PATH.format(**params)

    @property
    def address(self) -> str:
        """
        Current address which depends on the hrp and the private key.

        Returns:
            Address
        """
        if not self._seed_phrase:
            address = privkey_to_address(self._private_key, hrp=self._hrp) if not self._eth else privkey_to_eth_address(self._private_key, hrp=self._hrp)
        else:
            sub_private_key = seed_to_private_key(
                self._seed_phrase,
                self._derivation_path(address_index=self._address_index),
            )
            address = privkey_to_address(sub_private_key, hrp=self._hrp) if not self._eth else privkey_to_eth_address(sub_private_key, hrp=self._hrp)

        return address

    @property
    def eth_address(self) -> str:
        """
        Ethereum compatible address starting with 0x. Only available if Account is initialised with eth set to True.

        Returns:
            Address
        """
        if not self._eth:
            raise TypeError("Account hasn't been initialised with the eth mode set to true.")
        if not self._seed_phrase:
            address = privkey_to_eth_address(self._private_key)
        else:
            sub_private_key = seed_to_private_key(
                self._seed_phrase,
                self._derivation_path(address_index=self._address_index),
            )
            address = privkey_to_eth_address(sub_private_key)

        return address

    @property
    def seed_phrase(self) -> str:
        """
        Current Seed Phrase

        Returns:
            Seed Phrase
        """
        return self._seed_phrase

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
    def public_key(self) -> str:
        """
        Current public key which depends on the slip 44 param and the address index if the account is instantiated through a seed.

        Returns:
            Public Key
        """
        pubkey_bytes = privkey_to_pubkey(self.private_key)
        _pubkey = self.keys_pb2.PubKey()
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
            raise ValueError(
                "Can't the change the address index without provided seed")

    @property
    def hrp(self) -> str:
        """
        Current address prefix used by the Account.

        Args:
            hrp (str): New address prefix


        Returns:
            Address Prefix (hrp)
        """
        return self._hrp

    @hrp.setter
    def hrp(self, hrp: str) -> None:
        self._hrp = hrp

    @property
    def slip44(self) -> int:
        """"
        Set the Slip44 value. Cosmos defaults to 118

        Args:
            slip44 (int): New slip44 value as defined in the [slip44 registry](https://github.com/satoshilabs/slips/blob/master/slip-0044.md)

        Returns:
            Slip44

        """
        return self._slip44

    @slip44.setter
    def slip44(self, slip44: int) -> None:
        self._slip44 = slip44

    @property
    def eth(self) -> bool:
        """
        Change the eth compatibility mode. If you want to use Evmos you will need to set eth to true. Otherwise it defaults to False

        Args:
            eth (bool): ETH compatibility mode

        Returns:
            eth
          """
        return self._eth

    @eth.setter
    def eth(self, eth: bool):

        self._eth = eth