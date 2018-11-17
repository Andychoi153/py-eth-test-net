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
        # evm_code = _solidity.compile_code(solidity_code)
        evm_code = solidity.compile(solidity_code)
        abi = solidity.mk_full_signature(solidity_code)
        sender = app.services.accounts.unlocked_accounts[0].address

        eth = app.services.console.console_locals['eth']
        print(evm_code)
        tx = eth.transact(to='', data=evm_code, startgas=500000, sender=sender)
        app.mine_next_block()
        # creates = chain.head.transactions[0].creates

        # interact with the NameReg contract
        # abi = solidity.mk_full_signature(solidity_code)
        namereg = eth.new_contract(abi, tx.creates,sender)
        tx = namereg.register('alice')

        print(eth.find_transaction(tx))

        app.mine_next_block()
        print(eth.find_transaction(tx))
        result = namereg.resolve(sender)
        print(result.encode('hex'))
        return tx, result


def console_name_reg_contract_v2(app,
                                 solidity_code,
                                 sender_id,
                                 receiver_id,
                                 hashData,
                                 name,
                                 age,
                                 time_stamp):
    """
    :param app:
    :param solidity_code:
    :param reg_id:
    :param sender_id:
    :param receiver_id:
    :return:
    {'req_addr': str(addr[0]) + ':' + str(addr[1]),
        'data': {'hash': hash(str(cnnOut)),
                 'sol': {'name': 'hello',
                         'age': 'goodmorning'}
                 },
        'time_stamp': '201821199'
    }
    """

    from ethereum.tools import _solidity

    solidity = _solidity.get_solidity()
    if solidity is None:
        pytest.xfail("solidity not installed, not tested")
    else:
        # create the NameReg contract
        chain = app.services.chain.chain
        # sender: requester id
        sender = app.services.accounts.unlocked_accounts[sender_id].address
        receiver = app.services.accounts.unlocked_accounts[receiver_id].address

        evm_code = solidity.compile(solidity_code)
        abi = solidity.mk_full_signature(solidity_code)

        eth = app.services.console.console_locals['eth']
        tx = eth.transact(to='',
                          data=evm_code,
                          startgas=500000,
                          sender=sender.encode('hex'))
        app.mine_next_block()

        print(sender)
        print(sender.encode('hex'))
        print(receiver)
        print(receiver.encode('hex'))

        # Bug in the tx.address error
        # https://github.com/ethereum/pyethapp/issues/76
        # please modify the code in console_service.py in pyethapp

        # interact with the NameReg contract
        # abi = solidity.mk_full_signature(solidity_code)
        namereg = eth.new_contract(abi, tx.creates, sender)
        tx = namereg.writeResult(hashData,
                                 name,
                                 age,
                                 time_stamp)

        # print(address_test)
        app.mine_next_block()
        # result = namereg.resolve(sender)
        return tx
