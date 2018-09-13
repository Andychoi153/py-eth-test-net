import threading
import time
from DeepEdgeChain.log import log


class ReadBlockThread:
    def __init__(self, app):
        self.app = app
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            block_head_p = self.app.services.chain.chain.head
            log.info(block_head_p.header)
            time.sleep(5)
            peers = self.app.services.peermanager.peers
            log.info(peers)
