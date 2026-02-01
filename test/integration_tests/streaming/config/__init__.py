from cfg_environ.config import ConfigFacade

config = ConfigFacade(
    config_path='./test/integration_tests/streaming/client/subscriber',
    config_env='test',
    config_env_default='default')
