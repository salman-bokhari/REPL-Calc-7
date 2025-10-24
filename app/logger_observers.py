from abc import ABC, abstractmethod
from .logger import logger
import os
from .calculator_config import get_config
import pandas as pd

_cfg = get_config()
os.makedirs(_cfg['HISTORY_DIR'], exist_ok=True)
history_path = os.path.join(_cfg['HISTORY_DIR'], _cfg['HISTORY_FILE'])

class Observer(ABC):
    @abstractmethod
    def notify(self, calculation):
        pass

class LoggingObserver(Observer):
    def notify(self, calculation):
        logger.info(f'CALC {calculation.operation} {calculation.a} {calculation.b} = {calculation.result}')

class AutoSaveObserver(Observer):
    def notify(self, calculation):
        # append to CSV
        try:
            df = pd.DataFrame([calculation.to_dict()])
            if not os.path.exists(history_path):
                df.to_csv(history_path, index=False, encoding=_cfg['ENCODING'])
            else:
                df.to_csv(history_path, mode='a', header=False, index=False, encoding=_cfg['ENCODING'])
        except Exception as e:
            logger.error(f'AutoSave failed: {e}')
