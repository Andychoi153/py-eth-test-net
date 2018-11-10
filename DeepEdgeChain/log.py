from ethereum.slogging import get_logger, configure_logging


configure_logging(':trace')
log = get_logger('test.console_service')
