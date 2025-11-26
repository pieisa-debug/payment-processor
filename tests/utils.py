# utils.py

import logging
import os
import json

from payment_processor.config import Config

def load_config():
    config_path = os.environ.get('CONFIG_PATH', 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    return Config(config)

def setup_logger(logger_name, log_level, log_file):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def hash_string(s):
    import hashlib
    return hashlib.sha256(s.encode()).hexdigest()

def validate_credit_card(number):
    if not isinstance(number, str):
        raise ValueError('Invalid credit card number')
    digits = number.replace(' ', '')
    if len(digits) < 13 or len(digits) > 16:
        return False
    if not digits.isdigit():
        return False
    sum_of_digits = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 0:
            sum_of_digits += int(digit)
        else:
            doubled_digit = int(digit) * 2
            if doubled_digit > 9:
                doubled_digit -= 9
            sum_of_digits += doubled_digit
    return sum_of_digits % 10 == 0