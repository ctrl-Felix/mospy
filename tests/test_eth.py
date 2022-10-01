from mospy import Account, Transaction

expected_eth_tx_bytes = "Cr8BCpgBChwvY29zbW9zLmJhbmsudjFiZXRhMS5Nc2dTZW5kEngKLGV2bW9zMTV4cnYzcmN5cjBrcG54Y3k3aDloZXJsdXJrZW1tc21mbjA0ZXVqEixldm1vczE1eHJ2M3JjeXIwa3BueGN5N2g5aGVybHVya2VtbXNtZm4wNGV1ahoaCgZhZXZtb3MSEDM1MDAwMDAwMDAwMDAwMDASIlRoZSBmaXJzdCBtb3NweSBldm1vcyB0cmFuc2FjdGlvbiESfgpZCk8KKC9ldGhlcm1pbnQuY3J5cHRvLnYxLmV0aHNlY3AyNTZrMS5QdWJLZXkSIwohAhSo8BPAmQ3ByGd8vGBMgpWdkHTx/8uwzo9dP2dvm+SeEgQKAggBGAESIQobCgZhZXZtb3MSETQwMDAwMDAwMDAwMDAwMDAwEICJehpA6LslOemKjb3KTW3lsyKHOUjNXEwQwoQfuEXySvP7yugweWqSOQgIa5fh9KLCwTgE66bj5SNppaJAQpK0c53Ipw=="


class TestEthClass:
    def test_eth_transaction_creation(self):
        account = Account(
            seed_phrase="law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style",
            hrp="evmos",
            slip44=60,
            eth=True,
            next_sequence=1,
            account_number=2154050,
        )

        tx = Transaction(
            account=account,
            gas=2000000,
            memo="The first mospy evmos transaction!",
            chain_id="evmos_9001-2",
        )

        tx.set_fee(
            denom="aevmos",
            amount=40000000000000000
        )
        tx.add_msg(
            tx_type="transfer",
            sender=account,
            receipient=account.address,
            amount=3500000000000000,
            denom="aevmos",
        )

        assert tx.get_tx_bytes_as_string() == expected_eth_tx_bytes