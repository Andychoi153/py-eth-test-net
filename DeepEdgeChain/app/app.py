from pyethapp.app import EthApp
from pyethapp.accounts import Account

from ethereum.slogging import get_logger, configure_logging
from ethereum.pow.ethpow import mine

from itertools import count

configure_logging(':trace')
log = get_logger('test.console_service')


class EdgeChainApp(EthApp):

    def start(self):
        super(EdgeChainApp, self).start()
        log.debug('adding test accounts')

    def add_accounts(self, user_id, locked=False):
        account = Account.new(user_id)
        if locked:
            account.lock()
        self.services.accounts.add_account(account)

    def mine_next_block(self):
        """Mine until a valid nonce is found.
        :returns: the new head
        """
        log.debug('mining next block')
        block = self.services.chain.head_candidate
        chain = self.services.chain.chain

        delta_nonce = 10 ** 6
        for start_nonce in count(0, delta_nonce):
            bin_nonce, mixhash = mine(block.number, block.difficulty, block.mining_hash,
                                      start_nonce=start_nonce, rounds=delta_nonce)
            if bin_nonce:
                break
        self.services.pow.recv_found_nonce(bin_nonce, mixhash, block.mining_hash)
        if len(chain.time_queue) > 0:
            # If we mine two blocks within one second, pyethereum will
            # force the new block's timestamp to be in the future (see
            # ethereum1_setup_block()), and when we try to add that block
            # to the chain (via Chain.add_block()), it will be put in a
            # queue for later processing. Since we need to ensure the
            # block has been added before we continue the test, we
            # have to manually process the time queue.
            log.debug('block mined too fast, processing time queue')
            chain.process_time_queue(new_time=block.timestamp)
        log.debug('block mined')
        return chain.head
