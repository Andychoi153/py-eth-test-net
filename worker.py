from DeepEdgeChain.app.app import EdgeChainApp
from DeepEdgeChain.config import genesis_config
from DeepEdgeChain.log import log
from DeepEdgeChain.enum.enum import ENUMS
from DeepEdgeChain.config.contract_code import contract_code
from DeepEdgeChain.core.smart_contract import *

from multiprocessing import Process


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
        # TODO: Interworking with MES, SES Requester controller
