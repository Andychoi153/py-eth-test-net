from DeepEdgeChain.app.app import EdgeChainApp
from DeepEdgeChain.config import genesis_config
from DeepEdgeChain.log import log
from DeepEdgeChain.enum.enum import ENUMS
from DeepEdgeChain.config.contract_code import contract_code
from DeepEdgeChain.core.smart_contract import *

from multiprocessing import Process
import threading
import time

class Worker(Process):

    def __init__(self, dir):
        self._app = EdgeChainApp()
        self._dir = dir
        self._pool = []
        self._in_block = []
        self._image_packet1 = None
        self._detected_image1 = None
        self._detected_image_sol1 = None
        self._image_packet2 = None
        self._detected_image2 = None
        self._detected_image_sol2 = None

    def run(self):
        config, services= genesis_config.setting_config(self._app, self._dir)
        self.App = EdgeChainApp(config)

        for service in services:
            service.register_with_app(self.App)

        log.debug('starting app')
        self.App.start()
        MineBlock(self)
        # TODO: Interworking with MES, SES Requester controller


class MineBlock:
    def __init__(self, worker):
        self.worker = worker
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            if len(self.worker._pool) > 0:
                App = self.worker.App
                temp = self.worker._pool
                for pool in temp:
                    console_name_reg_contract_v2(App,
                                                 contract_code,
                                                 sender_id=ENUMS[pool['Requester']],
                                                 receiver_id=ENUMS['MES'],
                                                 hashData=str(pool['data']['hash']),
                                                 name=str(pool['data']['solution']['name']),
                                                 age=str(pool['data']['solution']['age']),
                                                 time_stamp=pool['time_stamp']
                                                 )

                self.worker._in_block = self.worker._pool
                self.worker._pool = []

                mined_block = App.mine_next_block()
                for pool in temp:
                    pool.update({
                        'Block hash': mined_block.hash
                    })

                self.worker._in_block.append(temp)
                self.worker._pool = []
