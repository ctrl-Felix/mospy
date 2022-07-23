from mospy import Account
from mospy.clients import HTTPClient

class TestHTTPClientClass:
    seed_phrase = "law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style"

    def test_account_data_loading(self):
        account = Account(
            seed_phrase=self.seed_phrase
        )

        client = HTTPClient()

        client.load_account_data(account)

        assert account.account_number == 1257460

        assert account.next_sequence >= 1
