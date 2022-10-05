from mospy import Account, Transaction
from mospy.clients import HTTPClient

SEED = ""

account = Account(
    seed_phrase=SEED,
)

client = HTTPClient(api="https://api.cosmoshub.interbloc.org")

client.load_account_data(account)

tx = Transaction(
    account=account,
    chain_id="cosmoshub-4",
    gas=250000
)

tx.add_msg('withdraw_reward', delegator=account.address,
           validator="cosmosvaloper1kgddca7qj96z0qcxr2c45z73cfl0c75p7f3s2e")
tx.add_msg('undelegate', delegator=account.address, validator="cosmosvaloper1kgddca7qj96z0qcxr2c45z73cfl0c75p7f3s2e",
           amount=500000, denom="uatom")
tx.add_msg('delegate', delegator=account.address, validator="cosmosvaloper1kgddca7qj96z0qcxr2c45z73cfl0c75p7f3s2e",
           amount=500000, denom="uatom")
tx.set_fee(
    amount=750,
    denom="uatom"
)
x = client.broadcast_transaction(transaction=tx)
print(x)
