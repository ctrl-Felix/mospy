from mospy import Transaction
from mospy.clients import HTTPClient

from src.mospy import Account

# As the account query returns a different json than the standard cosmos one evmos won't be compatible with the
# client.load_account() function
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

client = HTTPClient(api="https://api.evmos.interbloc.org")
tx_response = client.broadcast_transaction(transaction=tx)