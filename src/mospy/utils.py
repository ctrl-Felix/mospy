import hashlib

import ecdsa
import hdwallets
import bech32
from mnemonic import Mnemonic
from sha3 import keccak_256
import binascii


def seed_to_private_key(seed, derivation_path, passphrase: str = ""):
    seed_bytes = Mnemonic.to_seed(seed, passphrase=passphrase)
    hd_wallet = hdwallets.BIP32.from_seed(seed_bytes)
    # This can raise a `hdwallets.BIP32DerivationError` (which we alias so
    # that the same exception type is also in the `cosmospy` namespace).
    derived_privkey = hd_wallet.get_privkey_from_path(derivation_path)

    return derived_privkey


def privkey_to_pubkey(privkey: bytes, raw: bool = False) -> bytes:
    privkey_obj = ecdsa.SigningKey.from_string(privkey, curve=ecdsa.SECP256k1)
    pubkey_obj = privkey_obj.get_verifying_key()
    return pubkey_obj.to_string("raw") if raw else pubkey_obj.to_string("compressed")


def pubkey_to_address(pubkey: bytes, *, hrp: str) -> str:
    s = hashlib.new("sha256", pubkey).digest()
    r = hashlib.new("ripemd160", s).digest()
    five_bit_r = bech32.convertbits(r, 8, 5)
    assert five_bit_r is not None, "Unsuccessful bech32.convertbits call"
    return bech32.bech32_encode(hrp, five_bit_r)


def pubkey_to_eth_address(pubkey: bytes, *, hrp: str = None) -> str:
    k = keccak_256(pubkey).digest()[-20:].hex()
    if not hrp:
        return "0x" + k

    array = binascii.unhexlify(k)
    words = [x for x in array]
    bech32_words = bech32.convertbits(words, 8, 5)
    bech32_address = bech32.bech32_encode(hrp, bech32_words)
    return bech32_address


def privkey_to_eth_address(privkey: bytes, *, hrp: str = None) -> str:
    pubkey = privkey_to_pubkey(privkey, raw=True)
    return pubkey_to_eth_address(pubkey, hrp=hrp)


def privkey_to_address(privkey: bytes, *, hrp: str) -> str:
    pubkey = privkey_to_pubkey(privkey)
    return pubkey_to_address(pubkey, hrp=hrp)
