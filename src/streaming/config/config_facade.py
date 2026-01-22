"""
  This is again copied and pasted from the ingestion module. A separate
  issue is created to package all of the DRY code into PyPi from a separate
  repository. https://github.com/NoahT/Open-Notify-Streaming-API/issues/36.
  
  Config module with facade pattern to simplify access to only important
  fields. Supports environment-based configuration (development, staging, etc.)
"""
import json
import logging
from abc import ABC, abstractmethod


class Config(ABC):
  """
  Abstract base class for config access.
  """

  @abstractmethod
  def read_str(self, key: str, default: str = None) -> str:
    pass

  @abstractmethod
  def read_bool(self, key: str, default: bool = False) -> bool:
    pass

  @abstractmethod
  def read_list(self, key: str, default: list = None) -> list:
    pass

  @abstractmethod
  def read_dict(self, key: str, default: dict = None) -> dict:
    pass

  @abstractmethod
  def read_int(self, key: str, default: int = 0) -> int:
    pass

  @abstractmethod
  def read_float(self, key: str, default: float = 0) -> float:
    pass


class ConfigFacade(Config):
  """ Facade class for config access. """

  def __init__(
      self,
      config_path: str,
      config_env: str,
      config_env_default: str,
      logger: logging.Logger = logging.getLogger(__name__)
  ) -> None:
    self._config = None
    self._config_path = config_path
    self._config_env = config_env
    self._config_env_default = config_env_default
    self._logger = logger

  def read_str(self, key: str, default: str = None) -> str:
    return self.config[key] or default

  def read_bool(self, key: str, default: bool = False) -> bool:
    return self.config[key] or default

  def read_list(self, key: str, default: list = None) -> list:
    return self.config[key] or default

  def read_dict(self, key: str, default: dict = None) -> dict:
    return self.config[key] or default

  def read_int(self, key: str, default: int = 0) -> int:
    return self.config[key] or default

  def read_float(self, key: str, default: float = 0) -> float:
    return self.config[key] or default

  def _load_config(self, config_path: str, config_env: str) -> dict:
    """
    Load configuration based on the config directory and environemnt.
    
    :param config_path: Relative path: open(..) reads relative path based on 
    current working directory which is not based on this location in source code 
    (it will be based on path of execution for running process in Docker 
    container)
    :type config_path: str
    :param config_env: The environment used for configuration.
    :type config_env: str
    """
    config_file_path = f'{config_path}/{config_env}.json'
    self._logger.info(f'Config file: {config_file_path}')

    config = {}
    with open(config_file_path, 'r', encoding='utf-8') as file:
      config = json.loads(file.read())

    return config

  @property
  def config(self) -> dict:
    if not self._config:
      config_default = self._load_config(self._config_path,
                                         self._config_env_default)
      config_environment = self._load_config(self._config_path,
                                             self._config_env)
      # https://peps.python.org/pep-0448/
      config = {**config_default, **config_environment}
      self._config = config

    return self._config
