from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin
from mospy import Account
from mospy import Transaction

expected_tx_bytes = "CpABCo0BChwvY29zbW9zLmJhbmsudjFiZXRhMS5Nc2dTZW5kEm0KLWNvc21vczFxZWNuMHVqcDRydzhobjkzbDlqcHN4eXc0ZmEyOGE1MjM3YTRweBItY29zbW9zMXRrdjlycXV4cjg4cjdzbnJnNDJreGRqOWdzbmZ4eGcwMjhrdWg5Gg0KBXVhdG9tEgQxMDAwEmYKUApGCh8vY29zbW9zLmNyeXB0by5zZWNwMjU2azEuUHViS2V5EiMKIQIkQVvG9OBetDe7bYUgl2vwgbJFxmmGuquytVSEwhQ0uBIECgIIARgBEhIKDQoFdWF0b20SBDEwMDAQ6AcaQJqww3jDNgn4UMDpaFq34xPbdwTAsn4VnRvZ1rjYGCMEa6fDKnu9T5xlQV5IEpCDeMzmNBEhTo9QtcOIzjjPzes="

class TestTransactionClass:
    seed_phrase = "law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style"

    def test_transaction_creation(self):
        account = Account(
            seed_phrase=
            "law grab theory better athlete submit awkward hawk state wedding wave monkey audit blame fury wood tag rent furnace exotic jeans drift destroy style",
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
            receipient="cosmos1tkv9rquxr88r7snrg42kxdj9gsnfxxg028kuh9",
            amount=1000,
            denom="uatom",
        )


        tx_bytes = tx.get_tx_bytes_as_string()
        assert tx_bytes == expected_tx_bytes

