''' Init module for configuration. '''

from cfg_environ.config import ConfigFacade

config = ConfigFacade(config_path='test/integration_tests/ingestion/config',
                      config_env='test',
                      config_env_default='default')
