import json
import logging
import os
import re
from pathlib import Path
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
        self.pattern = self.fetch_json(pattern_bases, schema_path).get('file')

        logger.debug('pattern = %s', self.pattern)

        schema_bases = os.getenv('SCHEMA_LOCATIONS', 'https://protocol.isimip.org/schema/').split()
        self.schema = self.fetch_json(schema_bases, schema_path)

        logger.debug('schema = %s', self.schema)

    def fetch_json(self, bases, path):
        for base in bases:
            if urlparse(base).scheme:
                response = requests.get(base + path)

                if response.status_code == 200:
                    return response.json()

            else:
                location = Path(base) / path
                if location.exists():
                    return json.loads(open(location).read())

        raise RuntimeError('{} not found in {}'.format(path, bases))

    def validate(self, file_path):
        logger.info('file_path = %s', file_path)

        instance = {}
        m = re.match(self.pattern, file_path.name)
        if m:
            for key, value in m.groupdict().items():
                if value is not None:
                    if value.isdigit():
                        instance[key] = int(value)
                    else:
                        instance[key] = value
        else:
            logger.error('could not match %s', file_path)

        logger.debug('instance = %s', instance)

        try:
            jsonschema.validate(instance, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            logger.error('could not validate %s: %s', file_path, e)
