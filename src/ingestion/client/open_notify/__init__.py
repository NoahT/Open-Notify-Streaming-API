''' Init module for Open Notify client. '''

from cfg_environ.config import Config

from .client import (FaultTolerantOpenNotifyRequestsClient, OpenNotifyClient,
                     OpenNotifyRequestsClient)


def get_open_notify_client(config: Config) -> OpenNotifyClient:
  open_notify_client = OpenNotifyRequestsClient(config=config)
  fault_tolerant_open_notify_client = FaultTolerantOpenNotifyRequestsClient(
      client=open_notify_client)
  return fault_tolerant_open_notify_client
