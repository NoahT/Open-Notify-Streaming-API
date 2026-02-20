''' Init for configuration with cfg_environ '''

import os

from cfg_environ.config import Config, ConfigFacade

CONFIG_PATH = 'streaming/config'
CONFIG_ENV = 'development'
CONFIG_ENV_DEFAULT = 'default'


def get_config() -> Config:
  config_env = os.getenv('ENVIRONMENT') or CONFIG_ENV
  config = ConfigFacade(config_path=CONFIG_PATH,
                        config_env=config_env,
                        config_env_default=CONFIG_ENV_DEFAULT)

  return config
