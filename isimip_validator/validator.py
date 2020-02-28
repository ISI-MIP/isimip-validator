import json
import logging
import os
import re
from urllib.parse import urlparse

import jsonschema

import requests

logger = logging.getLogger(__name__)


class Validator(object):

    def __init__(self, simulation_round, period, sector):
        self.simulation_round = simulation_round
        self.period = period
        self.sector = sector

        schema_path = '{}/{}/{}.json'.format(simulation_round, period, sector)

        pattern_bases = os.getenv('PATTERN_LOCATIONS', 'https://protocol.isimip.org/pattern/').split()
        pattern_json = self.fetch_json(pattern_bases, schema_path)
        self.pattern = '_'.join(pattern_json['file'])

        schema_bases = os.getenv('SCHEMA_LOCATIONS', 'https://protocol.isimip.org/schema/').split()
        self.schema = self.fetch_json(schema_bases, schema_path)

    def fetch_json(self, bases, path):
        for base in bases:
            if urlparse(base).scheme:
                response = requests.get(base + path)

                if response.status_code == 200:
                    return response.json()

            else:
                location = os.path.join(os.path.expanduser(base), path)
                if os.path.exists(location):
                    return json.loads(open(location).read())

        raise RuntimeError('{} not found in {}'.format(path, bases))

    def validate_file_name(self, file_name):
        logger.debug('file_name = %s', file_name)

        instance = {
            'identifiers': {}
        }

        if file_name.endswith('.nc') or file_name.endswith('.nc4'):
            m = re.match(self.pattern, file_name)
            if m:
                for key, value in m.groupdict().items():
                    if value is not None:
                        if value.isdigit():
                            instance['identifiers'][key] = int(value)
                        else:
                            instance['identifiers'][key] = value
            else:
                logger.error('could not match %s', file_name)

        try:
            jsonschema.validate(instance, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            logger.error('could not validate %s: %s', file_name, e)
