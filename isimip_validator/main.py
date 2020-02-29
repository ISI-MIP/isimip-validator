import argparse
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from .validator import Validator


def main():
    # setup environment from the .env file
    load_dotenv(os.path.join(os.getcwd(), '.env'))

    # setup logging
    log_level = os.getenv('LOG_LEVEL', 'ERROR')
    logging.basicConfig(level=log_level)

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('simulation_round')
    parser.add_argument('sector')
    parser.add_argument('path', help='path to the file .nc to check')
    args = parser.parse_args()

    simulation_round = 'ISIMIP' + args.simulation_round.lower().replace('isimip', '')
    period = 'OutputData'
    sector = args.sector.lower()
    path = Path(args.path)

    # setup the Validator class
    validator = Validator(simulation_round, period, sector)

    # walk over files and validate
    if not path.exists():
        parser.error('Path does not exist {}'.format(path))

    if path.is_file():
        validator.validate(args.path)
    else:
        for root, dirs, files in os.walk(path):
            for file_name in files:
                file_path = Path(root) / file_name
                validator.validate(file_path)
