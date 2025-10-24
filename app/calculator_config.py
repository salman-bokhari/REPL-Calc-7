from dotenv import load_dotenv
import os

load_dotenv()

def get_config():
    return {
        'LOG_DIR': os.getenv('CALCULATOR_LOG_DIR', 'logs'),
        'HISTORY_DIR': os.getenv('CALCULATOR_HISTORY_DIR', 'data'),
        'MAX_HISTORY': int(os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '100')),
        'AUTO_SAVE': os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower() in ('1','true','yes'),
        'PRECISION': int(os.getenv('CALCULATOR_PRECISION', '6')),
        'MAX_INPUT': float(os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e12')),
        'ENCODING': os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8'),
        'LOG_FILE': os.getenv('CALCULATOR_LOG_FILE', 'calculator.log'),
        'HISTORY_FILE': os.getenv('CALCULATOR_HISTORY_FILE', 'history.csv'),
    }
