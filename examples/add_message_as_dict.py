from mospy import Account, Transaction
from mospy.clients import HTTPClient

account = Account(
    seed_phrase="",
    hrp='elys'
)
tx = Transaction(
    account=account,
    chain_id='elystestnet-1',
    gas=800000,
)


msg = {
    "creator": account.address,
    "amount": "1000"
}


tx.add_dict_msg(msg, type_url="/elys.stablestake.MsgBond")

client = HTTPClient(
    api="https://api.testnet.elys.network"
)

tx.set_fee(
    amount=100,
    denom="uelys"
)

client.load_account_data(account=account)
response = client.broadcast_transaction(transaction=tx)
