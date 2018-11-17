from pyethapp.accounts import AccountsService, mk_random_privkey
from pyethapp.db_service import DBService
from pyethapp.eth_service import ChainService
from pyethapp.pow_service import PoWService
from pyethapp.console_service import Console
from pyethapp.config import update_config_with_defaults, get_default_config

from ethereum.utils import encode_hex
from ethereum.config import default_config
from ethereum.tools import tester

from devp2p.peermanager import PeerManager

import json
import socket
import fcntl
import struct
import os


dir = os.path.dirname(os.path.realpath('__file__'))
json_data = open(dir+'/DeepEdgeChain/config/application.config.json').read()
config = json.loads(json_data)


def setting_config(app, tmpdir, bootstrap_nodes=None):
    # bootstrap_nodes example: ['enode://288b97262895b1c7ec61cf314c2e2004407d0a5dc77566877aad
    #                            1f2a36659c8b698f4b56fd06c4a0c0bf007b4cfb3e7122d907da3b005fa
    #                            90e724441902eb19e
    #                            @192.168.43.149:30303']

    config['data_dir'] = str(tmpdir)

    if bootstrap_nodes is not None:
        config['p2p']['bootstrap_nodes'] = bootstrap_nodes
        config['discovery']['bootstrap_nodes'] = bootstrap_nodes

    config['node'] = {'privkey_hex': encode_hex(mk_random_privkey())}
    config['pow'] = {'activated': True}
    config['eth']['network_id'] = 1337
    config['eth']['block']['GENESIS_INITIAL_ALLOC'] = {
                    encode_hex(tester.accounts[0]): {'balance': 10**24},
                    encode_hex(tester.accounts[1]): {'balance': 10**24},
                    encode_hex(tester.accounts[2]): {'balance': 10**24},
                    encode_hex(tester.accounts[3]): {'balance': 10 **24},

    }
    config['p2p']['listen_host'] = '127.0.0.1'

    services = [DBService, AccountsService, PeerManager, ChainService, PoWService, Console]
    update_config_with_defaults(config, get_default_config([app] + services))
    update_config_with_defaults(config, {'eth': {'block': default_config}})

    return config, services
