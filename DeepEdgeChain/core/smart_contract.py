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
        evm_code = _solidity.compile_code(solidity_code)
        chain = app.services.chain.chain
        sender = app.services.accounts.unlocked_accounts[0].address
        receiver = app.services.accounts.unlocked_accounts[1].address

        eth = app.services.console.console_locals['eth']
        print(evm_code)
        tx = eth.transact(to=receiver, data=evm_code['<stdin>:NameReg']['bin_hex'], startgas=500000, sender=sender)

        app.mine_next_block()
        creates = chain.head.transactions[0].creates

        # interact with the NameReg contract
        # abi = solidity.mk_full_signature(solidity_code)
        abi = evm_code['<stdin>:NameReg']['abi']
        namereg = eth.new_contract(abi, creates)
        namereg.register(reg_id, startgas=90000, gasprice=50 * 10**9)

        app.mine_next_block()
        result = namereg.resolve(sender)
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

        value1= sender.encode('hex')
        value2 = receiver.encode('hex')

        evm_code = _solidity.compile_code(solidity_code)#, extra_args=receiver)

        eth = app.services.console.console_locals['eth']
        tx = eth.transact(to='', data=evm_code['<stdin>:DataStruct']['bin_hex'], startgas=500000000, sender=sender)

        # interact with the NameReg contract
        # abi = solidity.mk_full_signature(solidity_code)
        abi = evm_code['<stdin>:DataStruct']['abi']
        namereg = eth.new_contract(abi, tx.creates, sender=sender)
        namereg.setMESAddress(receiver)
        namereg.writeResult(hashData, name, age, time_stamp)
        address_test = namereg.getMESAddress()
        hash_test = namereg.getHashData()
        name_test = namereg.getName()
        age_test = namereg.getAge()
        time_test = namereg.getTime()
        print(hash_test)
        print(age_test)
        print(name_test)
        print(time_test)

        namereg.confirmResult()
        print(address_test)
        app.mine_next_block()
        # result = namereg.resolve(sender)
        return tx
