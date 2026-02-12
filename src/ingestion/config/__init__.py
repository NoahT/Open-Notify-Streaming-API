''' Init module for configuration. '''

from cfg_environ.config import Config, ConfigFacade


def get_config() -> Config:
  config = ConfigFacade('ingestion/config', 'development', 'default')

  return config
