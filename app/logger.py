import logging, os
from .calculator_config import get_config

_cfg = get_config()
os.makedirs(_cfg['LOG_DIR'], exist_ok=True)
log_path = os.path.join(_cfg['LOG_DIR'], _cfg['LOG_FILE'])

logger = logging.getLogger('calculator')
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    fh = logging.FileHandler(log_path, encoding=_cfg['ENCODING'])
    fmt = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    fh.setFormatter(fmt)
    logger.addHandler(fh)
