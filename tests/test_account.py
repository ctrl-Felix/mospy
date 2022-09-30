from mospy import Account


class TestAccountClass:
    seed_phrase = "law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style"

    def test_wallet_creation_with_seed(self):
        account = Account(seed_phrase=self.seed_phrase, hrp="osmo")

        assert account.address == "osmo1qecn0ujp4rw8hn93l9jpsxyw4fa28a52e9w9h5"
    def test_wallet_creation_with_seed_for_eth(self):
        account = Account(seed_phrase=self.seed_phrase, hrp="evmos", eth=True, slip44=60)

        assert (account.address, account.eth_address) == ("evmos15xrv3rcyr0kpnxcy7h9herlurkemmsmfn04euj", "0xa186c88f041bec199b04f5cb7c8ffc1db3bdc369")

    def test_wallet_sub_account(self):
        account = Account(seed_phrase=self.seed_phrase,
                          address_index=2,
                          next_sequence=1)
        assert account.address == "cosmos1tkv9rquxr88r7snrg42kxdj9gsnfxxg028kuh9"

        account.increase_sequence(5)

        assert account.next_sequence == 6

    def test_wallet_generation(self):
        account = Account()

        assert(len(account.seed_phrase.split())) == 24
