from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin
from mospy import Account
from mospy import Transaction

expected_tx_bytes = "CpABCo0BChwvY29zbW9zLmJhbmsudjFiZXRhMS5Nc2dTZW5kEm0KLWNvc21vczFxZWNuMHVqcDRydzhobjkzbDlqcHN4eXc0ZmEyOGE1MjM3YTRweBItY29zbW9zMXRrdjlycXV4cjg4cjdzbnJnNDJreGRqOWdzbmZ4eGcwMjhrdWg5Gg0KBXVhdG9tEgQxMDAwEmYKUApGCh8vY29zbW9zLmNyeXB0by5zZWNwMjU2azEuUHViS2V5EiMKIQIkQVvG9OBetDe7bYUgl2vwgbJFxmmGuquytVSEwhQ0uBIECgIIARgBEhIKDQoFdWF0b20SBDEwMDAQ6AcaQJqww3jDNgn4UMDpaFq34xPbdwTAsn4VnRvZ1rjYGCMEa6fDKnu9T5xlQV5IEpCDeMzmNBEhTo9QtcOIzjjPzes="
expected_tx_bytes2 = "Ck8KTQoZL2VseXMuc3RhYmxlc3Rha2UuTXNnQm9uZBIwCitlbHlzMXFlY24wdWpwNHJ3OGhuOTNsOWpwc3h5dzRmYTI4YTUyMzd5anZ5EgExEmYKUApGCh8vY29zbW9zLmNyeXB0by5zZWNwMjU2azEuUHViS2V5EiMKIQIkQVvG9OBetDe7bYUgl2vwgbJFxmmGuquytVSEwhQ0uBIECgIIARgFEhIKDAoFdWVseXMSAzEyNRCgwh4aQLoR5z302GPGh9YfAS4lM/JeRLrkkNW0lEdc94mkYG3qTiWuJMLDL5653PkJ/w9qZOBjOcZn1huVDu7XTzUSajo="
class TestTransactionClass:
    seed_phrase = "law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style"

    def test_transaction_creation(self):
        account = Account(
            seed_phrase=self.seed_phrase,
            account_number=1,
            next_sequence=1,
        )

        fee = Coin(denom="uatom", amount="1000")

        tx = Transaction(
            account=account,
            fee=fee,
            gas=1000,
        )

        tx.add_msg(
            tx_type="transfer",
            sender=account,
            recipient="cosmos1tkv9rquxr88r7snrg42kxdj9gsnfxxg028kuh9",
            amount=1000,
            denom="uatom",
        )


        tx_bytes = tx.get_tx_bytes_as_string()
        assert tx_bytes == expected_tx_bytes

    def test_transaction_creation_from_dict(self):
        account = Account(
            seed_phrase=self.seed_phrase,
            hrp='elys',
            account_number=114923,
            next_sequence=5
        )
        tx = Transaction(
            account=account,
            chain_id='elystestnet-1',
            gas=500000,
        )

        msg = {
            "creator": account.address,
            "amount": "1"
        }

        tx.add_dict_msg(msg, type_url="/elys.stablestake.MsgBond")


        tx.set_fee(
            amount=125,
            denom="uelys"
        )

        tx_bytes = tx.get_tx_bytes_as_string()
        assert tx_bytes == expected_tx_bytes2
