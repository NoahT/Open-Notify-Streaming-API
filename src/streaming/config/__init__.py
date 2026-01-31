''' Init for configuration with cfg_environ '''

from cfg_environ.config import Config, ConfigFacade

CONFIG_PATH = 'streaming/config'
CONFIG_ENV = 'development'
CONFIG_ENV_DEFAULT = 'default'


def get_config() -> Config:
  config = ConfigFacade(config_path=CONFIG_PATH,
                        config_env=CONFIG_ENV,
                        config_env_default=CONFIG_ENV_DEFAULT)

  return config
