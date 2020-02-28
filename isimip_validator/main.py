import argparse
import logging
import os

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

    # setup the Validator class
    validator = Validator(simulation_round, period, sector)

    # walk over files and validate
    if not os.path.exists(args.path):
        parser.error('Path does not exist {}'.format(args.path))

    for root, dirs, files in os.walk(args.path):
        for file_name in files:
            validator.validate_file_name(file_name)
