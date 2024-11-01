# utils/logger.py

import logging
import logging.config
import yaml
import os

def get_logger(name: str) -> logging.Logger:
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f.read())
    if 'logging' in config:
        logging.config.dictConfig(config['logging'])
    else:
        logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)
