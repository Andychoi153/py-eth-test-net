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
            balance_amount = int(state.get_balance(account_info.address)/10**22)


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


class SendDetectData(Resource):
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
            # parser.add_argument('data', type=dict)
            parser.add_argument('hash', type=str)
            parser.add_argument('age', type=str)
            parser.add_argument('name', type=str)
            parser.add_argument('time_stamp', type=str)
            parser.add_argument('db_image', type=str)
            # log.debug(parser['ses_addr'])

            args = parser.parse_args()
            _eth_worker._pool.append({
                "Requester": args['req_addr'],
                "hash": args['hash'],
                "name": args['name'],
                "age": args['age'],
                "time_stamp": args['time_stamp']
            })

            address = args['req_addr']

            if address == 'REQUESTER1':
                _eth_worker._detected_image1 = args['db_image']
                _eth_worker._detected_image_sol1 = args['data']['sol']
                log.debug('receive packet from requester1')


            else:
                _eth_worker._detected_image2 = args['db_image']
                _eth_worker._detected_image_sol2 = args['data']['sol']

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
            temp = _eth_worker._pool
            for pool in temp:
                console_name_reg_contract_v2(App,
                                             contract_code,
                                             sender_id=ENUMS[pool['Requester']],
                                             receiver_id=ENUMS['MES'],
                                             hashData=pool['hash'],
                                             name=pool['name'],
                                             age=pool['age'],
                                             time_stamp=pool['time_stamp']
                                             )

            _eth_worker._in_block = _eth_worker._pool
            _eth_worker._pool = []

            mined_block = App.mine_next_block()
            for pool in temp:
                pool.update({
                    "Block hash": str(mined_block.hash)
                })

            _eth_worker._in_block.append(temp)
            _eth_worker._pool = []

            return {'status': 200}

        except Exception as e:
            return {'error': str(e)}


class ImagePacket(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('req_addr', type=str)
            parser.add_argument('image_packet', type=str)

            args = parser.parse_args()

            data = args['image_packet']

            address = args['req_addr']
            if address == 'REQUESTER1':
                _eth_worker._image_packet1 = data
                log.debug('get packet from req 1')

            else:
                _eth_worker._image_packet2 = data

            log.debug('get packet')

            return {'status': 200}

        except Exception as e:
            return {'error': str(e)}


class SendFrame(Resource):
    def post(self):
        try:
            temp_worker = _eth_worker

            return {'status': 200,
                    'image_packet1': temp_worker._image_packet1,
                    'detected_image1': temp_worker._detected_image1,
                    'sol1': temp_worker._detected_image_sol1,
                    'image_packet2': temp_worker._image_packet2,
                    'detected_image2': temp_worker._detected_image2,
                    'sol2': temp_worker._detected_image_sol2
                    }
        except Exception as e:
            return {'error': str(e)}


class SendBlockInfo(Resource):
    def post(self):
        try:
            pool = []
            for i in _eth_worker._pool:
                pool.append(str(i))
            in_block = []
            for i in _eth_worker._in_block:
                in_block.append(str(i))



            return {
                "status": 200,
                "pool_list":  pool,
                "in_block": in_block
            }
        except Exception as e:
            return {
                'error': str(e)
            }


import threading
import time


class MineBlock:
    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
        self.count = 0

    def run(self):
        while True:
            time.sleep(3)
            if len(_eth_worker._pool) > 0:
                App = _eth_worker.App
                temp = _eth_worker._pool
                for pool in temp:
                    console_name_reg_contract_v2(App,
                                                 contract_code,
                                                 sender_id=ENUMS[pool['Requester']],
                                                 receiver_id=ENUMS['MES'],
                                                 hashData=pool['hash'],
                                                 name=pool['name'],
                                                 age=pool['age'],
                                                 time_stamp=pool['time_stamp']
                                                 )

                _eth_worker._pool = []

                mined_block = App.mine_next_block()
                for pool in temp:
                    pool.update({
                        "Block hash": mined_block.hash
                    })

                    _eth_worker._in_block.append(pool)
                _eth_worker._pool = []
                # self.count = self.count +1
            time.sleep(2)
            _eth_worker._detected_image_sol1 = None
            _eth_worker._detected_image_sol2 = None
            _eth_worker._detected_image1 = None
            _eth_worker._detected_image2 = None
            # if self.count >2:
            #     break

MineBlock()

# For Frontend
api.add_resource(GetAccount, '/get_account')
api.add_resource(SendBlockInfo, '/send_block_info')
api.add_resource(SendFrame, '/send_frame')

# For Requester
api.add_resource(ImagePacket, '/image_packet')
api.add_resource(SendDetectData, '/send_detect_data')


# Not used
api.add_resource(GetTransactionPool, '/get_transaction_from_pool')
api.add_resource(GetTransactionFromBlockHeader, '/get_transaction_from_block_header')
api.add_resource(SendValueAccountToAccount, '/send_value_account_to_account')
api.add_resource(MiningBlock, '/mining_block')

if __name__ == '__main__':
    print('begin server')
    app.run(host='127.0.0.1')
