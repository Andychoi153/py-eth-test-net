from DeepEdgeChain.app import app
from DeepEdgeChain.config import genesis_config
from DeepEdgeChain.log import log
from multiprocessing import Process

from DeepEdgeChain.core.transaction import send_transaction
from DeepEdgeChain.core.smart_contract import *
from DeepEdgeChain.util.read_block_thread import ReadBlockThread
from DeepEdgeChain.config.contract_code import contract_code

import time
import os


class Test(Process):

    def __init__(self, dir):
        self._app = app.EdgeChainApp()
        self._dir = dir

    def run(self):
        os.environ['PATH'] = os.environ.get('PATH') + ':/home/haze/py-solc'
        config, services = genesis_config.setting_config(self._app, self._dir)
        test_App = app.EdgeChainApp(config)

        for service in services:
            service.register_with_app(test_App)

        log.debug('starting app')
        test_App.start()

        # This is for test module

        # Accounts listener, get Joseph, Andy as user_id
        # test_App.add_accounts('Joseph', locked=False)
        # test_App.add_accounts('Andy', locked=False)

        # Transaction listener
        # send_transaction(test_App, receiver_id=0, sender_id=1, value=1000)

        # Smart contract create
        example_solidity_code = '''contract NameReg  {
           event AddressRegistered(bytes32 indexed name, address indexed account);
           mapping (address => bytes32) toName;
           function register(bytes32 name) {
                   toName[msg.sender] = name;
                   AddressRegistered(name, msg.sender);
           }
        
           function resolve(address addr) constant returns (bytes32 name) {
                   return toName[addr];
           }
        }
        '''

        cnnOut = 2
        example_v2_version_code = contract_code

        # console_name_reg_contract(test_App,
        #                           example_solidity_code,
        #                           reg_id='Example',
        #                           sender_id='Joseph',
        #                           receiver_id='Andy')
        print('add_block')
        console_name_reg_contract_v2(test_App,
                                     example_v2_version_code,
                                     sender_id=0,
                                     receiver_id=1,
                                     hashData=hash(str(cnnOut)),
                                     name='hello',
                                     age=23,
                                     time_stamp='20181201'
                                     )
        print('add_block complete')
        ReadBlockThread(test_App)
        time.sleep(2)


if __name__ == '__main__':
    tmp_dir = os.path.dirname(__file__)

    test_pc = Test(tmp_dir)
    test_pc.run()
