import os

from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
# from DeepEdgeChain.core.transaction import

from worker import Worker
from DeepEdgeChain.enum.enum import ENUMS
from DeepEdgeChain.core.transaction import send_transaction
from DeepEdgeChain.config.contract_code import contract_code
from DeepEdgeChain.core.smart_contract import *
from DeepEdgeChain.log import log

from ethereum.state import State


app = Flask(__name__)
api = Api(app)

os.environ['PATH'] = os.environ.get('PATH') + ':/home/haze/py-solc'

tmp_dir = os.path.dirname(__file__)
_eth_worker = Worker(tmp_dir)
_eth_worker.run()

# Register Account
# TODO: rename accounts to node id and make matching function


class GetAccount(Resource):
    def post(self):
        try:
            App = _eth_worker.App
            parser = reqparse.RequestParser()
            parser.add_argument('account', type=str)
            args = parser.parse_args()

            # do something this values
            _accounts = App.services.accounts.accounts
            account_index = ENUMS[args['account']]
            account_info = _accounts[account_index]

            block_head = App.services.chain.chain.head
            state = State(block_head.state_root, App.services.chain.chain.env)
            log.info(state.get_balance(account_info.address))
            balance_amount = float(state.get_balance(account_info.address))


            # TODO: account info parsing
            return {'status': 200,
                    'pubkey': account_info.pubkey[0],
                    'balance_amount': balance_amount}

        except Exception as e:
            return {'error': str(e)}


class GetTransactionPool(Resource):
    def post(self):
        try:
            transaction_pool = _eth_worker._pool
            App = _eth_worker.App

            send_transaction_pool_list = []

            if len(transaction_pool) > 0:
                _accounts = App.services.accounts.accounts
                # TODO: Branch which use contract or just send.
                for i in transaction_pool:
                    for j, account in enumerate(_accounts):
                        value = i.value
                        address = i.sender.encode('hex')
                        if address == account.address.encode('hex'):
                            sender_id = account.keys()[account.values().index(j)]
                        address = i.to.encode('hex')
                        if address == account.address.encode('hex'):
                            receiver_id = account.keys()[account.values().index(j)]

                        transact_info = {'value': value,
                                         'sender_id': sender_id,
                                         'receiver_id': receiver_id}
                        send_transaction_pool_list.append(transact_info)
                return {'status': 200,
                        'transaction_list': send_transaction_pool_list}
            else:
                return {'status': 200,
                        'transaction_list': None}

        except Exception as e:
            return {'error': str(e)}


class GetTransactionFromBlockHeader(Resource):
    def post(self):
        App = _eth_worker.App
        transaction_in_block_list = []

        try:
            transaction_in_block = _eth_worker._in_block
            if len(transaction_in_block) > 0:
                _accounts = App.services.accounts.accounts
                # TODO: Branch which use contract or just send.
                for i in transaction_in_block:
                    for j, account in enumerate(_accounts):
                        value = i.value
                        address = i.sender.encode('hex')
                        if address == account.address.encode('hex'):
                            sender_id = account.keys()[account.values().index(j)]
                        address = i.to.encode('hex')
                        if address == account.address.encode('hex'):
                            receiver_id = account.keys()[account.values().index(j)]

                        transact_info = {'value': value,
                                         'sender_id': sender_id,
                                         'receiver_id': receiver_id}
                        transaction_in_block_list.append(transact_info)

                        return {'status': 200,
                                'transaction_list': transaction_in_block_list}

            else:
                # TODO: transaction list None
                return {'status': 200,
                        'transaction_list': None}

        except Exception as e:
            return {'error': str(e)}


class SendValueAccountToAccount(Resource):
    def post(self):
        try:
            App = _eth_worker.App
            parser = reqparse.RequestParser()

            parser.add_argument('sender_account', type=str)
            parser.add_argument('receiver_account', type=str)
            parser.add_argument('value', type=int)

            args = parser.parse_args()
            sender_id = ENUMS[args['sender_account']]
            receiver_id = ENUMS[args['receiver_account']]
            value = args['value']

            tx = send_transaction(App, sender_id, receiver_id, value)
            _eth_worker._pool.append(tx)

            return {'status': 200}
        except Exception as e:
            return {'error': str(e)}


class CreateTransactionByContract(Resource):
    def post(self):
        # Example json format
        #{ 'req_addr': 'req-256',
        #  'data': { 'hash': 'has2h15hasdfjk',
        #            'sol': { 'name': 'John',
        #                     'age': 23}
        #           }
        #  'time_stamp': '2018-9-22 12:00:00'
        #}
        try:
            App = _eth_worker.App
            parser = reqparse.RequestParser()
            # parser.add_argument('ses_addr', type=str)
            # parser.add_argument('mes_addr', type=str)
            parser.add_argument('req_addr', type=str)
            parser.add_argument('data', type=dict)
            parser.add_argument('time_stamp', type=str)
            # log.debug(parser['ses_addr'])

            args = parser.parse_args()

            console_name_reg_contract_v2(App,
                                         contract_code,
                                         sender_id=ENUMS[args['req_addr']],
                                         receiver_id=ENUMS['MES'],
                                         hashData=args['data']['hash'],
                                         name=args['data']['sol']['name'],
                                         age=args['data']['sol']['age'],
                                         time_stamp=args['time_stamp']
                                         )

            log.debug(args)
            # TODO: Create Solidity compile code when begin worker
            # TODO: And name register to that Solidity code then call that code
            # TODO: And make transaction

            return {'status': 200}

        except Exception as e:
            return {'error': str(e)}


class MiningBlock(Resource):
    def post(self):
        try:
            App = _eth_worker.App
            App.mine_next_block()
            _eth_worker._in_block = _eth_worker._pool
            _eth_worker._pool = []
            return {'status': 200}

        except Exception as e:
            return {'error': str(e)}


api.add_resource(GetAccount, '/get_account')
api.add_resource(GetTransactionPool, '/get_transaction_from_pool')
api.add_resource(GetTransactionFromBlockHeader, '/get_transaction_from_block_header')
api.add_resource(SendValueAccountToAccount, '/send_value_account_to_account')
api.add_resource(CreateTransactionByContract, '/create_transaction_by_contract')
api.add_resource(MiningBlock, '/mining_block')


if __name__ == '__main__':
    print('begin server')
    app.run(host='127.0.0.1')
