import pytest


def console_name_reg_contract(app, solidity_code, reg_id, sender_id, receiver_id):
    """
    exercise the console service with the NameReg contract found in The_Console wiki
    https://github.com/ethereum/pyethapp/wiki/The_Console#creating-contracts
    """

    from ethereum.tools import _solidity

    solidity = _solidity.get_solidity()
    if solidity is None:
        pytest.xfail("solidity not installed, not tested")
    else:
        # create the NameReg contract
        evm_code = solidity.compile(solidity_code)
        chain = app.services.chain.chain
        sender = app.services.accounts.unlocked_accounts[sender_id].address
        receiver = app.services.accounts.unlocked_accounts[receiver_id].address


        eth = app.services.console.console_locals['eth']
        tx = eth.transact(to=receiver, data=evm_code, startgas=500000, sender=sender)

        app.mine_next_block()
        creates = chain.head.transactions[0].creates

        # interact with the NameReg contract
        abi = solidity.mk_full_signature(solidity_code)
        namereg = eth.new_contract(abi, creates, sender=sender)
        namereg.register(reg_id, startgas=90000, gasprice=50 * 10**9)

        app.mine_next_block()
        result = namereg.resolve(sender)
        return tx, result
