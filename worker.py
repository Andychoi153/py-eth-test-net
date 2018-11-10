from DeepEdgeChain.app.app import EdgeChainApp
from DeepEdgeChain.config import genesis_config
from DeepEdgeChain.log import log

from DeepEdgeChain.core.smart_contract import console_name_reg_contract
from DeepEdgeChain.core.transaction import send_transaction

from multiprocessing import Process


class Worker(Process):

    def __init__(self, dir):
        self._app = EdgeChainApp()
        self._dir = dir
        self._pool = []
        self._in_block = []

    def run(self):
        config, services= genesis_config.setting_config(self._app, self._dir)
        self.App = EdgeChainApp(config)

        for service in services:
            service.register_with_app(self.App)

        log.debug('starting app')
        self.App.start()


        # TODO: Interworking with MES, SES Requester controller
