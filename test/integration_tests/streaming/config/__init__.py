''' Init to add integration test configuration '''
from cfg_environ.config import ConfigFacade

config = ConfigFacade(config_path='./test/integration_tests/streaming/config',
                      config_env='test',
                      config_env_default='default')
