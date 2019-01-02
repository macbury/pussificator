import logging
import os
from ruamel.yaml import YAML

LOGGER = logging.getLogger('pussy')
logging.basicConfig(
  level=logging.INFO,
  format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

CONFIG_PATH = os.path.join('./', 'config.yaml')
LOGGER.info("Loading config: " + CONFIG_PATH)
CONFIG = YAML(typ='safe').load(open(CONFIG_PATH))