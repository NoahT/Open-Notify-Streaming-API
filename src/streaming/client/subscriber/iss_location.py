'''
NOTE: This is a copy/paste of the model class currently in the ingestion module.
We can later consider exporting this to PyPi to avoid redundancy.
https://github.com/NoahT/Open-Notify-Streaming-API/issues/36

Classes used for reading and upserting ISS location data.
'''


class ISSLocation():
  '''
  Class containg ISS location data.
  '''

  def __init__(self, ts: int, pos_la: float, pos_lo: float) -> None:
    self._ts = ts
    self._pos_la = pos_la
    self._pos_lo = pos_lo

  @staticmethod
  def from_dict(iss_dict: dict):
    iss_document = ISSLocation(ts=iss_dict['ts'],
                               pos_la=iss_dict['pos_la'],
                               pos_lo=iss_dict['pos_lo'])

    return iss_document

  @property
  def iss_dict(self) -> dict:
    iss_dict = {'ts': self._ts, 'pos_la': self._pos_la, 'pos_lo': self._pos_lo}

    return iss_dict

  def __eq__(self, other) -> bool:
    if not isinstance(other, ISSLocation):
      return False
    return (self._ts == other._ts and self._pos_la == other._pos_la and
            self._pos_lo == other._pos_lo)

  def __repr__(self) -> str:
    iss_str = (f'ts={self._ts}, '
               f'pos_la={self._pos_la}, '
               f'pos_lo={self._pos_lo}')

    return iss_str
