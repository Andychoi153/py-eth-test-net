from ethereum.state import State


def send_transaction(app, sender_id, receiver_id,value):
    chain = app.services.chain.chain
    chainservice = app.services.chain

    hc_state = State(chainservice.head_candidate.state_root, chain.env)
    sender = app.services.accounts.unlocked_accounts[sender_id].address
    receiver = app.services.accounts.unlocked_accounts[receiver_id].address
    print sender
    print type(sender)

    assert hc_state.get_balance(sender) > 0

    eth = app.services.console.console_locals['eth']
    tx = eth.transact(to=receiver, value=value, startgas=500000, sender=sender)

    app.mine_next_block()
    return tx
