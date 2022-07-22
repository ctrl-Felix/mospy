from mospy.Account import Account

class TestAccountClass:
    seed_phrase = "law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style"

    def test_wallet_creation_with_seed(self):
        account = Account(
            seed_phrase=self.seed_phrase
        )

        assert account.address() == "cosmos1qecn0ujp4rw8hn93l9jpsxyw4fa28a5237a4px"

    def test_wallet_sub_account(self):
        account = Account(
            seed_phrase=self.seed_phrase,
            address_index=2
        )

        assert account.address() == "cosmos1tkv9rquxr88r7snrg42kxdj9gsnfxxg028kuh9"

